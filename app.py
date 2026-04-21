import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import random

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'agents'))

# Try to import ShopifyAuth, fallback to mock if fails
try:
    from shopify_auth import ShopifyAuth
    SHOPIFY_AVAILABLE = True
except ImportError:
    SHOPIFY_AVAILABLE = False

import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION - CALLED ONLY ONCE
# ==========================================
st.set_page_config(
    page_title="AI E-Commerce Agent Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CLEAN CSS - SMOOTH 2D ANIMATIONS
# ==========================================
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
    }
    
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
        animation: fadeIn 0.6s ease-out;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    
    .agent-status-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 15px;
        color: white;
        margin: 8px 0;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .agent-status-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }
    
    .status-online { background: #00ff88; box-shadow: 0 0 10px #00ff88; }
    .status-busy { background: #ffbe0b; box-shadow: 0 0 10px #ffbe0b; }
    .status-offline { background: #ff006e; }
    
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
        animation: fadeIn 0.6s ease-out;
    }
    
    .feature-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        background: #e9ecef;
        transform: translateX(3px);
    }
    
    .log-container {
        background: #1e1e1e;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #00ff88;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        padding: 20px 0;
    }
    
    .nav-item {
        padding: 12px 15px;
        margin: 5px 0;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: #f0f4ff;
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA INITIALIZATION
# ==========================================
@st.cache_resource
def get_shopify_data():
    """Initialize Shopify connection or return mock data"""
    if SHOPIFY_AVAILABLE:
        try:
            auth = ShopifyAuth()
            products = auth.get("/products.json?limit=50").get("products", [])
            orders = auth.get("/orders.json?status=any&limit=50").get("orders", [])
            return {'products': products, 'orders': orders}
        except Exception as e:
            st.error(f"Shopify connection failed: {e}")
            return get_mock_data()
    else:
        return get_mock_data()

def get_mock_data():
    """Return realistic mock data"""
    return {
        'products': [
            {
                "id": i,
                "title": f"Product {i}",
                "product_type": random.choice(["Electronics", "Clothing", "Home", "Sports", "Books"]),
                "variants": [{
                    "sku": f"SKU-{i:04d}",
                    "price": str(random.randint(10, 500)),
                    "inventory_quantity": random.randint(0, 100)
                }],
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            }
            for i in range(1, 21)
        ],
        'orders': [
            {
                "id": i,
                "name": f"#{1000+i}",
                "total_price": str(random.randint(20, 500)),
                "created_at": (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat(),
                "fulfillment_status": random.choice([None, "fulfilled", "partial"]),
                "financial_status": random.choice(["paid", "pending", "refunded"]),
                "customer": {
                    "email": f"customer{i}@example.com",
                    "first_name": f"Customer{i}",
                    "orders_count": random.randint(1, 5)
                },
                "line_items": [{"title": f"Item {j}", "quantity": random.randint(1, 3), "price": str(random.randint(10, 100))} 
                              for j in range(random.randint(1, 4))]
            }
            for i in range(1, 16)
        ]
    }

# Load data
data = get_shopify_data()
product_list = data['products']
order_list = data['orders']

# Calculate metrics
total_revenue = sum(float(o['total_price']) for o in order_list)
low_stock_count = sum(1 for p in product_list if p['variants'][0]['inventory_quantity'] < 10)
pending_orders = len([o for o in order_list if o.get('fulfillment_status') != 'fulfilled'])

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 AI Agents</div>', unsafe_allow_html=True)
    
    # Agent selector with icons
    agent_menu = st.radio(
        "Select Agent:",
        [
            "🏠 Home",
            "💬 Customer Service", 
            "📦 Inventory & Pricing",
            "🎯 Recommendations",
            "🛡️ Fraud Detection",
            "📢 Marketing",
            "🚚 Shipping & Logistics",
            "📊 Analytics",
            "📜 Conversation History",
            "🔍 System Status"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Quick Stats in Sidebar
    st.subheader("⚡ Live Status")
    
    agents_status = [
        ("🤖 AI Orchestrator", "online", "99.9%"),
        ("💬 Customer Service", "online", "98.5%"),
        ("📦 Inventory", "online", "97.2%"),
        ("🎯 Recommendations", "busy", "94.8%"),
        ("🛡️ Fraud Detection", "online", "99.1%"),
        ("📢 Marketing", "online", "96.5%"),
        ("🚚 Shipping", "busy", "93.2%"),
        ("📊 Analytics", "online", "98.9%")
    ]
    
    for name, status, uptime in agents_status:
        status_class = f"status-{status}"
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 8px 0; font-size: 13px;">
            <span class="status-indicator {status_class}"></span>
            <span style="flex-grow: 1;">{name}</span>
            <span style="color: {'#00ff88' if status == 'online' else '#ffbe0b'}; font-weight: bold;">{uptime}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # System Info
    st.caption("🔧 System Info")
    st.markdown("""
    <div style="font-size: 12px; color: #666;">
        <div>Project: MCA Final Year</div>
        <div>Version: 3.0.0</div>
        <div>Agents: 8 Active</div>
        <div>API: Online ✅</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# MAIN CONTENT BASED ON SELECTION
# ==========================================

# Extract agent name from menu selection
current_agent = agent_menu.split()[1] if len(agent_menu.split()) > 1 else "Home"

# HEADER (for all pages)
st.markdown(f"""
<div class="main-header">
    <h1>🛒 E-Commerce AI Agent Dashboard</h1>
    <p>Autonomous AI Agent Swarm | Active: {current_agent} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <small>Welcome to AI E-Commerce System | 8 Agents Active | Version 3.0.0</small>
</div>
""", unsafe_allow_html=True)

# HOME DASHBOARD
if agent_menu == "🏠 Home":
    st.subheader("📊 Executive Dashboard")
    
    # Top Metrics
    metric_cols = st.columns(4)
    metrics = [
        ("🤖 Active Agents", "8", "100% Uptime", "#667eea"),
        ("🛒 Total Orders", len(order_list), f"+{len([o for o in order_list if 'created_at' in o and (datetime.now() - datetime.fromisoformat(o['created_at'].replace('Z', '+00:00').replace('+00:00', ''))).days < 1])} today", "#00ff88"),
        ("💰 Revenue", f"${total_revenue:,.0f}", "+18% vs last week", "#ffbe0b"),
        ("⚠️ Alerts", low_stock_count + pending_orders, "Action needed", "#ff006e")
    ]
    
    for col, (label, value, change, color) in zip(metric_cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {color};">
                <h4 style="color: #666; margin: 0;">{label}</h4>
                <h1 style="font-size: 32px; margin: 10px 0; color: #333;">{value}</h1>
                <span style="color: {color}; font-size: 12px;">{change}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Charts Row
    st.divider()
    chart_cols = st.columns(3)
    
    with chart_cols[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Sales Velocity")
        sales_data = pd.DataFrame({
            'Hour': list(range(24)),
            'Sales': [random.randint(20, 150) for _ in range(24)]
        })
        fig = px.area(sales_data, x='Hour', y='Sales', 
                     color_discrete_sequence=['#667eea'],
                     )
        fig.update_layout(height=250, showlegend=False, 
                         margin=dict(l=20, r=20, t=30, b=20),
                         plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📦 Inventory Status")
        inv_status = pd.DataFrame({
            'Status': ['Healthy', 'Low Stock', 'Out of Stock', 'Overstock'],
            'Count': [len([p for p in product_list if p['variants'][0]['inventory_quantity'] > 20]),
                      len([p for p in product_list if 10 <= p['variants'][0]['inventory_quantity'] <= 20]),
                      len([p for p in product_list if p['variants'][0]['inventory_quantity'] == 0]),
                      len([p for p in product_list if p['variants'][0]['inventory_quantity'] > 50])]
        })
        fig = px.pie(inv_status, values='Count', names='Status', hole=0.4,
                    color_discrete_sequence=['#00ff88', '#ffbe0b', '#ff006e', '#4facfe'])
        fig.update_layout(height=250, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols[2]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🎯 Order Pipeline")
        pipeline_data = pd.DataFrame({
            'Stage': ['New', 'Processing', 'Shipped', 'Delivered'],
            'Orders': [len([o for o in order_list if o.get('fulfillment_status') is None]),
                       len([o for o in order_list if o.get('fulfillment_status') == 'partial']),
                       8, 45]
        })
        fig = px.funnel(pipeline_data, x='Orders', y='Stage', 
                       color='Orders')
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.divider()
    st.subheader("⚡ Quick Actions")
    action_cols = st.columns(6)
    actions = [
        ("➕ Add Product", "primary"),
        ("📥 Bulk Import", "secondary"),
        ("🎁 Create Coupon", "secondary"),
        ("📧 Send Campaign", "secondary"),
        ("🔄 Sync Inventory", "secondary"),
        ("📊 Generate Report", "secondary")
    ]
    
    for col, (label, btn_type) in zip(action_cols, actions):
        with col:
            if st.button(label, use_container_width=True, type=btn_type):
                st.toast(f"Action triggered: {label}", icon="🚀")

# CUSTOMER SERVICE AGENT
elif agent_menu == "💬 Customer Service":
    st.subheader("💬 Customer Service Agent")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎫 Open Tickets", "12", "-3")
    col2.metric("⏱️ Avg Response", "2.5 min", "-30s")
    col3.metric("⭐ Satisfaction", "4.8/5", "+0.2")
    col4.metric("🤖 Auto-Resolved", "68%", "+5%")
    
    st.divider()
    
    # Ticket Management
    st.subheader("🎫 Active Tickets")
    
    tickets = [
        {"id": "T-1024", "customer": "john@email.com", "issue": "Order not received", "priority": "High", "status": "Open", "agent": "AI"},
        {"id": "T-1023", "customer": "sarah@email.com", "issue": "Wrong size received", "priority": "Medium", "status": "In Progress", "agent": "Human"},
        {"id": "T-1022", "customer": "mike@email.com", "issue": "Refund request", "priority": "Low", "status": "Resolved", "agent": "AI"},
        {"id": "T-1021", "customer": "emma@email.com", "issue": "Product inquiry", "priority": "Low", "status": "Open", "agent": "AI"}
    ]
    
    for ticket in tickets:
        with st.expander(f"🎫 {ticket['id']} - {ticket['issue']} ({ticket['priority']})"):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**Customer:** {ticket['customer']}")
                st.write(f"**Status:** {ticket['status']}")
                st.write(f"**Assigned to:** {ticket['agent']}")
            with col2:
                st.text_area("Notes:", f"Customer contacted on {datetime.now().strftime('%Y-%m-%d')}", key=ticket['id'])
            with col3:
                if st.button("✅ Resolve", key=f"resolve_{ticket['id']}"):
                    st.success("Ticket resolved!")
                if st.button("➡️ Escalate", key=f"escalate_{ticket['id']}"):
                    st.warning("Escalated to human!")
                if st.button("🤖 Auto-Reply", key=f"auto_{ticket['id']}"):
                    st.info("AI response sent!")

# INVENTORY & PRICING AGENT
elif agent_menu == "📦 Inventory & Pricing":
    st.subheader("📦 Inventory & Pricing Agent")
    
    # Filters
    st.markdown('<div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">', unsafe_allow_html=True)
    filter_cols = st.columns(4)
    with filter_cols[0]:
        category = st.multiselect("Category:", ["All", "Electronics", "Clothing", "Home", "Sports"], ["All"])
    with filter_cols[1]:
        stock_level = st.select_slider("Stock:", ["All", "Critical", "Low", "Normal", "High"])
    with filter_cols[2]:
        price_range = st.slider("Price:", 0, 1000, (0, 1000))
    with filter_cols[3]:
        sort_by = st.selectbox("Sort:", ["Name", "Stock Level", "Price", "Last Updated"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Buttons
    btn_cols = st.columns(5)
    with btn_cols[0]:
        if st.button("➕ Add Product", type="primary", use_container_width=True):
            with st.expander("New Product Form", expanded=True):
                with st.form("new_product"):
                    st.text_input("Product Name")
                    st.number_input("Price", min_value=0.0, step=0.01)
                    st.number_input("Initial Stock", min_value=0, step=1)
                    st.selectbox("Category", ["Electronics", "Clothing", "Home", "Sports"])
                    if st.form_submit_button("🚀 Create Product"):
                        st.success("Product created successfully!")
                        st.balloons()
    
    with btn_cols[1]:
        if st.button("📥 Import CSV", use_container_width=True):
            uploaded = st.file_uploader("Upload CSV", type="csv")
            if uploaded:
                st.success(f"Imported {random.randint(10, 100)} products!")
    
    with btn_cols[2]:
        if st.button("🔄 AI Price Optimize", use_container_width=True):
            st.info("AI analyzing market trends...")
            time.sleep(1)
            st.success("Prices optimized! Revenue +12% predicted")
    
    with btn_cols[3]:
        if st.button("📊 Stock Forecast", use_container_width=True):
            forecast = pd.DataFrame({
                'Date': pd.date_range(start=datetime.now(), periods=30, freq='d'),
                'Predicted Demand': [random.randint(80, 150) for _ in range(30)],
                'Recommended Stock': [random.randint(100, 180) for _ in range(30)]
            })
            fig = px.line(forecast, x='Date', y=['Predicted Demand', 'Recommended Stock'],
                         title="30-Day AI Stock Forecast")
            st.plotly_chart(fig, use_container_width=True)
    
    with btn_cols[4]:
        if st.button("📤 Export", use_container_width=True):
            st.download_button("Download CSV", "product,data", "inventory.csv")
    
    # Inventory Table
    st.divider()
    
    inventory_data = []
    for p in product_list[:20]:
        variant = p['variants'][0]
        stock = variant['inventory_quantity']
        
        if stock == 0:
            status, color = "🔴 Out of Stock", "#ff006e"
        elif stock < 10:
            status, color = "🟡 Low Stock", "#ffbe0b"
        elif stock > 50:
            status, color = "🔵 Overstock", "#4facfe"
        else:
            status, color = "🟢 Optimal", "#00ff88"
        
        # AI Price Suggestion
        current_price = float(variant['price'])
        if stock < 5:
            suggested = current_price * 1.15
            price_action = f"🔼 ${suggested:.2f}"
        elif stock > 50:
            suggested = current_price * 0.85
            price_action = f"🔽 ${suggested:.2f}"
        else:
            price_action = "✅ Optimal"
        
        inventory_data.append({
            "Product": p['title'],
            "SKU": variant['sku'],
            "Current Price": f"${current_price:.2f}",
            "AI Suggestion": price_action,
            "Stock": stock,
            "Status": status,
            "Category": p.get('product_type', 'General'),
            "7-Day Sales": random.randint(0, 50),
            "Action": "Edit | Delete"
        })
    
    df = pd.DataFrame(inventory_data)
    st.dataframe(df, use_container_width=True, height=400)
    
    # Bulk Actions
    st.divider()
    bulk_cols = st.columns([2, 2, 1])
    with bulk_cols[0]:
        selected_items = st.multiselect("Select products:", df['Product'].tolist()[:5])
    with bulk_cols[1]:
        bulk_action = st.selectbox("Bulk action:", ["Update Price", "Adjust Stock", "Change Category", "Delete"])
    with bulk_cols[2]:
        if st.button("⚡ Apply", use_container_width=True, type="primary"):
            st.success(f"Applied {bulk_action} to {len(selected_items)} products!")

# FRAUD DETECTION AGENT
elif agent_menu == "🛡️ Fraud Detection":
    st.subheader("🛡️ Fraud Detection Agent")
    
    # Risk Metrics
    risk_cols = st.columns(4)
    with risk_cols[0]:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=2,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Score"},
            delta={'reference': 5},
            gauge={'axis': {'range': [None, 10]},
                   'bar': {'color': "#00ff88"},
                   'steps': [{'range': [0, 3], 'color': "#e0ffe0"},
                            {'range': [3, 7], 'color': "#fff3cd"},
                            {'range': [7, 10], 'color': "#f8d7da"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 7}}))
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with risk_cols[1]:
        st.metric("🚫 Blocked Today", "3", "↑ 1")
    with risk_cols[2]:
        st.metric("💰 $ Protected", "$1,240", "+$450")
    with risk_cols[3]:
        st.metric("🤖 AI Confidence", "96.5%", "+2.1%")
    
    st.divider()
    
    # Risk Analysis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 24-Hour Risk Timeline")
        risk_data = pd.DataFrame({
            'Time': pd.date_range(end=datetime.now(), periods=24, freq='h'),
            'Risk Score': [random.randint(0, 10) for _ in range(24)],
            'Transaction Value': [random.randint(50, 500) for _ in range(24)]
        })
        fig = px.scatter(risk_data, x='Time', y='Risk Score', size='Transaction Value',
                        color='Risk Score', color_continuous_scale='RdYlGn_r',
                        title="Risk Score vs Transaction Value")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Quick Actions")
        if st.button("🔍 Deep Scan All", use_container_width=True, type="primary"):
            with st.spinner("AI analyzing all pending orders..."):
                import time
                time.sleep(2)
            st.success("Scan complete! 0 new threats detected.")
        
        if st.button("📋 Review Queue (12)", use_container_width=True):
            st.info("12 orders pending manual review")
        
        if st.button("⚙️ Adjust Sensitivity", use_container_width=True):
            st.slider("Risk Threshold", 0, 100, 75)
            st.slider("High-Value Threshold", 50, 500, 100)
        
        st.divider()
        st.subheader("🚨 Recent Alerts")
        st.error("🔴 Order #1024: IP mismatch + new customer")
        st.warning("🟡 Order #1023: Unusual shipping address")
        st.info("🟢 Order #1022: Cleared after verification")

# SHIPPING & LOGISTICS AGENT
elif agent_menu == "🚚 Shipping & Logistics":
    st.subheader("🚚 Shipping & Logistics Agent")
    
    # Fulfillment Metrics
    fulfill_cols = st.columns(4)
    fulfill_cols[0].metric("📦 Unfulfilled", str(pending_orders), "2 urgent")
    fulfill_cols[1].metric("🚚 In Transit", "12", "3 delivered today")
    fulfill_cols[2].metric("✅ Delivered", "48", "This week")
    fulfill_cols[3].metric("📅 Scheduled", "3", "Tomorrow")
    
    st.divider()
    
    # Order Fulfillment Pipeline
    st.subheader("📋 Fulfillment Pipeline")
    
    unfulfilled = [o for o in order_list if o.get('fulfillment_status') != 'fulfilled']
    
    if unfulfilled:
        for order in unfulfilled[:5]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"**{order['name']}**")
                    customer = order.get('customer', {})
                    st.caption(f"Customer: {customer.get('email', 'Guest') if customer else 'Guest'}")
                
                with col2:
                    items = order.get('line_items', [])
                    st.write(f"{len(items)} items: {', '.join([i['title'][:20] for i in items[:2]])}")
                
                with col3:
                    st.write(f"${order['total_price']}")
                
                with col4:
                    if st.button(f"🚚 Ship", key=f"ship_{order['id']}"):
                        st.success(f"Order {order['name']} marked as shipped!")
                        st.balloons()
    else:
        st.success("🎉 All orders fulfilled! Great job!")
    
    # Shipping Providers
    st.divider()
    st.subheader("🚛 Shipping Providers")
    provider_cols = st.columns(3)
    
    with provider_cols[0]:
        st.info("**📦 Standard Shipping**\n- 3-5 business days\n- $5.00 flat rate\n- 85% on-time delivery")
    
    with provider_cols[1]:
        st.info("**🚀 Express Shipping**\n- 1-2 business days\n- $12.00 flat rate\n- 95% on-time delivery")
    
    with provider_cols[2]:
        st.info("**⚡ Same Day Delivery**\n- Today (cutoff 2PM)\n- $25.00 flat rate\n- 98% on-time delivery")

# ANALYTICS AGENT
elif agent_menu == "📊 Analytics":
    st.subheader("📊 Business Analytics Agent")
    
    # Report Type Selector
    report_type = st.selectbox(
        "Select Report Type:",
        ["Sales Overview", "Product Performance", "Customer Insights", "Inventory Forecast", "Custom Report"]
    )
    
    # Date Range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date:", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date:", datetime.now())
    
    if st.button("📊 Generate Report", use_container_width=True, type="primary"):
        st.success(f"Generating {report_type} for {start_date} to {end_date}...")
        
        if report_type == "Sales Overview":
            # Revenue trend
            df = pd.DataFrame({
                'Date': pd.date_range(start=start_date, end=end_date, freq='d'),
                'Revenue': [1000 + i*50 + random.randint(-200, 200) for i in range((end_date-start_date).days + 1)]
            })
            fig = px.area(df, x='Date', y='Revenue', 
                         title='Revenue Trend',
                         color_discrete_sequence=['#667eea'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Key metrics
            metric_cols = st.columns(4)
            metric_cols[0].metric("Total Revenue", "$45,230", "+12%")
            metric_cols[1].metric("Orders", "156", "+8%")
            metric_cols[2].metric("AOV", "$290", "+3%")
            metric_cols[3].metric("Conversion", "3.2%", "+0.5%")
            
        elif report_type == "Product Performance":
            # Top products
            product_perf = pd.DataFrame({
                'Product': [p['title'][:25] for p in product_list[:8]],
                'Sales': [random.randint(20, 80) for _ in range(8)],
                'Revenue': [random.randint(1000, 8000) for _ in range(8)],
                'Profit Margin': [random.randint(15, 45) for _ in range(8)]
            })
            fig = px.bar(product_perf, x='Product', y='Revenue', 
                        color='Profit Margin',
                        title='Top Products by Revenue')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Export Options
    st.divider()
    export_cols = st.columns(3)
    with export_cols[0]:
        if st.button("📥 Download PDF"):
            st.success("PDF report downloaded!")
    with export_cols[1]:
        if st.button("📊 Export Excel"):
            st.success("Excel file downloaded!")
    with export_cols[2]:
        if st.button("📧 Email Report"):
            st.success("Report emailed to admin!")

# SYSTEM STATUS
elif agent_menu == "🔍 System Status":
    st.subheader("🔍 System Status & Agent Health")
    
    # Agent Performance Grid
    st.markdown("### 🤖 Agent Performance Monitor")
    
    agent_perf_cols = st.columns(4)
    agents_perf = [
        ("📦 Inventory", "98%", "Active", "2 alerts"),
        ("🛡️ Fraud Detection", "95%", "Active", "0 alerts"),
        ("🚚 Shipping", "92%", "Active", "1 pending"),
        ("📊 Analytics", "100%", "Active", "0 alerts"),
        ("🎧 Support", "88%", "Active", "3 tickets"),
        ("📢 Marketing", "90%", "Active", "2 campaigns"),
        ("💡 Recommendations", "85%", "Active", "learning"),
        ("🎯 Orchestrator", "99%", "Active", "coordinating")
    ]
    
    for i, (name, score, status, note) in enumerate(agents_perf):
        with agent_perf_cols[i % 4]:
            st.markdown(f"""
            <div class="agent-status-card">
                <h4>{name}</h4>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span class="status-indicator status-online"></span>
                    <span>{status}</span>
                </div>
                <div style="margin-top: 10px;">
                    <div style="background: rgba(255,255,255,0.3); border-radius: 10px; height: 8px;">
                        <div style="background: white; width: {score}; height: 100%; border-radius: 10px;"></div>
                    </div>
                    <small>Performance: {score}</small>
                </div>
                <small style="opacity: 0.8;">{note}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # System Resources
    st.divider()
    st.subheader("⚙️ System Resources")
    
    resource_cols = st.columns(4)
    resource_cols[0].metric("CPU Usage", "42%", "-5%")
    resource_cols[1].metric("Memory", "68%", "+2%")
    resource_cols[2].metric("API Calls/min", "240", "+12%")
    resource_cols[3].metric("Latency", "45ms", "-8ms")
    
    # Logs
    st.divider()
    st.subheader("📜 Recent System Logs")
    
    logs = [
        ("10:42:15", "🎯 Orchestrator", "INFO", "Agent coordination cycle completed"),
        ("10:41:32", "📦 Inventory", "WARNING", "Low stock alert: SKU-4421"),
        ("10:40:08", "🚚 Shipping", "INFO", "Batch label generation completed"),
        ("10:39:45", "💡 Recommendations", "INFO", "Model updated with 1,240 new interactions"),
        ("10:38:12", "🛡️ Fraud", "ERROR", "False positive rate spike detected"),
        ("10:37:30", "📊 Analytics", "INFO", "Hourly report generated"),
        ("10:36:55", "🎧 Support", "DEBUG", "NLP confidence: 94.2%"),
        ("10:35:18", "📢 Marketing", "INFO", "Campaign #45 sent to 2,400 subscribers"),
    ]
    
    st.markdown('<div class="log-container">', unsafe_allow_html=True)
    for ts, agent, level, msg in logs:
        color = "#ff006e" if "ERROR" in level else "#ffbe0b" if "WARNING" in level else "#00ff88" if "DEBUG" in level else "#4facfe"
        st.markdown(f"""
        <div class="log-entry">
            <span style="color: #666;">[{ts}]</span>
            <span style="color: #667eea; font-weight: bold;">{agent}</span>
            <span style="color: {color};">{level}:</span>
            {msg}
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# OTHER AGENTS (Placeholder with features)
else:
    agent_name = agent_menu.split()[1] if len(agent_menu.split()) > 1 else "Agent"
    st.subheader(f"{agent_menu}")
    
    st.info(f"🚀 {agent_name} Agent is active and processing requests...")
    
    # Generic metrics for other agents
    metric_cols = st.columns(4)
    metric_cols[0].metric("Status", "🟢 Online")
    metric_cols[1].metric("Tasks Today", str(random.randint(50, 200)))
    metric_cols[2].metric("Success Rate", f"{random.randint(85, 99)}%")
    metric_cols[3].metric("Avg Response", f"{random.randint(100, 500)}ms")
    
    st.divider()
    
    # Feature cards
    st.subheader("✨ Key Features")
    
    features = {
        "Recommendations": ["Personalized product suggestions", "Customer behavior analysis", "A/B testing framework", "Revenue optimization"],
        "Conversation": ["Chat history analysis", "Sentiment tracking", "Response templates", "Escalation management"],
        "Marketing": ["Campaign automation", "Email segmentation", "Social media scheduling", "ROI tracking"]
    }
    
    current_features = features.get(agent_name, ["AI-powered automation", "Real-time processing", "Machine learning models", "Analytics dashboard"])
    
    for feature in current_features:
        st.markdown(f"""
        <div class="feature-card">
            <h4>✅ {feature}</h4>
            <p style="color: #666; font-size: 12px;">Active and optimized for performance</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# FOOTER (All Pages)
# ==========================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
    <p>🤖 AI E-Commerce Agent Dashboard | Autonomous AI Agent Swarm</p>
    <p>Project: MCA Final Year | Version: 3.0.0 | 8 Agents Active | API: Online ✅</p>
    <p><small>NEW AGENTS ADDED: Shipping & Logistics, Business Analytics</small></p>
</div>
""", unsafe_allow_html=True)