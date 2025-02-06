# mypy: ignore-errors
import os
import shutil

from PyPDF2 import PdfReader

TOTAL = 0
PDFS_DIR = r"C:\Users\Consultant\OneDrive - IKOSCONSULTING\Bureau\scrap-files\downloads\pdf"
SUBSET26_DIR = r"./subset-026"

def get_num_pages(path: str) -> int:
    try:
        with open(path, 'rb') as pdf_f:
            return len(PdfReader(pdf_f).pages)
    except Exception as err:
        print(f"Exception: {err}")
        return 0

def chunk():
    """ dived the PDFS dir into folder s of pdf that has a maximum of 1000 pages all"""
    os.makedirs(r"./downloads/g_files/", exist_ok=True)

    total = 0
    chunk = 1
    files_pdf = ()

    for path in os.listdir(PDFS_DIR):
        path = os.path.join(PDFS_DIR, path)

        pdf_pages = get_num_pages(path)
        if pdf_pages > 1000:
            shutil.copyfile(path, os.path.join(r"./downloads/g_files/", os.path.basename(path)))
            # TOTAL += pdf_pages
            continue

        total += pdf_pages
        # TOTAL += pdf_pages

        if total < 1000:
            files_pdf += (path,)
            continue

        # creates a folder
        chunk_p = os.path.join(r"./downloads", f"chunk_{chunk}")
        os.makedirs(chunk_p, exist_ok=True)

        for src in files_pdf:
            dest = os.path.join(chunk_p, os.path.basename(src))
            shutil.copyfile(src, dest)

        total = get_num_pages(path)
        files_pdf = (path, )
        chunk += 1

    # print(f"Overall number of pages in {PDFS_DIR}: {TOTAL}")

if __name__ == '__main__':
    # chunk()
    for path in os.listdir(SUBSET26_DIR):
        path = os.path.join(PDFS_DIR, path)

        pdf_pages = get_num_pages(path)
        TOTAL += pdf_pages

    print(f"Overall number of pages in {SUBSET26_DIR}: {TOTAL}")
