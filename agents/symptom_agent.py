from agents.base_agent import BaseAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

class SymptomAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def check_symptoms(self, symptoms: str, language: str = "english") -> str:
        context = self.retrieve(symptoms)
        context_str = "\n".join(context)
        lang_instruction = "Respond in Telugu." if language == "telugu" else "Respond in English."
        prompt = f"""You are a health assistant. Based only on the context below,
describe what conditions may match the symptoms. Do NOT diagnose.
Always say: Please visit a doctor for proper diagnosis.
{lang_instruction}

Context:
{context_str}

Symptoms: {symptoms}"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
