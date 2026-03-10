from ai_pnp.core.models.game_state import GameState
from ai_pnp.core.models.quest import Quest

class ContentLoader:
    def create_initial_state(self) -> GameState:
        state = GameState()
        state.active_quests.append(
            Quest(
                quest_id="missing_courier",
                title="Der verschwundene Kurier",
                summary="Ein Kurier ist auf dem letzten Abschnitt der Heerstraße nicht angekommen."
            )
        )
        return state
