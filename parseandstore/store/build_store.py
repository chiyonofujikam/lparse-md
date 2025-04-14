import json
import os

from clickhouse_connect import get_client
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from tqdm import tqdm

load_dotenv()

class VecStore:
    def __init__(self, data_dir: str, batch_size: int=300,
                 table_name: str="ERA_DATA", build: bool=True):
        self.batch_size = batch_size
        self.table_name = table_name
        self.build = build
        self.content_dict: dict[int, tuple[str, str]] = {}

        self.client = self.get_client()

        self.splitter = self.get_splitter()

        self.build_store(data_dir)

    def get_client(self):
        """ Get 'MYSCALE' client """
        return get_client(
                host=os.getenv('MYSCALE_HOST'),
                port=os.getenv('MYSCALE_PORT'),
                username=os.getenv('MYSCALE_USERNAME'),
                password=os.getenv('MYSCALE_PASSWORD')
        )

    def get_embeddings(self, model: str):
        """ Get embeddings from 'google.generativeai' """
        return OllamaEmbeddings(model=model)

    def embed_content(self, content: str):
        """ Get embeddings from 'google.generativeai' """
        embeddings = self.get_embeddings(model="nomic-embed-text")
        return embeddings.embed_query(content)

    def get_splitter(self):
        """ Get splitter from 'langchain_text_splitters' """
        embeddings = self.get_embeddings(model="nomic-embed-text")
        return SemanticChunker(
            embeddings,
            min_chunk_size=300,
            breakpoint_threshold_type="gradient"
        )

    def create_table(self):
        """ Create table in 'MYSCALE' """
        # create table
        query = f"""
            CREATE TABLE {self.table_name} (
                id Int64,
                embeddings Array(Float32),
                CONSTRAINT check_data_length CHECK length(embeddings) = 768
            ) ENGINE = MergeTree()
            ORDER BY id
        """
        self.client.command(query)
        print("\nTable created successfully")

    def create_vector_index(self):
        """ Create vector index in 'MYSCALE' """
        self.client.command(f"""
            ALTER TABLE {self.table_name}
            ADD VECTOR INDEX vector_index embeddings
            TYPE MSTG ('metric_type=Cosine');
        """)
        print("\nVector index created successfully")

    @classmethod
    def insert_to_existing(cls, data_dir: str, batch_size: int=300, table_name: str="ERA_DATA", build: bool=False):
        """ Class method to create instance and insert data without table creation """
        store = cls(data_dir="", batch_size=batch_size, table_name=table_name, build=build)
        store.insert_data(data_dir)
        return store

    def get_loader_md(self, md_file: str):
        """ Get loader from 'langchain_community.document_loaders' """
        with open(md_file, "r", encoding="utf-8") as md:
            text = md.read()

        docs = self.splitter.create_documents([text])
        print(f"Created {len(docs)} semantic chunks from {md_file}")
        return docs

    def get_last_id(self) -> int:
        """Get the highest ID from the existing table"""
        try:
            result = self.client.query(f"SELECT MAX(id) as max_id FROM {self.table_name}")
            last_id = result.first_row[0]
            return last_id if last_id is not None else -1
        except Exception as e:
            print(f"Error getting last ID: {e}")
            return -1

    def insert_data(self, dir_path: str):
        """ Get dataframe from directory """
        current_id = self.get_last_id() + 1
        batch_data: list[tuple[int, list[float]]] = []
        self.content_dict = {}

        try:
            for path in os.listdir(dir_path):

                path = os.path.join(dir_path, path)
                if not os.path.isfile(path):
                    print(f"Not a file: {path}")
                    continue

                if not path.endswith('.md'):
                    print(f"\nNot a markdown file: {path}")
                    continue
    
                for doc in tqdm(self.get_loader_md(path), desc=f"Processing {path}"):
                    self.content_dict[current_id] = (path, doc.page_content)
                    batch_data.append((current_id, self.embed_content(doc.page_content)))

                    if len(batch_data) >= self.batch_size:
                        self.client.insert(
                            table=self.table_name,
                            column_names=['id', 'embeddings'],
                            data=batch_data)

                        print(f"\nBatch of {len(batch_data)} records inserted.")
                        batch_data = []

                    current_id += 1

            if batch_data:
                try:
                    self.client.insert(
                        table=self.table_name,
                        column_names=['id', 'embeddings'],
                        data=batch_data)
                    print(f"\nFinal batch of {len(batch_data)} records inserted.")
                except Exception as e:
                    print(f"Error inserting final batch: {e}")
        
        except Exception as e:
            print(f"\nError during data insertion: {e}")

        with open(f"{self.table_name}_content.json", "w") as j_file:
            json.dump(self.content_dict, j_file)

        print("\nData inserted successfully")

    def build_store(self, data_dir: str):
        """ Build store from markdown files """
        if not self.build:
            return

        # create MYSCALE table
        self.create_table()

        # insert data into MYSCALE table
        self.insert_data(data_dir)

        # create vector index
        self.create_vector_index()

        print("\nStore built successfully")

if __name__ == "__main__":
    # ? TODO: change data_dir to the path of the directory containing the markdown files
    VecStore(data_dir=r"./data/md_subset_026/", batch_size=20,
             table_name="SUBSET_026", build=True)
