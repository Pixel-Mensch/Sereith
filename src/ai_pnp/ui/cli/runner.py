from dataclasses import dataclass


@dataclass
class CliResponse:
    message: str
    should_quit: bool = False


def handle_cli_input(engine, raw_input: str) -> CliResponse:
    action = raw_input.strip()
    if not action:
        return CliResponse("Leere Eingabe ignoriert.")

    lowered = action.lower()
    if lowered == "quit":
        return CliResponse("Spiel beendet.", should_quit=True)
    if lowered.startswith("save"):
        parts = action.split(maxsplit=1)
        result = engine.save_game(parts[1].strip() if len(parts) > 1 else None)
        return CliResponse(result["message"])
    if lowered.startswith("load"):
        parts = action.split(maxsplit=1)
        result = engine.load_game(parts[1].strip() if len(parts) > 1 else None)
        if not result["ok"]:
            return CliResponse(result["message"])
        return CliResponse(f"{result['message']}\n\n{engine.describe_current_scene()}")
    if lowered == "state":
        return CliResponse(engine.render_state_summary())

    result = engine.process_action(action)
    if not result["ok"]:
        return CliResponse(result["message"])
    message = result["narration"]
    if result["system_note"]:
        message = f"{message}\n\n[System: {result['system_note']}]"
    return CliResponse(message)


def run(engine=None, input_func=input, output_func=print) -> None:
    if engine is None:
        from ai_pnp.core.application import Application

        engine = Application().engine

    output_func("AI-PnP gestartet")
    output_func("Befehle: save [name], load [name], state, quit\n")
    output_func(engine.describe_current_scene())
    while True:
        response = handle_cli_input(engine, input_func("\n> "))
        output_func(f"\n{response.message}")
        if response.should_quit:
            break
