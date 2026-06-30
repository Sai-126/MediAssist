import sys
sys.path.append(".")
from agents.orchestrator import Orchestrator

print("=" * 50)
print("MediAssist — Full Integration Test")
print("=" * 50)

orch = Orchestrator()

print("\n--- Testing Prescription Flow ---")
r1 = orch.route("prescription", query="Tab Paracetamol 500mg twice daily after food", language="english")
assert len(r1) > 20, "Prescription response too short"
print("PASS - Prescription flow working")
print(r1[:200])

print("\n--- Testing Symptom Flow ---")
r2 = orch.route("symptoms", query="fever and headache for 2 days", language="english")
assert len(r2) > 20, "Symptom response too short"
print("PASS - Symptom flow working")
print(r2[:200])

print("\n--- Testing Scheme Flow ---")
r3 = orch.route("scheme", profile={
    "district": "Warangal",
    "income": 50000,
    "age": 40,
    "family_size": 4,
    "category": "BC"
}, language="english")
assert len(r3) > 20, "Scheme response too short"
print("PASS - Scheme flow working")
print(r3[:200])

print("\n--- Testing Telugu Language ---")
r4 = orch.route("symptoms", query="fever and headache", language="telugu")
assert len(r4) > 20, "Telugu response too short"
print("PASS - Telugu flow working")

print("\n" + "=" * 50)
print("ALL INTEGRATION TESTS PASSED!")
print("=" * 50)