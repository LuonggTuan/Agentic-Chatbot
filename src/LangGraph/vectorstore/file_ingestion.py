from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os
import tempfile
from src.LangGraph.vectorstore.embedding_model.all_MiniLM_model import AllMiniLMModel

def ingest_uploaded_file(uploaded_file, embedding_model: str, vectorstore_path: str):
    suffix = os.path.splitext(uploaded_file.name)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        # Chọn loader phù hợp
        if suffix == ".txt":
            loader = TextLoader(tmp_file_path, encoding='utf-8')
        elif suffix == ".pdf":
            loader = PyPDFLoader(tmp_file_path)
        elif suffix == ".docx":
            loader = Docx2txtLoader(tmp_file_path)
        else:
            raise ValueError("Unsupported file type")

        # Tải và chia nhỏ văn bản
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        print(chunks)
        # Tải mô hình embedding
        embedding_model = AllMiniLMModel(embedding_model).get_embedding_model()

        # Đưa vào vectorstore
        vectorstore = Chroma.from_documents(chunks, embedding_model, persist_directory=vectorstore_path)

        if len(chunks):
            print(f"Successfully processed {len(chunks)} chunks from {uploaded_file.name} and stored in vectorstore.")
            return True
        else:
            return False

    finally:
        # Xoá file tạm nếu tồn tại
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)