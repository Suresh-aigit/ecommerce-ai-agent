from typing import Dict, Any

# MOCK MODE - No OpenAI API calls needed
USE_MOCK = True

class BaseEcommerceAgent:
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.mock_mode = USE_MOCK
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement process method")
