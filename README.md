This project is a mini AI-based security vulnerability analysis system.
It analyzes:
Vulnerable code snippets
Security scan outputs
Dependency lists
The system uses vector embeddings + Pinecone + a local LLaMA GGUF model to identify security vulnerabilities and generate a structured vulnerability report.

System Architecture:
User Input (code / scan output)
        ↓
Text Embeddings
        ↓
Pinecone Vector Database
        ↓
Relevant Vulnerability Context
        ↓
Local LLaMA GGUF Model
        ↓
Structured JSON Vulnerability Report
