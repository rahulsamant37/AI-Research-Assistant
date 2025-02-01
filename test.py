import pytesseract
from pdf2image import convert_from_path
from transformers import BertTokenizer, BertModel
import torch
import pathway as pw
from pathway.xpacks.llm.vector_store import VectorStoreServer

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def pdf_to_text(pdf_path):
    """
    Convert PDF to text using OCR.
    """
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=300)
    text = ''
    for image in images:
        # Perform OCR on each image
        text += pytesseract.image_to_string(image)
    return text

def extract_features(text):
    """
    Extract BERT features from text.
    """
    # Tokenize input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    # Obtain hidden states from BERT
    with torch.no_grad():
        outputs = model(**inputs)
    # Extract the embeddings of the [CLS] token
    cls_embeddings = outputs.last_hidden_state[:, 0, :]
    return cls_embeddings

# Define the embedding function
def embedding_function(texts):
    """
    Convert a list of texts to their BERT embeddings.
    """
    embeddings = []
    for text in texts:
        embedding = extract_features(text)
        embeddings.append(embedding.squeeze().numpy())
    return embeddings

# Specify the path to your documents
document_path = './sample_docs'

documents = pw.io.fs.read(document_path, format='plaintext', mode='static', with_metadata=True)

# Initialize the vector store without the 'data_sources' parameter
vector_store = VectorStoreServer(
    docs=documents,
    embedder=embedding_function
)

vector_store.run_server(host='localhost', port=8080)

def store_vector(pdf_path):
    # Extract text from PDF
    text = pdf_to_text(pdf_path)
    # Store the text in the vector store
    vector_store.add_texts([text], metadatas=[{"pdf_path": pdf_path}])
    print(f"Vector for {pdf_path} stored in the vector store.")

if __name__ == "__main__":
    pdf_path = 'artifacts/data_ingestion/Non-Publishable/R001.pdf'
    store_vector(pdf_path)
