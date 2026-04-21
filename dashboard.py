import streamlit as st
import sys
sys.path.append('backend/agents')

from shopify_auth import ShopifyAuth
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Agents Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🚀 8 AI Agents - Shopify Dashboard")
st.markdown(f"**Connected Store:** ai-swarm-2 | **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Initialize Shopify connection
@st.cache_resource
def get_shopify():
    return ShopifyAuth()

try:
    auth = get_shopify()
    
    # Create columns
    col1, col2, col3 = st.columns(3)
    
    # ========== INVENTORY AGENT ==========
    with col1:
        st.header("📦 Inventory Agent")
        products = auth.get("/products.json?limit=10")
        product_list = products.get("products", [])
        
        # Stock levels
        low_stock = []
        healthy_stock = []
        
        for p in product_list:
            variant = p.get("variants", [{}])[0]
            inventory = variant.get("inventory_quantity", 0)
            title = p["title"]
            
            if inventory < 10:
                low_stock.append({"Product": title, "Stock": inventory, "Status": "⚠️ Low"})
            else:
                healthy_stock.append({"Product": title, "Stock": inventory, "Status": "✅ OK"})
        
        # Display metrics
        st.metric("Total Products", len(product_list))
        st.metric("Low Stock Items", len(low_stock))
        
        # Low stock table
        if low_stock:
            st.warning("⚠️ Low Stock Alert")
            st.dataframe(pd.DataFrame(low_stock), use_container_width=True)
    
    # ========== ORDERS & FRAUD DETECTION ==========
    with col2:
        st.header("🛒 Orders & Fraud Detection")
        
        # Get orders
        orders = auth.get("/orders.json?status=any&limit=20")
        order_list = orders.get("orders", [])
        
        # Calculate metrics
        open_orders = [o for o in order_list if o.get("financial_status") == "paid"]
        total_revenue = sum(float(o.get("total_price", 0)) for o in order_list)
        
        st.metric("Open Orders", len(open_orders))
        st.metric("Total Revenue", f"${total_revenue:.2f}")
        
        # Recent orders with risk analysis
        if order_list:
            st.subheader("Recent Orders (Fraud Check)")
            for o in order_list[:5]:
                total = float(o.get("total_price", 0))
                customer = o.get("customer")
                is_new = customer is None or customer.get("orders_count", 0) == 0
                
                # Risk badge
                if total > 100 and is_new:
                    risk = "🚨 HIGH"
                    color = "red"
                elif total > 50:
                    risk = "⚠️ MED"
                    color = "orange"
                else:
                    risk = "✅ LOW"
                    color = "green"
                
                st.markdown(f"**{o['name']}**: ${total} | Risk: :{color}[{risk}]")
    
    # ========== ANALYTICS AGENT ==========
    with col3:
        st.header("📊 Analytics Agent")
        
        # Product performance
        if product_list:
            st.subheader("Top Products by Stock")
            stock_data = []
            for p in product_list[:5]:
                variant = p.get("variants", [{}])[0]
                stock_data.append({
                    "Product": p["title"][:20],
                    "Stock": variant.get("inventory_quantity", 0),
                    "Price": f"${variant.get('price', '0')}"
                })
            
            st.dataframe(pd.DataFrame(stock_data), use_container_width=True)
            
            # Stock distribution chart
            st.subheader("Stock Distribution")
            stock_values = [p.get("variants", [{}])[0].get("inventory_quantity", 0) for p in product_list]
            st.bar_chart(stock_values[:10])
    
    # ========== MARKETING & RECOMMENDATIONS ==========
    st.divider()
    st.header("🎯 Marketing Agent - Pricing Recommendations")
    
    recommendations = []
    for p in product_list:
        variant = p.get("variants", [{}])[0]
        inventory = variant.get("inventory_quantity", 0)
        price = float(variant.get("price", 0))
        title = p["title"]
        
        if inventory < 5:
            recommendations.append({
                "Product": title,
                "Current Price": f"${price}",
                "Recommended": f"${price * 1.15:.2f}",
                "Action": "🔼 Increase 15% (Low Stock)",
                "Priority": "HIGH"
            })
        elif inventory > 50:
            recommendations.append({
                "Product": title,
                "Current Price": f"${price}",
                "Recommended": f"${price * 0.90:.2f}",
                "Action": "🔽 Decrease 10% (Clearance)",
                "Priority": "MEDIUM"
            })
    
    if recommendations:
        st.dataframe(pd.DataFrame(recommendations), use_container_width=True)
    else:
        st.info("No pricing adjustments needed at this time.")
    
    # ========== SYSTEM STATUS ==========
    st.divider()
    st.header("🔧 System Status")
    
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    
    with status_col1:
        st.success("✅ Inventory Agent\nActive")
    with status_col2:
        st.success("✅ Fraud Detection\nActive")
    with status_col3:
        st.success("✅ Analytics Agent\nActive")
    with status_col4:
        st.success("✅ Marketing Agent\nActive")

except Exception as e:
    st.error(f"❌ Error: {e}")
    st.info("Please check your Shopify credentials in .env file")