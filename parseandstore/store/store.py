import os
from colorama import Fore, Style, init

from clickhouse_connect import get_client
from dotenv import load_dotenv

load_dotenv()

class VecStore:
    def __init__(self, table_name: str="ERA_DATA"):
        self.table_name = table_name
        self.client = get_client(
            host=os.getenv('MYSCALE_HOST', default=""),
            port=int(os.getenv('MYSCALE_PORT', default=443)),
            username=os.getenv('MYSCALE_USERNAME', default=""),
            password=os.getenv('MYSCALE_PASSWORD', default="")
        )
        self.create_table()

    def create_table(self):
        """ Create table in 'MYSCALE' """
        # create table: len Bg3 1024
        query = f"""
            CREATE TABLE {self.table_name} (
                id Int64,
                embeddings Array(Float32),
                CONSTRAINT check_data_length CHECK length(embeddings) = 768
            ) ENGINE = MergeTree()
            ORDER BY id
        """
        try:
            self.client.command(query)
            print(f"\n{Fore.GREEN}Table created successfully{Style.RESET_ALL}")
        except Exception as err:
            print(f"\n{Fore.YELLOW}{err}{Style.RESET_ALL}")

    def create_vector_index(self):
        """ Create vector index in 'MYSCALE' """
        query = f"""
            ALTER TABLE {self.table_name}
            ADD VECTOR INDEX vector_index embeddings
            TYPE MSTG ('metric_type=Cosine');
        """
        try:
            self.client.command(query)
            print(f"\n{Fore.GREEN}Vector index created successfully{Style.RESET_ALL}")
        except Exception as err:
            print(f"\n{Fore.YELLOW}{err}{Style.RESET_ALL}")

    def get_last_id(self) -> int:
        """Get The highest 'ID' from the existing table"""
        try:
            result = self.client.query(
                f"SELECT MAX(id) as max_id FROM {self.table_name}"
            )
            last_id = result.first_row[0]
            return last_id if last_id is not None else -1
        except Exception as e:
            print(f"Error getting last ID: {e}")
            return -1

    def insert(self, batch_data: list[tuple[int, list[float]]],
               vect_index: bool=False) -> None:
        """ Insert into DataBase 'MYSCALE' """
        self.client.insert(
            table=self.table_name,
            column_names=['id', 'embeddings'],
            data=batch_data
        )
        print(f"\nBatch of {len(batch_data)} records inserted.")
        if vect_index:
            self.create_vector_index()
