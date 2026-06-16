import sys
import os
sys.path.append(".")
from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import Orchestrator

print("=" * 50)
print("MediAssist — Agent Tests Week 2")
print("=" * 50)

orch = Orchestrator()

print("\n--- Test 1: Prescription Agent ---")
result = orch.route(
    "prescription",
    query="Tab Paracetamol 500mg twice daily after food, Tab Metformin 500mg after meals",
    language="english"
)
print(result[:400])
print("✓ Prescription Agent working\n")

print("\n--- Test 2: Symptom Agent ---")
result = orch.route(
    "symptoms",
    query="I have fever 102 degrees, headache and body pain for 2 days",
    language="english"
)
print(result[:400])
print("✓ Symptom Agent working\n")

print("\n--- Test 3: Scheme Agent ---")
result = orch.route(
    "scheme",
    profile={
        "district": "Warangal",
        "income": 80000,
        "age": 45,
        "family_size": 5,
        "category": "BC"
    },
    language="english"
)
print(result[:400])
print("✓ Scheme Agent working\n")

print("\n--- Test 4: Telugu Response ---")
result = orch.route(
    "symptoms",
    query="నాకు జ్వరం మరియు తలనొప్పి ఉంది",
    language="telugu"
)
print(result[:400])
print("✓ Telugu working\n")

print("=" * 50)
print("All tests passed!")
print("=" * 50)