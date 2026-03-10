class MemoryService:
    def get_recent_context(self, state) -> list[dict]:
        return state.turn_log

    def record_turn(self, state, action: str, narration: str) -> None:
        state.turn_log.append({"action": action, "result": narration})
        if len(state.turn_log) > 20:
            state.turn_log[:] = state.turn_log[-20:]
