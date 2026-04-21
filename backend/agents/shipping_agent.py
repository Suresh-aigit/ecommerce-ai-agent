from backend.agents.base_agent import BaseEcommerceAgent
from typing import Dict, Any
import random
from datetime import datetime, timedelta

class ShippingAgent(BaseEcommerceAgent):
    def __init__(self):
        super().__init__("Shipping & Logistics Coordinator")
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        task_type = input_data.get("task_type", "track_shipment")
        
        try:
            if task_type == "track_shipment":
                return await self.track_shipment(input_data)
            elif task_type == "estimate_delivery":
                return await self.estimate_delivery(input_data)
            elif task_type == "optimize_route":
                return await self.optimize_route(input_data)
            elif task_type == "shipping_options":
                return await self.get_shipping_options(input_data)
            
            return {"error": "Unknown task type", "agent_type": "shipping"}
            
        except Exception as e:
            return {
                "agent_type": "shipping",
                "task": task_type,
                "error": str(e)
            }
    
    async def track_shipment(self, data: Dict) -> Dict[str, Any]:
        tracking_number = data.get("tracking_number", "TRK123456789")
        order_id = data.get("order_id", 1)
        
        # Try real OpenAI first
        if not self.mock_mode:
            system_prompt = "You are a shipping logistics AI. Provide realistic tracking updates."
            user_prompt = f"Generate tracking status for order {order_id}, tracking number {tracking_number}"
            ai_response = await self.get_llm_response(system_prompt, user_prompt)
            
            if ai_response:
                return {
                    "agent_type": "shipping",
                    "task": "track_shipment",
                    "tracking_number": tracking_number,
                    "order_id": order_id,
                    "ai_generated_response": ai_response,
                    "source": "openai"
                }
        
        # Mock fallback
        statuses = [
            {"status": "picked_up", "location": "Warehouse", "progress": 10},
            {"status": "in_transit", "location": "Distribution Center", "progress": 40},
            {"status": "out_for_delivery", "location": "Local Facility", "progress": 80},
            {"status": "delivered", "location": "Customer Address", "progress": 100}
        ]
        
        current_status = random.choice(statuses)
        estimated_delivery = datetime.now() + timedelta(days=random.randint(1, 5))
        
        return {
            "agent_type": "shipping",
            "task": "track_shipment",
            "tracking_number": tracking_number,
            "order_id": order_id,
            "current_status": current_status["status"],
            "current_location": current_status["location"],
            "progress_percent": current_status["progress"],
            "estimated_delivery": estimated_delivery.strftime("%Y-%m-%d"),
            "shipping_carrier": random.choice(["FedEx", "UPS", "DHL", "USPS"]),
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "history": [
                {"time": "2024-01-15 09:00", "event": "Order placed"},
                {"time": "2024-01-15 14:30", "event": "Package picked up"},
                {"time": "2024-01-16 08:00", "event": "Arrived at distribution center"}
            ],
            "source": "mock"
        }
    
    async def estimate_delivery(self, data: Dict) -> Dict[str, Any]:
        origin = data.get("origin", "New York, NY")
        destination = data.get("destination", "Los Angeles, CA")
        shipping_method = data.get("shipping_method", "standard")
        
        days_map = {
            "standard": (3, 7),
            "express": (1, 3),
            "overnight": (1, 1),
            "international": (7, 21)
        }
        
        min_days, max_days = days_map.get(shipping_method, (3, 7))
        estimated_days = random.randint(min_days, max_days)
        
        delivery_date = datetime.now() + timedelta(days=estimated_days)
        
        return {
            "agent_type": "shipping",
            "task": "estimate_delivery",
            "origin": origin,
            "destination": destination,
            "shipping_method": shipping_method,
            "estimated_days": estimated_days,
            "estimated_delivery_date": delivery_date.strftime("%Y-%m-%d"),
            "cost_estimate": round(random.uniform(5.99, 49.99), 2),
            "confidence": round(random.uniform(0.85, 0.98), 2)
        }
    
    async def optimize_route(self, data: Dict) -> Dict[str, Any]:
        warehouses = data.get("warehouses", ["Warehouse A", "Warehouse B"])
        destination = data.get("destination", "Customer Location")
        
        # Simple route optimization logic
        optimal_warehouse = random.choice(warehouses)
        
        return {
            "agent_type": "shipping",
            "task": "route_optimization",
            "destination": destination,
            "optimal_warehouse": optimal_warehouse,
            "estimated_savings": f"{random.randint(10, 30)}%",
            "route_distance": f"{random.randint(50, 500)} miles",
            "estimated_transit_time": f"{random.randint(1, 5)} days",
            "carbon_footprint": f"{random.randint(5, 25)} kg CO2",
            "recommendation": f"Ship from {optimal_warehouse} for fastest delivery"
        }
    
    async def get_shipping_options(self, data: Dict) -> Dict[str, Any]:
        weight = data.get("weight_kg", 1.0)
        dimensions = data.get("dimensions", "10x10x10")
        
        options = [
            {
                "method": "Standard Ground",
                "cost": round(5.99 + (weight * 2), 2),
                "delivery_time": "3-5 business days",
                "tracking": True,
                "insurance_included": False
            },
            {
                "method": "Express Shipping",
                "cost": round(15.99 + (weight * 3), 2),
                "delivery_time": "1-2 business days",
                "tracking": True,
                "insurance_included": True
            },
            {
                "method": "Overnight",
                "cost": round(29.99 + (weight * 5), 2),
                "delivery_time": "Next business day",
                "tracking": True,
                "insurance_included": True
            }
        ]
        
        return {
            "agent_type": "shipping",
            "task": "shipping_options",
            "package_weight_kg": weight,
            "package_dimensions": dimensions,
            "options": options,
            "recommended_option": "Express Shipping",
            "savings_tip": "Choose Standard Ground to save $10"
        }