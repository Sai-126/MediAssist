from agents.base_agent import BaseAgent
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

class SymptomAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = ChatNVIDIA(
            model="meta/llama-3.1-8b-instruct",
            api_key=os.getenv("NVIDIA_API_KEY"),
            temperature=0.3
        )

    def check(self, symptoms: str, language: str = "english") -> str:
        docs = self.retrieve(symptoms)
        context = self.format_context(docs)
        lang = "Telugu" if language == "telugu" else "English"

        prompt = f"""You are a health information assistant for rural patients in India.
Use ONLY the context below to answer.
Cite the source document name for every fact.
Respond in {lang}.
Do NOT diagnose. Always end with "Please consult a qualified doctor."
If you cannot find relevant information, say so honestly.

Context:
{context}

Patient symptoms:
{symptoms}

List:
- Possible conditions matching these symptoms
- General advice
- Warning signs that need immediate hospital visit"""

        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content