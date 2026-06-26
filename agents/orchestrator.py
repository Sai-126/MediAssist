from agents.prescription_agent import PrescriptionAgent
from agents.symptom_agent import SymptomAgent
from agents.scheme_agent import SchemeAgent

class Orchestrator:
    def __init__(self):
        print("Loading agents...")
        self.prescription_agent = PrescriptionAgent()
        self.symptom_agent = SymptomAgent()
        self.scheme_agent = SchemeAgent()
        print("All agents ready.")

    def route(self, query_type: str, query=None, image_file=None,
              profile: dict = None, language: str = "english") -> str:

        if query_type == "prescription":
            if not query and not image_file:
                return "Please provide prescription text or upload an image."
            return self.prescription_agent.explain(text=query, image_file=image_file, language=language)

        elif query_type == "symptoms":
            if not query:
                return "Please describe your symptoms."
            return self.symptom_agent.check(query, language)

        elif query_type == "scheme":
            if not profile:
                return "Please provide patient details."
            return self.scheme_agent.check_eligibility(profile, language)

        else:
            return "Invalid query type. Choose: prescription, symptoms, or scheme."