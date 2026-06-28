# MediAssist

Agentic RAG system helping rural patients in Andhra Pradesh and Telangana understand prescriptions, symptoms, and government health schemes in Telugu and English.

## Live Demo
Coming soon - deployment in progress

## Team 1 - SolvEmpire AIML Batch
- Sai Laxmi Pasagadugula (Team Lead)
- Hemalatha Kada (RAG Pipeline)
- Vennela Gubbala (Frontend)

## Features
- Prescription reader with OCR support
- Symptom checker with medical document retrieval
- Government health scheme eligibility checker (Aarogyasri, PM-JAY, NHM)
- Multilingual support (Telugu and English)
- Source citation on every answer - no hallucination
- Nearby facility finder
- Dosage reminder generator

## Tech Stack
- LLM: Groq (Llama 3.1 8B Instant)
- RAG Framework: LangChain
- Vector Store: ChromaDB
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- OCR: Tesseract
- Frontend: Streamlit
- Deployment: Render.com

## Setup Instructions
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your `GROQ_API_KEY`
4. Run the app: `streamlit run frontend/app.py`

## Knowledge Base
1302 documents loaded, 5168 chunks indexed, covering Aarogyasri, PM-JAY, NHM guidelines, WHO medicine list, emergency care, first aid, snakebite treatment, burns management, and common illness guidelines.