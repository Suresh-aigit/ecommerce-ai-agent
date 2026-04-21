"""
Emoji Formatter for All 8 E-Commerce Agents
Converts JSON responses to beautiful emoji summaries
"""


class EmojiFormatter:
    
    @staticmethod
    def inventory(result: dict) -> str:
        """📦 Inventory & Pricing Agent"""
        a = result.get("analysis", {})
        stock = a.get("current_stock", "?")
        status = a.get("stock_status", "unknown")
        action = a.get("recommended_action", "none")
        lead_time = a.get("supplier_lead_time", "?")
        note = a.get("note", "No notes")
        
        status_emojis = {
            "adequate": "✅",
            "low": "⚠️", 
            "critical": "🚨",
            "out_of_stock": "❌"
        }
        status_emoji = status_emojis.get(status, "⚪")
        
        action_text = "No reorder needed" if action == "none" else action.replace("_", " ").title()
        action_emoji = "💰" if action == "none" else "🛒"
        action_result = "Saving money" if action == "none" else "Action required"
        
        return f"""
🎯 Quick Summary
"""
    
    @staticmethod
    def analytics(result: dict) -> str:
        """📊 Analytics Agent"""
        data = result.get("data", {})
        metrics = data.get("metrics", {})
        
        sales = metrics.get("total_sales", "N/A")
        orders = metrics.get("total_orders", "N/A")
        revenue = metrics.get("revenue", "N/A")
        trend = data.get("trend", "stable")
        
        trend_emojis = {"up": "📈", "down": "📉", "stable": "➡️"}
        trend_emoji = trend_emojis.get(trend, "➡️")
        
        return f"""
🎯 Quick Summary
"""
    
    @staticmethod
    def fraud(result: dict) -> str:
        """🛡️ Fraud Detection Agent"""
        a = result.get("analysis", {})
        risk = a.get("risk_level", "unknown")
        score = a.get("fraud_score", 0)
        status = a.get("status", "pending")
        
        risk_emojis = {"low": "🟢", "medium": "🟡", "high": "🔴", "critical": "🚨"}
        risk_emoji = risk_emojis.get(risk, "⚪")
        
        status_emojis = {"approved": "✅", "flagged": "⚠️", "rejected": "❌", "pending": "⏳"}
        status_emoji = status_emojis.get(status, "⚪")
        
        score_text = "✅ Safe" if score < 30 else "⚠️ Review" if score < 70 else "🚨 Block"
        
        return f"""
🎯 Quick Summary
"""
    
    @staticmethod
    def recommendation(result: dict) -> str:
        """🎯 Recommendations Agent"""
        recs = result.get("recommendations", [])
        user = result.get("user_segment", "general")
        count = len(recs)
        
        top_product = recs[0].get("product_name", "N/A") if recs else "No matches"
        confidence = recs[0].get("confidence", 0) if recs else 0
        
        return f"""
🎯 Quick Summary
"""
    
    @staticmethod
    def marketing(result: dict) -> str:
        """📢 Marketing Agent"""
        campaign = result.get("campaign", {})
        name = campaign.get("name", "Unnamed")
        channel = campaign.get("channel", "multi")
        reach = campaign.get("estimated_reach", "N/A")
        roi = campaign.get("projected_roi", "N/A")
        
        return f"""
🎯 Quick Summary
"""
    
    @staticmethod
    def shipping(result: dict) -> str:
        """🚚 Shipping & Logistics Agent"""
        a = result.get("analysis", {})
        order_id = result.get("order_id", "N/A")
        status = a.get("status", "processing")
        eta = a.get("estimated_delivery", "N/A")
        carrier = a.get("carrier", "N/A")
        
        status_emojis = {
            "processing": "⏳",
            "shipped": "🚚",
            "in_transit": "🚛",
            "out_for_delivery": "🛵",
            "delivered": "✅",
            "delayed": "⚠️"
        }
        status_emoji = status_emojis.get(status, "📦")
        
        return f"""
🎯 Quick Summary
"""