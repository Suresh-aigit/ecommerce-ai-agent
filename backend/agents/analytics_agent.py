from backend.agents.base_agent import BaseEcommerceAgent
from typing import Dict, Any, List
import random
from datetime import datetime, timedelta

class AnalyticsAgent(BaseEcommerceAgent):
    def __init__(self):
        super().__init__("Business Analytics Specialist")
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        task_type = input_data.get("task_type", "sales_report")
        
        try:
            if task_type == "sales_report":
                return await self.generate_sales_report(input_data)
            elif task_type == "customer_analytics":
                return await self.customer_analytics(input_data)
            elif task_type == "product_performance":
                return await self.product_performance(input_data)
            elif task_type == "predictive_forecast":
                return await self.predictive_forecast(input_data)
            elif task_type == "churn_analysis":
                return await self.churn_analysis(input_data)
            
            return {"error": "Unknown task type", "agent_type": "analytics"}
            
        except Exception as e:
            return {
                "agent_type": "analytics",
                "task": task_type,
                "error": str(e)
            }
    
    async def generate_sales_report(self, data: Dict) -> Dict[str, Any]:
        period = data.get("period", "last_30_days")
        
        # Try real OpenAI
        if not self.mock_mode:
            system_prompt = "You are a business analytics AI. Provide detailed sales insights."
            user_prompt = f"Generate sales report for {period} with key metrics and trends"
            ai_response = await self.get_llm_response(system_prompt, user_prompt)
            
            if ai_response:
                return {
                    "agent_type": "analytics",
                    "task": "sales_report",
                    "period": period,
                    "ai_analysis": ai_response,
                    "source": "openai"
                }
        
        # Mock data
        return {
            "agent_type": "analytics",
            "task": "sales_report",
            "period": period,
            "summary": {
                "total_revenue": round(random.uniform(50000, 150000), 2),
                "total_orders": random.randint(500, 2000),
                "average_order_value": round(random.uniform(75, 150), 2),
                "conversion_rate": round(random.uniform(2.5, 5.5), 2),
                "growth_vs_last_period": f"{random.randint(-10, 25)}%"
            },
            "top_products": [
                {"name": "Wireless Headphones", "revenue": 15420, "units_sold": 154},
                {"name": "Smart Watch", "revenue": 22350, "units_sold": 89},
                {"name": "Yoga Mat", "revenue": 8970, "units_sold": 299}
            ],
            "insights": [
                "Revenue increased 15% compared to last month",
                "Mobile traffic conversion improved by 2.3%",
                "Weekend sales show 40% higher average order value",
                "Returning customers account for 65% of revenue"
            ],
            "recommendations": [
                "Increase inventory for top 3 products",
                "Launch weekend flash sale campaign",
                "Optimize mobile checkout flow"
            ],
            "source": "mock"
        }
    
    async def customer_analytics(self, data: Dict) -> Dict[str, Any]:
        segment = data.get("segment", "all_customers")
        
        return {
            "agent_type": "analytics",
            "task": "customer_analytics",
            "segment": segment,
            "metrics": {
                "total_customers": random.randint(1000, 10000),
                "active_customers": random.randint(500, 5000),
                "new_customers": random.randint(50, 500),
                "churned_customers": random.randint(20, 200),
                "customer_lifetime_value": round(random.uniform(150, 800), 2),
                "avg_purchase_frequency": round(random.uniform(2.5, 8.5), 1)
            },
            "behavioral_data": {
                "peak_shopping_hours": "6:00 PM - 9:00 PM",
                "preferred_payment_methods": ["Credit Card (45%)", "PayPal (30%)", "Apple Pay (15%)"],
                "device_breakdown": {"mobile": 65, "desktop": 30, "tablet": 5},
                "avg_session_duration": f"{random.randint(3, 12)} minutes"
            },
            "cohort_analysis": {
                "jan_2024": {"retention": "85%", "revenue": 45000},
                "feb_2024": {"retention": "78%", "revenue": 52000},
                "mar_2024": {"retention": "82%", "revenue": 61000}
            }
        }
    
    async def product_performance(self, data: Dict) -> Dict[str, Any]:
        category = data.get("category", "all")
        
        products = [
            {
                "product_id": 1,
                "name": "Wireless Headphones Pro",
                "category": "Electronics",
                "revenue": 45200,
                "units_sold": 452,
                "return_rate": "2.1%",
                "rating": 4.7,
                "stock_turnover": 12,
                "trend": "upward"
            },
            {
                "product_id": 2,
                "name": "Smart Fitness Watch",
                "category": "Wearables",
                "revenue": 38900,
                "units_sold": 156,
                "return_rate": "3.5%",
                "rating": 4.5,
                "stock_turnover": 8,
                "trend": "stable"
            },
            {
                "product_id": 3,
                "name": "Premium Yoga Mat",
                "category": "Fitness",
                "revenue": 12400,
                "units_sold": 413,
                "return_rate": "1.2%",
                "rating": 4.9,
                "stock_turnover": 15,
                "trend": "upward"
            }
        ]
        
        return {
            "agent_type": "analytics",
            "task": "product_performance",
            "category": category,
            "products": products,
            "category_summary": {
                "total_revenue": sum(p["revenue"] for p in products),
                "total_units": sum(p["units_sold"] for p in products),
                "avg_rating": round(sum(p["rating"] for p in products) / len(products), 2),
                "top_performer": "Wireless Headphones Pro"
            },
            "recommendations": [
                "Increase marketing budget for Smart Fitness Watch",
                "Bundle Yoga Mat with other fitness products",
                "Consider premium pricing for high-rated items"
            ]
        }
    
    async def predictive_forecast(self, data: Dict) -> Dict[str, Any]:
        forecast_type = data.get("forecast_type", "revenue")
        horizon_days = data.get("horizon_days", 30)
        
        base_value = random.uniform(40000, 80000)
        growth_rate = random.uniform(0.02, 0.15)
        
        forecast = []
        for i in range(5):  # 5 periods
            period_value = base_value * ((1 + growth_rate) ** i)
            forecast.append({
                "period": f"Week {i+1}",
                "predicted_value": round(period_value, 2),
                "confidence_interval": {
                    "low": round(period_value * 0.85, 2),
                    "high": round(period_value * 1.15, 2)
                }
            })
        
        return {
            "agent_type": "analytics",
            "task": "predictive_forecast",
            "forecast_type": forecast_type,
            "horizon_days": horizon_days,
            "forecast_data": forecast,
            "model_accuracy": f"{random.randint(85, 95)}%",
            "key_drivers": [
                "Seasonal demand patterns",
                "Marketing campaign effectiveness",
                "Economic indicators",
                "Competitor pricing changes"
            ],
            "risk_factors": [
                "Supply chain disruptions",
                "Economic downturn",
                "New competitor entry"
            ]
        }
    
    async def churn_analysis(self, data: Dict) -> Dict[str, Any]:
        return {
            "agent_type": "analytics",
            "task": "churn_analysis",
            "churn_rate": f"{random.uniform(5, 15):.1f}%",
            "at_risk_customers": random.randint(100, 500),
            "churn_reasons": [
                {"reason": "Price sensitivity", "percentage": 35},
                {"reason": "Better competitor offers", "percentage": 28},
                {"reason": "Poor customer service", "percentage": 20},
                {"reason": "Product quality issues", "percentage": 12},
                {"reason": "Other", "percentage": 5}
            ],
            "early_warning_signs": [
                "Decreased purchase frequency",
                "Lower engagement with emails",
                "Increased support tickets",
                "Cart abandonment increase"
            ],
            "retention_strategies": [
                "Personalized win-back campaigns",
                "Loyalty program incentives",
                "Proactive customer service outreach",
                "Exclusive discount offers"
            ]
        }