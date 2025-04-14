# PARSE & STORE 'MYSCALE' DOCUMENTS

## Setting Up the Virtual Environment and Running the Application

1- Ensure you're in the `./parse-store` directory, then run the following commands:

```bash
py -m pip cache purge
py -m venv .\.venv
.\.venv\Scripts\activate
.\.venv\Scripts\python.exe -m pip cache purge
.\.venv\Scripts\python.exe -m pip install --upgrade pip wheel build setuptools
.\.venv\Scripts\python.exe -m pip --no-cache-dir install --use-pep517 -e .
```

2- Cleaning "__pycache__" from the project:

```powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```

or

```bash
for /d /r %i in (__pycache__) do rmdir /s /q "%i"
```

3- Launching the Application, execute:

```bash
parse_store
```

or

```bash
.\.venv\Scripts\python.exe -m parseandstore
```

4- Managing Dependencies: When a new package is required, simply add it to the install_requires section in the setup.cfg file, specifying the desired version.

## How to use the application

### Development Mode

### Basic Usage

## Documentation

- langchain text split: <https://medium.com/@harsh.vardhan7695/mastering-text-splitting-in-langchain-735313216e01>
- langchain vector store: <https://medium.com/@vladris/embeddings-and-vector-databases-732f9927b377>
- vector search: <https://medium.com/@vladris/vector-search-with-langchain-and-chroma-db-926738443e70>
- ollama structured output: <https://ollama.com/blog/structured-outputs>