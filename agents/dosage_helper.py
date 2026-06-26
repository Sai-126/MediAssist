import re

def generate_dosage_schedule(prescription_text: str) -> str:
    """
    Generates a simple morning/afternoon/night schedule
    based on common dosage keywords found in prescription text.
    """
    text = prescription_text.lower()
    schedule = []

    if "once daily" in text or "once a day" in text:
        schedule.append("Morning: 1 dose")
    elif "twice daily" in text or "two times" in text:
        schedule.append("Morning: 1 dose")
        schedule.append("Night: 1 dose")
    elif "thrice daily" in text or "three times" in text:
        schedule.append("Morning: 1 dose")
        schedule.append("Afternoon: 1 dose")
        schedule.append("Night: 1 dose")
    elif "four times" in text:
        schedule.append("Morning: 1 dose")
        schedule.append("Afternoon: 1 dose")
        schedule.append("Evening: 1 dose")
        schedule.append("Night: 1 dose")

    if not schedule:
        return "Could not determine a clear schedule. Please follow your doctor's exact instructions."

    food_note = ""
    if "after food" in text:
        food_note = " (after eating food)"
    elif "before food" in text:
        food_note = " (before eating food, empty stomach)"

    result = "Suggested daily schedule" + food_note + ":\n"
    for item in schedule:
        result += f"- {item}\n"

    return result.strip()