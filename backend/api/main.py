import sys
import os
import random
from datetime import datetime

backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_path)

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from models.database import init_db, get_db, save_conversation, get_conversation_history

app = FastAPI(
    title="E-Commerce AI Agent System",
    description="Autonomous AI agents for e-commerce operations",
    version="3.0.0"
)

class CustomerQuery(BaseModel):
    query: str
    customer_id: Optional[int] = None

class InventoryRequest(BaseModel):
    task_type: str
    product_id: int

class RecommendationRequest(BaseModel):
    customer_id: int
    browsing_history: Optional[list] = []

class FraudRequest(BaseModel):
    task_type: str
    transaction_id: int
    amount: Optional[float] = 0

class MarketingRequest(BaseModel):
    task_type: str
    product_category: Optional[str] = "electronics"
    customer_name: Optional[str] = "Valued Customer"

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized!")

@app.get("/")
async def root():
    return {
        "message": "E-Commerce AI Agent System",
        "agents": ["customer_service", "inventory", "pricing", "recommendation", "fraud_detection", "marketing"],
        "features": ["database_persistence", "conversation_history", "fraud_protection", "marketing_automation"]
    }

@app.get("/health")
async def health_check():
    return {
        "customer_service": "active",
        "inventory_pricing": "active",
        "recommendation": "active",
        "fraud_detection": "active",
        "marketing": "active",
        "orchestrator": "active"
    }

