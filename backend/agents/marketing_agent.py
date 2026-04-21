from backend.agents.base_agent import BaseEcommerceAgent
from typing import Dict, Any, List
import random

class MarketingAgent(BaseEcommerceAgent):
    def __init__(self):
        super().__init__("Marketing & Campaign Specialist")

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        task_type = input_data.get("task_type", "generate_campaign")

        try:
            if task_type == "generate_campaign":
                return await self.generate_campaign(input_data)
            elif task_type == "customer_segmentation":
                return await self.segment_customers(input_data)
            elif task_type == "personalized_email":
                return await self.create_personalized_email(input_data)
            elif task_type == "social_media_content":
                return await self.generate_social_content(input_data)
            elif task_type == "discount_strategy":
                return await self.optimize_discounts(input_data)

            return {"error": "Unknown task type", "agent_type": "marketing"}

        except Exception as e:
            return {
                "agent_type": "marketing",
                "task": task_type,
                "error": str(e)
            }

    async def generate_campaign(self, data: Dict) -> Dict[str, Any]:
        product_category = data.get("product_category", "electronics")
        target_audience = data.get("target_audience", "general")
        budget = data.get("budget", 5000)

        campaigns = {
            "electronics": {
                "name": "Tech Revolution Sale",
                "tagline": "Upgrade Your Life with Cutting-Edge Technology",
                "channels": ["email", "social_media", "google_ads"],
                "duration_days": 14,
                "expected_roi": 2.5
            },
            "fashion": {
                "name": "Summer Style Festival",
                "tagline": "Discover Your Perfect Look",
                "channels": ["instagram", "influencer", "email"],
                "duration_days": 21,
                "expected_roi": 3.2
            },
            "home": {
                "name": "Cozy Home Makeover",
                "tagline": "Transform Your Space, Transform Your Life",
                "channels": ["pinterest", "facebook", "email"],
                "duration_days": 30,
                "expected_roi": 2.8
            }
        }

        campaign = campaigns.get(product_category, campaigns["electronics"])

        return {
            "agent_type": "marketing",
            "task": "campaign_generation",
            "campaign": {
                "name": campaign["name"],
                "tagline": campaign["tagline"],
                "target_audience": target_audience,
                "budget": budget,
                "channels": campaign["channels"],
                "duration_days": campaign["duration_days"],
                "expected_roi": campaign["expected_roi"],
                "key_messages": [
                    "Limited time offer - Don't miss out!",
                    "Exclusive deals for loyal customers",
                    "Free shipping on orders over $50"
                ],
                "confidence": round(random.uniform(0.85, 0.95), 2)
            }
        }

    async def segment_customers(self, data: Dict) -> Dict[str, Any]:
        segments = [
            {
                "name": "VIP Customers",
                "size_percent": 15,
                "characteristics": ["High spenders", "Frequent buyers", "Brand loyal"],
                "strategy": "Exclusive offers, early access, personal shopper"
            },
            {
                "name": "Bargain Hunters",
                "size_percent": 35,
                "characteristics": ["Price sensitive", "Deal seekers", "Seasonal buyers"],
                "strategy": "Discount alerts, clearance sales, coupon codes"
            },
            {
                "name": "Window Shoppers",
                "size_percent": 25,
                "characteristics": ["Browse often", "Rarely purchase", "Research heavy"],
                "strategy": "Retargeting ads, abandoned cart emails, reviews"
            },
            {
                "name": "New Customers",
                "size_percent": 25,
                "characteristics": ["First-time buyers", "Exploring", "Uncommitted"],
                "strategy": "Welcome series, onboarding, first-purchase discount"
            }
        ]

        return {
            "agent_type": "marketing",
            "task": "customer_segmentation",
            "total_segments": len(segments),
            "segments": segments,
            "recommendation": "Focus on VIP retention and New Customer conversion",
            "confidence": round(random.uniform(0.88, 0.96), 2)
        }

    async def create_personalized_email(self, data: Dict) -> Dict[str, Any]:
        customer_name = data.get("customer_name", "Valued Customer")
        purchase_history = data.get("purchase_history", [])

        subject_lines = [
            f"{customer_name}, your exclusive offer is waiting!",
            "Don't miss out - Limited time deal inside",
            "We picked these just for you"
        ]

        email_body = f"""Hi {customer_name},

We noticed you've been browsing our latest collection. Based on your interests, we've curated special recommendations just for you!

SPECIAL OFFER: 20% OFF your next purchase
Code: SPECIAL20

Happy Shopping!
The E-Commerce Team"""

        return {
            "agent_type": "marketing",
            "task": "personalized_email",
            "email": {
                "subject": random.choice(subject_lines),
                "body": email_body,
                "personalization_score": round(random.uniform(0.75, 0.95), 2),
                "recommended_send_time": "Tuesday 10:00 AM",
                "expected_open_rate": "28%",
                "expected_click_rate": "12%"
            }
        }

    async def generate_social_content(self, data: Dict) -> Dict[str, Any]:
        platform = data.get("platform", "instagram")
        product = data.get("product", "new arrival")

        content_templates = {
            "instagram": {
                "caption": f"Introducing our latest {product}! Swipe to see why everyone's obsessed. Shop link in bio! #NewArrival #MustHave",
                "hashtags": ["#ShopNow", "#Trending", "#OOTD", "#Style"],
                "best_posting_time": "6:00 PM - 9:00 PM",
                "content_type": "carousel_post"
            },
            "facebook": {
                "caption": f"Big news! Our new {product} is here and flying off the shelves. Get yours before they're gone!",
                "hashtags": ["#NewProduct", "#LimitedStock", "#ShopToday"],
                "best_posting_time": "1:00 PM - 3:00 PM",
                "content_type": "video_post"
            },
            "twitter": {
                "caption": f"Hot drop: {product} now available! RT for a chance to win a $50 gift card. Shop: [link]",
                "hashtags": ["#NewDrop", "#Giveaway", "#ShopSmall"],
                "best_posting_time": "12:00 PM - 1:00 PM",
                "content_type": "text_with_image"
            }
        }

        content = content_templates.get(platform, content_templates["instagram"])

        return {
            "agent_type": "marketing",
            "task": "social_media_content",
            "platform": platform,
            "content": content,
            "expected_engagement": round(random.uniform(2.5, 8.5), 1),
            "confidence": round(random.uniform(0.80, 0.92), 2)
        }

    async def optimize_discounts(self, data: Dict) -> Dict[str, Any]:
        product_id = data.get("product_id", 1)
        current_price = data.get("current_price", 100)
        inventory_level = data.get("inventory_level", "medium")

        strategies = {
            "low": {
                "discount": 0,
                "strategy": "no_discount",
                "reason": "Low stock - maintain price",
                "urgency": "scarcity"
            },
            "medium": {
                "discount": 10,
                "strategy": "moderate_discount",
                "reason": "Steady sales - stimulate demand",
                "urgency": "limited_time"
            },
            "high": {
                "discount": 25,
                "strategy": "aggressive_discount",
                "reason": "High inventory - clear stock",
                "urgency": "clearance"
            }
        }

        strategy = strategies.get(inventory_level, strategies["medium"])
        new_price = current_price * (1 - strategy["discount"] / 100)

        return {
            "agent_type": "marketing",
            "task": "discount_optimization",
            "product_id": product_id,
            "pricing_strategy": {
                "current_price": current_price,
                "recommended_discount": f"{strategy['discount']}%",
                "new_price": round(new_price, 2),
                "strategy": strategy["strategy"],
                "reasoning": strategy["reason"],
                "urgency_tactic": strategy["urgency"],
                "expected_lift": f"{random.randint(15, 45)}%",
                "confidence": round(random.uniform(0.82, 0.94), 2)
            }
        }