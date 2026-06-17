from agents.base_agent import BaseAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

class PrescriptionAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def explain_prescription(self, text: str, language: str = "english") -> str:
        context = self.retrieve(text)
        context_str = "\n".join(context)
        lang_instruction = "Respond in Telugu." if language == "telugu" else "Respond in English."
        prompt = f"""You are a medical assistant helping rural patients understand prescriptions.
Use only the information from the context below. Cite the source document name for each fact.
{lang_instruction}

Context:
{context_str}

Prescription text: {text}

Explain each medicine in simple words a patient can understand."""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
