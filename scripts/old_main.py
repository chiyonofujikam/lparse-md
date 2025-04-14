# mypy: ignore-errors
import json
import os

import nest_asyncio
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse

nest_asyncio.apply()

load_dotenv()

instructions = """
Extract all technical, regulatory, and operational information related to the railway domain,
including but not limited to signaling systems, railway safety and certification,
infrastructure and rolling stock requirements, operational rules and technical specifications,
European railway regulations, and relevant UNISIG subsets,
while excluding general introductions, legal disclaimers, duplicate content
and non-technical annexes unless they contain essential railway-related data.
"""

content_guidelines = """
Extract all technical, regulatory, and operational information related to the railway domain.
Structure the extracted data into clearly defined sections.
Excluding general introductions, legal disclaimers, duplicate content and non-technical annexes unless they contain essential railway-related informations.
If any mathematical equation is found, output it in LaTeX markdown format between double dollar signs ($$...$$).
If any table is found, output it in Markdown table format using pipes (|) and dashes (-) for structure.
"""

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

instructions2 = """
If any mathematical equation is found, output it in LaTeX markdown format between double dollar signs ($$...$$).
If any table is found, output it in Markdown table format using pipes (|) and dashes (-) for structure.
"""


# set up parser
parser = LlamaParse(
    api_key=os.getenv('LLAMA_CLOUD_API_KEY'),
    result_type="markdown",
    # parsing_instruction=instructions,
    content_guideline_instruction=content_guidelines,
)

with open('./data/file1111.md', 'w', encoding='utf-8') as md_file:
    for doc in parser.load_data('./data/file.pdf'):
        try:
            md_file.write(doc.text + '\n')
        except UnicodeDecodeError as ee:
            print(ee)

# # use SimpleDirectoryReader to parse our file
# file_extractor = {".pdf": parser}
# documents = SimpleDirectoryReader(input_files=['data/file.pdf'], file_extractor=file_extractor).load_data()
# with open('./data/file_.md', 'w') as f:
#     for doc in documents:
#         f.write(doc.text)
