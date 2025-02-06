# mypy: ignore-errors
import os

import nest_asyncio
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse

nest_asyncio.apply()

load_dotenv()

instructions0 = """
Extract all technical, regulatory, and operational information related to the railway domain, including but not limited to signaling systems (ERTMS/ETCS, interlocking, GSM-R, RBC, balises), railway safety and certification (CSM, RAMS, SIL levels, fail-safe principles), infrastructure and rolling stock requirements, operational rules and technical specifications (TSIs), European railway regulations, and relevant UNISIG subsets (e.g., Subset-026, Subset-034), while excluding general introductions, legal disclaimers, duplicate content, and non-technical annexes unless they contain essential railway-related data.
if any math equation is found output it in LATEX markdown (between $$)
if any table is found output it markdown Table
"""

instructions1 = """
Extract all technical, regulatory, and operational information related to the railway domain, including but not limited to signaling systems (ERTMS/ETCS, interlocking, GSM-R, RBC, balises), railway safety and certification (CSM, RAMS, SIL levels, fail-safe principles), infrastructure and rolling stock requirements, operational rules and technical specifications (TSIs), European railway regulations, and relevant UNISIG subsets (e.g., Subset-026, Subset-034), while excluding general introductions, legal disclaimers, duplicate content, and non-technical annexes unless they contain essential railway-related data.
if any math equation is found output it in LATEX markdown (between $$)
if any table is found output it markdown Table
"""

instructions = """
If any mathematical equation is found, output it in LaTeX markdown format between double dollar signs ($$...$$).
If any table is found, output it in Markdown table format using pipes (|) and dashes (-) for structure.
"""

SUBSET26_DIR = r"./subset-026"

# set up parser
parser = LlamaParse(
    api_key=os.getenv('LLAMA_CLOUD_API_KEY_2'),
    result_type="markdown",
    parsing_instruction=instructions0
)


if __name__ == '__main__':

    os.makedirs(r"./md_subset_026/", exist_ok=True)

    for path in os.listdir(SUBSET26_DIR):
        output_f = os.path.join(r"./md_subset_026/", f'{os.path.splitext(path)[0]}.md')
        path = os.path.join(SUBSET26_DIR, path)

        if path != r'./subset-026\index003_-_SUBSET-023_v400.pdf':
            continue

        with open(output_f, 'w', encoding='utf-8') as md_file:
            for doc in parser.load_data(path):
                try:
                    md_file.write(doc.text + '\n')
                except UnicodeDecodeError as ee:
                    print(ee)
