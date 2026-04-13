class ExecutorAgent:
    def __init__(self, tools, memory):
        self.tools = tools
        self.memory = memory

    def execute(self, action, input_data):

        tool = self.tools.get(action)

        if not tool:
            return None

        result = tool(input_data)

        return result