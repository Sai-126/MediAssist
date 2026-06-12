# MediAssist - Test Plan

## RAG Tests (Hema)
- Query: "What is Aarogyasri?" -> must retrieve from Aarogyasri PDF
- Query: "Paracetamol dosage" -> must return from medical_faqs.txt
- Query: "NHM scheme AP" -> must retrieve NHM document chunk

## Agent Tests (Sai Laxmi)
- Prescription agent with sample text -> returns explanation with source citations
- Symptom agent with "fever and cough" -> returns conditions, not a diagnosis
- Scheme agent with low income profile -> correctly identifies eligibility

## UI Tests (Vennela)
- File upload works without crashing
- Telugu/English toggle visible and saves preference
- All 3 tabs load correctly
- Mobile display still readable

## Integration Tests (Week 3)
- Full flow: upload prescription -> agent -> explanation shown in UI
- Language toggle switches response language correctly
- Source citations appear below every answer
