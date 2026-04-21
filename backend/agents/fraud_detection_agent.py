from backend.agents.base_agent import BaseEcommerceAgent
from typing import Dict, Any
import random

class FraudDetectionAgent(BaseEcommerceAgent):
    def __init__(self):
        super().__init__("Fraud Detection Specialist")
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        task_type = input_data.get("task_type", "analyze_transaction")
        transaction_id = input_data.get("transaction_id", 1)
        
        try:
            if task_type == "analyze_transaction":
                return await self.analyze_transaction(transaction_id, input_data)
            elif task_type == "detect_anomaly":
                return await self.detect_anomaly(input_data)
            elif task_type == "risk_assessment":
                return await self.risk_assessment(input_data)
            
            return {"error": "Unknown task type", "agent_type": "fraud_detection"}
            
        except Exception as e:
            return {
                "agent_type": "fraud_detection",
                "task": task_type,
                "error": str(e),
                "transaction_id": transaction_id
            }
    
    async def analyze_transaction(self, transaction_id: int, data: Dict) -> Dict[str, Any]:
        risk_score = random.randint(0, 100)
        
        if risk_score < 30:
            risk_level = "low"
            status = "approved"
            action = "process"
        elif risk_score < 70:
            risk_level = "medium"
            status = "review"
            action = "manual_review"
        else:
            risk_level = "high"
            status = "declined"
            action = "block"
        
        return {
            "agent_type": "fraud_detection",
            "task": "transaction_analysis",
            "transaction_id": transaction_id,
            "analysis": {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "status": status,
                "recommended_action": action,
                "flags": [
                    "Unusual location" if risk_score > 50 else None,
                    "High amount" if data.get("amount", 0) > 1000 else None,
                    "New device" if random.random() > 0.7 else None
                ],
                "confidence": round(random.uniform(0.75, 0.98), 2),
                "notes": f"Transaction analyzed with {risk_level} risk profile"
            }
        }
    
    async def detect_anomaly(self, data: Dict) -> Dict[str, Any]:
        anomalies = []
        
        if data.get("amount", 0) > 5000:
            anomalies.append("High value transaction")
        if data.get("velocity", 0) > 5:
            anomalies.append("Multiple transactions in short time")
        if data.get("location") != data.get("usual_location"):
            anomalies.append("Unusual location")
        
        return {
            "agent_type": "fraud_detection",
            "task": "anomaly_detection",
            "anomalies_detected": len(anomalies),
            "anomaly_list": anomalies if anomalies else ["No anomalies detected"],
            "requires_review": len(anomalies) > 0,
            "confidence": round(random.uniform(0.80, 0.95), 2)
        }
    
    async def risk_assessment(self, data: Dict) -> Dict[str, Any]:
        customer_id = data.get("customer_id", 1)
        
        risk_factors = {
            "account_age": random.choice(["new", "established", "veteran"]),
            "transaction_history": random.choice(["clean", "minor_issues", "flagged"]),
            "device_trust": random.choice(["trusted", "new", "suspicious"]),
            "location_consistency": random.choice(["consistent", "variable", "unusual"])
        }
        
        risk_score = 0
        if risk_factors["account_age"] == "new":
            risk_score += 20
        if risk_factors["transaction_history"] == "flagged":
            risk_score += 40
        if risk_factors["device_trust"] == "suspicious":
            risk_score += 30
        if risk_factors["location_consistency"] == "unusual":
            risk_score += 25
        
        return {
            "agent_type": "fraud_detection",
            "task": "risk_assessment",
            "customer_id": customer_id,
            "risk_score": min(risk_score, 100),
            "risk_factors": risk_factors,
            "recommendation": "monitor" if risk_score < 50 else "review" if risk_score < 80 else "restrict",
            "confidence": round(random.uniform(0.82, 0.96), 2)
        }
