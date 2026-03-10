def build_prompt(state, action):
    location = state.get("location", "unknown")
    return f"Location: {location}\nPlayer action: {action}\nNarrate what happens."
