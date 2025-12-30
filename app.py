import pinecone
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama
import json

# 1. Pinecone setup
pinecone.init(
    api_key="pcsk_MXUms_KvUrXQTNGNRQhCBVqG5MopjAW6j3NyYCocF1VtbvXZ55attS11ozDd5V99Ucaw8",
    environment="gcp-starter"
)

index_name = "vuln-index"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=384)

index = pinecone.Index(index_name)

# 2. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 3. Read vulnerability docs
with open("data/owasp_top10.txt") as f:
    docs = f.readlines()

vectors = []
for i, text in enumerate(docs):
    emb = model.encode(text).tolist()
    vectors.append((str(i), emb, {"text": text}))

index.upsert(vectors)

# 4. Load user input
with open("sample_input.txt") as f:
    user_input = f.read()

query_vector = model.encode(user_input).tolist()

# 5. Search similar vulnerability
result = index.query(
    vector=query_vector,
    top_k=2,
    include_metadata=True
)

context = ""
for match in result["matches"]:
    context += match["metadata"]["text"]

# 6. Load LLaMA GGUF
llm = Llama(
    model_path="models/llama.gguf",
    n_ctx=2048
)

# 7. Ask LLaMA
prompt = f"""
Analyze the code and identify security issues.

Code:
{user_input}

Reference:
{context}

Return JSON only:
{{
  "vulnerability": "",
  "severity": "",
  "description": "",
  "impact": "",
  "remediation": []
}}
"""

response = llm(prompt, max_tokens=300)
text = response["choices"][0]["text"]

print(json.dumps(json.loads(text), indent=2))