@app.post("/api/agent/customer-service")
async def customer_service(query: CustomerQuery, db: Session = Depends(get_db)):
    try:
        customer_query = query.query.lower()
        
        if "order" in customer_query or "where" in customer_query:
            response_data = {
                "intent": "order_status",
                "response": f"Hello! I've checked your order. Your order #12345 is currently being processed and will be shipped within 24 hours. You can track it using tracking number TRK789456.",
                "action": "check_order",
                "confidence": 0.95
            }
        elif "return" in customer_query or "refund" in customer_query:
            response_data = {
                "intent": "return_request",
                "response": "I can help you with your return. Since your order was placed within 30 days, you're eligible for a full refund. I'll initiate the return process now.",
                "action": "process_return",
                "confidence": 0.92
            }
        else:
            response_data = {
                "intent": "general",
                "response": "Thank you for contacting us! I'm here to help with orders, returns, product questions, or any other concerns. How can I assist you today?",
                "action": "none",
                "confidence": 0.85
            }
        
        save_conversation(db, query.customer_id or 1, "customer_service", query.query, response_data["response"])
        
        return {
            "agent_type": "customer_service",
            "success": True,
            "data": response_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/inventory")
async def inventory_management(request: InventoryRequest, db: Session = Depends(get_db)):
    try:
        task_type = request.task_type
        product_id = request.product_id
        
        if task_type == "check_stock":
            stock_status = random.choice(["adequate", "low", "critical"])
            result = {
                "agent_type": "inventory",
                "task": "stock_check",
                "product_id": product_id,
                "analysis": {
                    "stock_status": stock_status,
                    "current_stock": random.randint(5, 500),
                    "recommended_action": "reorder" if stock_status == "low" else "none",
                    "quantity_to_order": 100 if stock_status == "low" else 0,
                    "supplier_lead_time": "3-5 days",
                    "note": "Seasonal demand expected to increase next month"
                }
            }
        elif task_type == "update_price":
            result = {
                "agent_type": "pricing",
                "task": "price_optimization",
                "product_id": product_id,
                "recommendation": {
                    "current_price": 99.99,
                    "recommended_price": 89.99,
                    "strategy": "competitive",
                    "expected_impact": "increase_sales",
                    "competitor_analysis": "Competitors pricing similar products at - range",
                    "confidence": 0.87
                }
            }
        else:
            result = {
                "agent_type": "inventory",
                "task": "demand_forecast",
                "product_id": product_id,
                "forecast": {
                    "next_30_days": random.randint(100, 500),
                    "confidence": 0.85,
                    "trend": "increasing"
                }
            }
        
        save_conversation(db, 1, "inventory", f"Task: {task_type}, Product: {product_id}", str(result))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/recommendations")
async def get_recommendations(request: RecommendationRequest, db: Session = Depends(get_db)):
    try:
        products = [
            {"id": 1, "name": "Wireless Noise-Cancelling Headphones", "price": 99.99, "confidence": 0.95, "reasoning": "Based on your interest in electronics"},
            {"id": 2, "name": "Smart Fitness Watch Pro", "price": 249.99, "confidence": 0.88, "reasoning": "Complements your active lifestyle"},
            {"id": 3, "name": "Premium Yoga Mat", "price": 29.99, "confidence": 0.82, "reasoning": "Frequently bought together with fitness watches"},
            {"id": 4, "name": "Bluetooth Speaker Mini", "price": 45.99, "confidence": 0.79, "reasoning": "Portable audio solution"},
            {"id": 5, "name": "Laptop Stand Adjustable", "price": 35.99, "confidence": 0.76, "reasoning": "Popular among similar customers"}
        ]
        
        result = {
            "agent_type": "recommendation",
            "customer_id": request.customer_id,
            "browsing_history": request.browsing_history,
            "recommendations": {
                "top_picks": products[:3],
                "personalized_bundle": {
                    "items": [products[0], products[1]],
                    "bundle_price": 299.99,
                    "savings": 50.00
                },
                "strategy": "personalized_collaborative_filtering"
            }
        }
        
        save_conversation(db, request.customer_id, "recommendation", str(request.browsing_history), str(result))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/fraud-detection")
async def fraud_detection(request: FraudRequest, db: Session = Depends(get_db)):
    try:
        task_type = request.task_type
        transaction_id = request.transaction_id
        
        if task_type == "analyze_transaction":
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
            
            result = {
                "agent_type": "fraud_detection",
                "task": "transaction_analysis",
                "transaction_id": transaction_id,
                "analysis": {
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                    "status": status,
                    "recommended_action": action,
                    "flags": ["Unusual location" if risk_score > 50 else None, "High amount" if request.amount > 1000 else None],
                    "confidence": round(random.uniform(0.75, 0.98), 2)
                }
            }
        else:
            result = {
                "agent_type": "fraud_detection",
                "task": "risk_assessment",
                "transaction_id": transaction_id,
                "risk_score": random.randint(20, 80),
                "recommendation": "monitor"
            }
        
        save_conversation(db, 1, "fraud_detection", f"Task: {task_type}, TX: {transaction_id}", str(result))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/marketing")
async def marketing(request: MarketingRequest, db: Session = Depends(get_db)):
    try:
        task_type = request.task_type
        
        if task_type == "generate_campaign":
            campaigns = {
                "electronics": {"name": "Tech Revolution Sale", "tagline": "Upgrade Your Life", "channels": ["email", "social_media"], "expected_roi": 2.5},
                "fashion": {"name": "Summer Style Festival", "tagline": "Discover Your Look", "channels": ["instagram", "influencer"], "expected_roi": 3.2}
            }
            campaign = campaigns.get(request.product_category, campaigns["electronics"])
            
            result = {
                "agent_type": "marketing",
                "task": "campaign_generation",
                "campaign": {
                    "name": campaign["name"],
                    "tagline": campaign["tagline"],
                    "channels": campaign["channels"],
                    "expected_roi": campaign["expected_roi"],
                    "confidence": round(random.uniform(0.85, 0.95), 2)
                }
            }
        elif task_type == "customer_segmentation":
            result = {
                "agent_type": "marketing",
                "task": "customer_segmentation",
                "segments": [
                    {"name": "VIP Customers", "size_percent": 15, "strategy": "Exclusive offers"},
                    {"name": "Bargain Hunters", "size_percent": 35, "strategy": "Discount alerts"},
                    {"name": "New Customers", "size_percent": 25, "strategy": "Welcome series"}
                ],
                "confidence": round(random.uniform(0.88, 0.96), 2)
            }
        else:
            result = {
                "agent_type": "marketing",
                "task": task_type,
                "message": f"Marketing task {task_type} completed successfully",
                "confidence": round(random.uniform(0.80, 0.95), 2)
            }
        
        save_conversation(db, 1, "marketing", f"Task: {task_type}", str(result))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{customer_id}")
async def get_conversations(customer_id: int, limit: int = 10, db: Session = Depends(get_db)):
    try:
        history = get_conversation_history(db, customer_id, limit)
        return [
            {
                "id": conv.id,
                "agent_type": conv.agent_type,
                "message": conv.message,
                "response": conv.response,
                "timestamp": conv.timestamp.isoformat() if conv.timestamp else None
            }
            for conv in history
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException
from backend.agents.shipping_agent import ShippingAgent
from backend.agents.analytics_agent import AnalyticsAgent

router = APIRouter()

# Add these endpoints if they don't exist:

@router.post("/api/agent/shipping")
async def shipping_endpoint(request: dict):
    try:
        agent = ShippingAgent()
        result = await agent.process(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/agent/analytics")
async def analytics_endpoint(request: dict):
    try:
        agent = AnalyticsAgent()
        result = await agent.process(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Shipping Agent Endpoint
@app.post("/api/agent/shipping")
async def shipping_endpoint(request: dict):
    from backend.agents.shipping_agent import ShippingAgent
    agent = ShippingAgent()
    return await agent.process(request)

# Analytics Agent Endpoint  
@app.post("/api/agent/analytics")
async def analytics_endpoint(request: dict):
    from backend.agents.analytics_agent import AnalyticsAgent
    agent = AnalyticsAgent()
    return await agent.process(request)