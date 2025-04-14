# type: ignore
import json
import os
from pathlib import Path

from colorama import Fore, Style
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from llama_parse import LlamaParse

from .store import VecStore

load_dotenv()


class Parser:
    def __init__(self, output_dir: str = r'./output_md'):
        self.store = VecStore()

        self.parser = LlamaParse(
            api_key=os.getenv('LLAMA_CLOUD_API_KEY_22kam'),
            result_type="markdown",
            verbose=True,
        )

        self.semantic_splitter = SemanticChunker(
            embeddings=self.get_embedding(model="bge-m3"),
            breakpoint_threshold_type="gradient"
        )

        self.batch_size = 15
        self.table_name = self.store.table_name

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.hash_embed: dict[str, str] = {}

    def get_embedding(self, model: str = "nomic-embed-text"):
        """ Get embeddings from Ollama """
        return OllamaEmbeddings(model=model)

    def embed_content(self, content: str):
        """ Get embeddings from 'google.generativeai' """
        embedd_mod = self.get_embedding() # model="mxbai-embed-large:latest")
        return embedd_mod.embed_query(content)

    def process_directory(self, directory: str) -> None:
        """ Process all files in the data directory and save the output to the output directory """
        batch_data: list[tuple[int, list[float]]] = []
        iterator = self.store.get_last_id() + 1

        for path in Path(directory).glob("*.pdf"):
            folder_path = self.output_dir / path.stem
            folder_path.mkdir(exist_ok=True)

            # load data
            print(f"{Fore.GREEN}Loading data from : {path}{Style.RESET_ALL}")
            data = self.parser.load_data(file_path=path)

            # joining
            documents = self.semantic_splitter.create_documents(
                [''.join(doc.text for doc in data)])
            print(f"{Fore.GREEN}Semantic Splitting of: {path}{Style.RESET_ALL}")

            for document in documents:
                # chunck saving
                output_file = folder_path / f"{iterator}.md"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(document.page_content)

                # Vectore DataBase
                content_embed = self.embed_content(document.page_content)
                print(f"{Fore.GREEN}Document {iterator} embedded ( len : {len(content_embed)} ){Style.RESET_ALL}")

                self.hash_embed[iterator] = os.path.join(os.getcwd(), output_file)

                batch_data.append((
                        iterator,
                        content_embed
                ))

                if len(batch_data) >= self.batch_size:
                    self.store.insert(batch_data)
                    batch_data = []

                iterator += 1

        if batch_data:
            self.store.insert(batch_data, vect_index=True)

        self.save_hash()
        return

    def save_hash(self):
        """ save the related path to a json file """
        with open(r'./misc/store_data.json', 'w') as hash_f:
            json.dump(self.hash_embed, hash_f, indent=4)
