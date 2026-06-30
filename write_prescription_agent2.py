content = '''import base64
from agents.base_agent import BaseAgent
from agents.image_preprocess import preprocess_prescription_image
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
            temperature=0.1
        )

    def _image_to_b64(self, image_buffer) -> str:
        image_buffer.seek(0)
        return base64.b64encode(image_buffer.read()).decode("utf-8")

    def _read_image_with_vision(self, image_file) -> str:
        processed = preprocess_prescription_image(image_file)
        b64_image = self._image_to_b64(processed)

        first_pass_prompt = (
            "You are reading a photo of a doctor's prescription, which may have messy "
            "handwriting, circled numbers, underlines, and medical shorthand. "
            "Look very carefully at each line. For each medicine you see, look for these clues: "
            "a circled number usually means quantity, underlined text is usually the medicine name, "
            "abbreviations like Tab/Cap/T/Inj mean tablet/capsule/injection. "
            "List every medicine line you can find, in this exact format: "
            "'Medicine name | dosage | frequency | duration | confidence(high/medium/low)'. "
            "Only mark confidence as high if you are genuinely certain of the medicine name based on "
            "clear letter shapes. Mark medium if it is a reasonable guess based on partial letters and "
            "common Indian medicine name patterns. Mark low if you are mostly guessing. "
            "Never invent a medicine name that does not match any visible letters in the image - "
            "if a word's letters genuinely don't form a recognizable medicine, write 'illegible' as the name "
            "instead of substituting a different real medicine name that you simply recognize from training data."
        )

        message = HumanMessage(
            content=[
                {"type": "text", "text": first_pass_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
            ]
        )
        first_response = self.vision_llm.invoke([message]).content.strip()

        verify_prompt = (
            "Here is a first-pass reading of a prescription image:\\n\\n"
            f"{first_response}\\n\\n"
            "Now look at the SAME image again very carefully one more time. "
            "Check each medicine name against the actual letters visible in the image. "
            "If any medicine name was likely wrong or hallucinated and does not actually match "
            "the letter shapes in the image, correct it or mark it 'illegible' instead. "
            "If a medicine name looks correct, keep it as is. "
            "Output the corrected final list in the same format: "
            "'Medicine name | dosage | frequency | duration | confidence(high/medium/low)'."
        )

        message2 = HumanMessage(
            content=[
                {"type": "text", "text": verify_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
            ]
        )
        verified_response = self.vision_llm.invoke([message2]).content.strip()
        return verified_response

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

The prescription reading below includes a confidence level for each medicine (high/medium/low) and may
include entries marked "illegible" where the handwriting could not be confidently read.

Rules:
- For "illegible" entries, clearly tell the patient this could not be read and they should ask their pharmacist or doctor to confirm.
- For "low" confidence entries, mention this is an uncertain reading and should be verified.
- For "high" and "medium" confidence entries, explain normally using the context documents.
- If you cannot find specific information about a medicine in the context, say "I do not have detailed information about this specific medicine in my documents" for that medicine only.
- Do NOT make up dosage or medical information that is not in the context.

Context:
{context}

Prescription reading (with confidence levels):
{text}

For each medicine, explain clearly:
- What it is generally used for (if known and high/medium confidence)
- How and when to take it, if mentioned
- Important warnings or side effects, if available in context
- Any food or drink restrictions, if available in context

Use simple words a patient with no medical background can understand.\'\'\'

        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
'''

with open("agents/prescription_agent.py", "w", encoding="utf-8") as f:
    f.write(content)

print("prescription_agent.py (v2 with two-pass verification) written successfully!")