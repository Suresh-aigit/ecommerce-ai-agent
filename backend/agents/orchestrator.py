from backend.agents.customer_service_agent import CustomerServiceAgent
from backend.agents.inventory_agent import InventoryPricingAgent
from backend.agents.recommendation_agent import RecommendationAgent
from backend.agents.fraud_detection_agent import FraudDetectionAgent
from backend.agents.marketing_agent import MarketingAgent
from typing import Dict, Any

class AgentOrchestrator:
    def __init__(self):
        self.customer_service = CustomerServiceAgent()
        self.inventory = InventoryPricingAgent()
        self.recommendation = RecommendationAgent()
        self.fraud_detection = FraudDetectionAgent()
        self.marketing = MarketingAgent()
        
        self.agent_map = {
            "customer_service": self.customer_service,
            "inventory": self.inventory,
            "pricing": self.inventory,
            "recommendation": self.recommendation,
            "fraud_detection": self.fraud_detection,
            "marketing": self.marketing
        }
    
    async def route_request(self, request_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if request_type in self.agent_map:
            agent = self.agent_map[request_type]
            return await agent.process(data)
        
        if request_type == "complete_purchase_assistance":
            return await self.handle_purchase_workflow(data)
        
        return {"error": f"No agent found for type: {request_type}"}
    
    async def handle_purchase_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        customer_id = data.get("customer_id")
        
        rec_result = await self.recommendation.process({
            "customer_id": customer_id,
            "browsing_history": data.get("browsing_history", [])
        })
        
        cs_result = await self.customer_service.process({
            "query": "I am looking for product recommendations",
            "customer_id": customer_id
        })
        
        return {
            "workflow": "purchase_assistance",
            "recommendations": rec_result,
            "customer_context": cs_result,
            "next_steps": ["show_products", "answer_questions", "process_order"]
        }
    
    async def get_agent_status(self) -> Dict[str, Any]:
        return {
            "customer_service": "active",
            "inventory_pricing": "active", 
            "recommendation": "active",
            "fraud_detection": "active",
            "marketing": "active",
            "orchestrator": "active"
        }
