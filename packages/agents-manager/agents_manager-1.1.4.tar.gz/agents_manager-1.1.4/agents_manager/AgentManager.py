import json
from typing import List, Optional, Any

from agents_manager.Agent import Agent


class AgentManager:
    def __init__(self) -> None:
        """
        Initialize the AgentManager with an empty list of agents.
        """
        self.agents: List[Agent] = []

    def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to the manager's list.

        Args:
            agent (Agent): The agent instance to add.
        """
        if not isinstance(agent, Agent):
            raise ValueError("Only Agent instances can be added")
        self.agents.append(agent)
        agent.set_messages([{"role": "assistant", "content": agent.instruction}])
        agent.set_tools(agent.tools)

    def get_agent(self, name: str) -> Optional[Agent]:
        """
        Retrieve an agent by name.

        Args:
            name (str): The name of the agent to find.

        Returns:
            Optional[Agent]: The agent if found, else None.
        """
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None

    def run_agent(self, name: str, user_input: Optional[Any] = None) -> Any:
        """
        Run a specific agent's non-streaming response.

        Args:
            name (str): The name of the agent to run.
            user_input (str, optional): Additional user input to append to messages.

        Returns:
            Any: The agent's response.
        """
        agent = self.get_agent(name)
        if agent is None:
            raise ValueError(f"No agent found with name: {name}")

        if user_input:
            current_messages = agent.get_messages() or []
            if isinstance(user_input, str):
                user_input = {"role": "user", "content": user_input}
                current_messages.append(user_input)
            if isinstance(user_input, dict):
                user_input = [user_input]
                current_messages.extend(user_input)
            if isinstance(user_input, list):
                current_messages.extend(user_input)
            agent.set_messages(current_messages)

        response = agent.get_response()

        if not response['tool_calls']:
            return response["content"]

        tool_calls = response['tool_calls']
        current_messages = agent.get_messages()
        current_messages.append(agent.get_model().get_assistant_message(response))
        tool_responses = []
        for tool_call in tool_calls:
            output = agent.get_model().get_keys_in_tool_output(tool_call)
            id = output["id"]
            function_name = output["name"]
            if isinstance(output["arguments"], str):
                arguments = json.loads(output["arguments"])
            else:
                arguments = output["arguments"]

            tools = agent.tools
            for tool in tools:
                if tool.__name__ == function_name:
                    tool_result = tool(**arguments)
                    if isinstance(tool_result, Agent):
                        self.add_agent(tool_result)
                        nested_response = self.run_agent(tool_result.name,
                                                         user_input
                                                         )
                        tool_response_content = (
                            nested_response.content
                            if hasattr(nested_response, "content")
                            else str(nested_response)
                        )
                        return tool_response_content
                    else:
                        tool_responses.append({
                            "id": id,
                            "tool_result": str(tool_result),
                        })

        tool_response = agent.get_model().get_tool_message(tool_responses)
        if isinstance(tool_response, dict):
            current_messages.append(tool_response)
        if isinstance(tool_response, list):
            for response in tool_response:
                current_messages.append(response)

        agent.set_messages(current_messages)
        response = agent.get_response()
        return response["content"]
