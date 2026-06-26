from agents.base_agent import BaseAgent
from agents.ocr_tool import extract_text_from_image
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

class PrescriptionAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.3
        )

    def explain(self, text: str = None, image_file=None, language: str = "english") -> str:
        if image_file is not None:
            text = extract_text_from_image(image_file)
            if not text:
                return "Could not read any text from the uploaded image. Please try a clearer photo or type the prescription manually."

        if not text:
            return "Please provide prescription text or an image."

        docs = self.retrieve(text)
        context = self.format_context(docs)
        lang = "Telugu" if language == "telugu" else "English"

        prompt = f"""You are a medical assistant helping rural patients in India understand prescriptions.
Use ONLY the information from the context below to answer.
Cite the source document name for every fact you mention.
Respond in {lang}.
If you cannot find the answer in the context, say "I don't have information about this medicine in my documents."
Do NOT make up information.

Context:
{context}

Prescription text:
{text}

Explain each medicine clearly:
- What it is used for
- How and when to take it
- Important warnings or side effects
- Any food or drink restrictions
Use simple words a patient with no medical background can understand."""

        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content