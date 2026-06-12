from agents.prescription_agent import PrescriptionAgent
from agents.symptom_agent import SymptomAgent
from agents.scheme_agent import SchemeAgent

class Orchestrator:
    def __init__(self):
        self.prescription_agent = PrescriptionAgent()
        self.symptom_agent = SymptomAgent()
        self.scheme_agent = SchemeAgent()

    def route(self, query_type: str, query: str, language: str = "english") -> str:
        if query_type == "prescription":
            return self.prescription_agent.explain_prescription(query, language)
        elif query_type == "symptoms":
            return self.symptom_agent.check_symptoms(query, language)
        elif query_type == "scheme":
            return self.scheme_agent.check_eligibility(query, language)
        else:
            return "Please select a valid query type: prescription, symptoms, or scheme."
