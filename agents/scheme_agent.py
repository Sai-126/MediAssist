from agents.base_agent import BaseAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

class SchemeAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def check_eligibility(self, profile: str, language: str = "english") -> str:
        context = self.retrieve(profile)
        context_str = "\n".join(context)
        lang_instruction = "Respond in Telugu." if language == "telugu" else "Respond in English."
        prompt = f"""You are a government scheme advisor for rural patients in AP and Telangana.
Based only on the context below, tell if the patient qualifies for Aarogyasri, PM-JAY, or NHM schemes.
Cite which document each eligibility rule comes from.
{lang_instruction}

Context:
{context_str}

Patient profile: {profile}"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
