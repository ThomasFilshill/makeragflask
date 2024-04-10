class Config():
    DATA_ROOT = 'data'
    PDF_ROOT = f'{DATA_ROOT}/pdf'
    MARKDOWN_ROOT = f'{DATA_ROOT}/markdown'
    JSON_ROOT = f'{DATA_ROOT}/json'
    CHROMA_PATH = "chroma"

    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """