# MediAssist — System Architecture

## Agent Flow
User query → Streamlit UI → Orchestrator → [Prescription / Symptom / Scheme] Agent → RAG retrieval → LLM generation → Response with source citation → UI

## Orchestrator Logic
Receives query_type from UI tab and routes to the correct agent.
Can combine outputs from multiple agents if needed.

## Agent Responsibilities
- Prescription Agent: reads medicine names from text/OCR, retrieves from medical RAG, returns plain-language explanation with dosage
- Symptom Agent: takes described symptoms, retrieves matching conditions from medical PDFs, returns possible conditions with disclaimer
- Scheme Agent: takes patient profile, retrieves from scheme documents, returns eligibility result with application steps

## Why Removing One Agent Breaks the System
- Without Prescription Agent: cannot explain medicines
- Without Symptom Agent: cannot handle symptom queries
- Without Scheme Agent: cannot check eligibility
Each agent retrieves from different document types — swapping them returns irrelevant results.

## Tools Used
- Prescription Agent: Tesseract OCR, ChromaDB retrieval, Gemini 2.5 Flash
- Symptom Agent: ChromaDB retrieval, Gemini 2.5 Flash
- Scheme Agent: ChromaDB retrieval, Gemini 2.5 Flash

## Tech Stack
- LLM: Gemini 2.5 Flash
- RAG Framework: LangChain
- Vector Store: ChromaDB
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Frontend: Streamlit
- Deployment: Render.com