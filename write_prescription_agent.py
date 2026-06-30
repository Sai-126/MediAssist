content = '''import base64
from agents.base_agent import BaseAgent
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
        self.vision_llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2
        )

    def _read_image_with_vision(self, image_file) -> str:
        image_file.seek(0)
        image_bytes = image_file.read()
        b64_image = base64.b64encode(image_bytes).decode("utf-8")

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": (
                        "This is a photo of a handwritten or printed doctor's prescription, "
                        "possibly in messy handwriting. Carefully read every medicine name, "
                        "dosage, and instruction you can identify, even if the handwriting is "
                        "unclear or in shorthand. List each medicine you can identify on its own "
                        "line in this format: 'Medicine name - dosage - frequency - duration if visible'. "
                        "If a word is genuinely illegible, write 'unclear' for that specific detail only, "
                        "but still list what you can read. Do not skip the attempt - try your best to "
                        "extract real medicine names even from imperfect handwriting, using your knowledge "
                        "of common medicine names to make educated identification of partially visible text."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}
                }
            ]
        )

        response = self.vision_llm.invoke([message])
        return response.content.strip()

    def explain(self, text: str = None, image_file=None, language: str = "english") -> str:
        if image_file is not None:
            try:
                extracted = self._read_image_with_vision(image_file)
            except Exception as e:
                return f"Could not process the prescription image right now. Please try typing the medicine names instead. (Technical detail: {str(e)[:150]})"

            if not extracted or len(extracted) < 5:
                return "Could not read the prescription image clearly. Please try a clearer photo with good lighting, or type the medicine names manually."

            text = extracted

        if not text:
            return "Please provide prescription text or an image."

        docs = self.retrieve(text)
        context = self.format_context(docs)
        lang = "Telugu" if language == "telugu" else "English"

        prompt = f\'\'\'You are a medical assistant helping rural patients in India understand prescriptions.
Use ONLY the information from the context below to answer.
Cite the source document name for every fact you mention.
Respond in {lang}.
If you cannot find specific information about a medicine in the context, say "I do not have detailed information about this specific medicine in my documents" for that medicine only - do not skip it entirely, still mention its name.
Do NOT make up dosage or medical information that is not in the context.

Context:
{context}

Prescription text (extracted from image or typed by user, may contain unclear words marked as "unclear"):
{text}

For each medicine identified above, explain clearly:
- What it is generally used for
- How and when to take it, if mentioned
- Important warnings or side effects, if available in context
- Any food or drink restrictions, if available in context

If a medicine name was marked unclear or you cannot confidently identify it, say so honestly instead of guessing.
Use simple words a patient with no medical background can understand.\'\'\'

        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
'''

with open("agents/prescription_agent.py", "w", encoding="utf-8") as f:
    f.write(content)

print("prescription_agent.py written successfully!")