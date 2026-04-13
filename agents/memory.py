class AgentMemory:
    def __init__(self):
        self.state = {
            "data": [],
            "filtered": [],
            "summaries": [],
            "final": []
        }

    def update(self, key, value):
        self.state[key] = value

    def get(self, key):
        return self.state.get(key)