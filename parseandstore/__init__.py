# type: ignore

import json
import os

from colorama import Fore, Style

from .parser import Parser

__version__ = '0.1.0'

def get_config():
    p0 = r"C:\Users\Consultant\OneDrive - IKOSCONSULTING\Bureau\lparse-md\era_md_files"
    json_dict = {}
    for item in os.listdir(p0):
        p1 = os.path.join(p0, item)
        for path in os.listdir(p1):
            path = os.path.join(p1, path)
            json_dict[int(os.path.basename(path).replace('.md', ''))] = path

    with open(r'C:\Users\Consultant\railai_1\data\store_data.json', 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, indent=4)


def start():
    """ entry point for the application """
    print(f'{Fore.GREEN}Starting parse-store{Style.RESET_ALL}')
    parser = Parser(output_dir=r'./era_md_files')

    # parser.process_directory(r'.\downloads\395') # done
    # parser.process_directory(r'.\downloads\ba') # done
    # parser.process_directory(r'.\downloads\chunk_1') # done
    # parser.process_directory(r'.\downloads\chunk_2') # done
    # parser.process_directory(r'.\downloads\chunk_3') # done
    # parser.process_directory(r'.\downloads\chunk_4') # done
    # parser.process_directory(r'.\downloads\chunk_5') # done
    # parser.process_directory(r'.\downloads\chunk_6') # done
    # parser.process_directory(r'.\downloads\chunk_7') # done
    # parser.process_directory(r'.\downloads\chunk_7_rev') # done
    # parser.process_directory(r'.\downloads\chunk_8') # done
    # parser.process_directory(r'.\downloads\chunk_9') # done
    # parser.process_directory(r'.\downloads\chunk_10') # done
    # parser.process_directory(r'.\downloads\chunk_11') # done
    # parser.process_directory(r'.\downloads\chunk_11_rev') # done
    # parser.process_directory(r'.\downloads\chunk_12') # done
    # parser.process_directory(r'.\downloads\chunk_13') # done
    # parser.process_directory(r'.\downloads\chunk_14') # done
    # parser.process_directory(r'.\downloads\chunk_15') # done
    # parser.process_directory(r'.\downloads\chunk_16') # done
    # parser.process_directory(r'.\downloads\chunk_17') # done
    # parser.process_directory(r'.\downloads\chunk_18') # done

    parser.process_directory(r'.\downloads\g_files')
    get_config()
