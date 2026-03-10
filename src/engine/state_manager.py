class StateManager:
    def __init__(self):
        self.state = {
            "location": "tavern",
            "player": {
                "name": "Hero",
                "hp": 10,
                "inventory": []
            }
        }

    def get_state(self):
        return self.state
