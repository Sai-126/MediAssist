from agents.base_agent import BaseAgent
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

class SchemeAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.3
        )

    def check_eligibility(self, profile: dict, language: str = "english") -> str:
        query = f"eligibility criteria income {profile.get('income')} family {profile.get('family_size')} district {profile.get('district')}"
        docs = self.retrieve(query)
        context = self.format_context(docs)
        lang = "Telugu" if language == "telugu" else "English"

        prompt = f"""You are a government health scheme assistant for rural patients in India.
Use ONLY the context below to answer.
Cite the scheme document name for every fact.
Respond in {lang}.
If you cannot find eligibility information, say so honestly.

Context:
{context}

Patient profile:
- District: {profile.get('district')}
- Annual income: Rs.{profile.get('income')}
- Age: {profile.get('age')}
- Family size: {profile.get('family_size')}
- Category: {profile.get('category')}

List:
- Which schemes this patient qualifies for (Aarogyasri, PM-JAY, NHM)
- Benefits available
- Steps to apply"""

        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content