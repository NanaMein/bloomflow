from typing import Mapping
from crewai import Agent


class AgentConfigurationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class AgentsService:
    required_keys = {"role", "goal", "backstory"}
    def __init__(self):
        self._agents = []


    def add_agent_config(self, data: Mapping[str, object]) -> Agent:
        
        missing_keys = self.required_keys - data.keys()

        if missing_keys:
            raise AgentConfigurationError(f"Missing required keys: {missing_keys}")

        invalid_keys: set[str] = set()

        for key in self.required_keys:
            value = data[key]
            if not isinstance(value, str) or not value.strip():
                invalid_keys.add(key)


        if invalid_keys:
            raise AgentConfigurationError(
                f"Values must be non-empty strings: {', '.join(sorted(invalid_keys))}"
            )

        agent = Agent(
            role=data["role"],
            goal=data["goal"],
            backstory=data["backstory"],
        )

        self._agents.append(agent)
        return agent