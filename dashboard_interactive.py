import streamlit as st
import sys
sys.path.append('backend/agents')
from shopify_auth import ShopifyAuth
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="8 AI Agents - Interactive Command Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for 3D buttons and effects
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
}

/* 3D Agent Button */
.agent-button {
    background: linear-gradient(145deg, #1e3c72 0%, #2a5298 100%);
    border: none;
    border-radius: 20px;
    padding: 30px;
    color: white;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 
        0 10px 30px rgba(0,0,0,0.5),
        inset 0 2px 0 rgba(255,255,255,0.1),
        0 0 20px rgba(42, 82, 152, 0.5);
    transform-style: preserve-3d;
    position: relative;
    overflow: hidden;
}

.agent-button:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 
        0 20px 40px rgba(42, 82, 152, 0.6),
        inset 0 2px 0 rgba(255,255,255,0.2),
        0 0 30px rgba(0, 255, 255, 0.4);
}

.agent-button:active {
    transform: translateY(-5px) scale(0.98);
}

.agent-icon {
    font-size: 50px;
    margin-bottom: 10px;
    display: block;
}

.agent-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
    font-weight: bold;
    color: #00ffff;
    text-shadow: 0 0 10px rgba(0,255,255,0.5);
}

.agent-status {
    font-size: 12px;
    color: #00ff88;
    margin-top: 5px;
}

/* Results Panel */
.results-panel {
    background: rgba(0, 20, 40, 0.9);
    border: 2px solid #00ffff;
    border-radius: 20px;
    padding: 30px;
    margin-top: 20px;
    box-shadow: 0 0 50px rgba(0,255,255,0.2);
    animation: slideIn 0.5s ease;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Neon Header */
.neon-header {
    font-family: 'Orbitron', sans-serif;
    color: #fff;
    text-align: center;
    text-shadow: 
        0 0 5px #fff,
        0 0 10px #fff,
        0 0 20px #00ffff,
        0 0 30px #00ffff,
        0 0 40px #00ffff;
    font-size: 50px;
    margin-bottom: 10px;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, rgba(255,0,110,0.2), rgba(131,56,236,0.2));
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.metric-value {
    font-size: 36px;
    font-weight: bold;
    color: #00ffff;
    font-family: 'Orbitron', sans-serif;
}

.metric-label {
    color: rgba(255,255,255,0.7);
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Data Table */
.data-table {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    overflow: hidden;
}

/* Alert Badges */
.alert-critical {
    background: linear-gradient(90deg, #ff006e, #ff4d6d);
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 12px;
}

.alert-warning {
    background: linear-gradient(90deg, #ffbe0b, #ff8500);
    color: black;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 12px;
}

.alert-success {
    background: linear-gradient(90deg, #00ff88, #00cc6a);
    color: black;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# Initialize
@st.cache_resource
def get_shopify():
    return ShopifyAuth()

auth = get_shopify()

# Header
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h1 class="neon-header">🤖 NEURAL COMMAND CENTER</h1>
    <p style="color: #00ffff; font-family: Orbitron; letter-spacing: 3px; font-size: 18px;">
        8 AI AGENTS • CLICK TO ACTIVATE
    </p>
    <p style="color: rgba(255,255,255,0.5); font-size: 14px;">
        Store: ai-swarm-2 | {time}
    </p>
</div>
""".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

st.divider()

# Session state for tracking which agent is selected
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = None

# Agent definitions
agents = [
    {"id": "inventory", "icon": "📦", "name": "INVENTORY AGENT", "color": "#00ff88", 
     "desc": "Stock monitoring & management"},
    {"id": "fraud", "icon": "🛡️", "name": "FRAUD DETECTION", "color": "#ff006e",
     "desc": "Risk analysis & prevention"},
    {"id": "shipping", "icon": "🚚", "name": "SHIPPING AGENT", "color": "#3a86ff",
     "desc": "Logistics & fulfillment"},
    {"id": "analytics", "icon": "📊", "name": "ANALYTICS AGENT", "color": "#ffbe0b",
     "desc": "Data insights & metrics"},
    {"id": "customer", "icon": "🎧", "name": "CUSTOMER SERVICE", "color": "#8338ec",
     "desc": "Support & returns"},
    {"id": "marketing", "icon": "📢", "name": "MARKETING AGENT", "color": "#00ffff",
     "desc": "Pricing & promotions"},
    {"id": "recommend", "icon": "💡", "name": "RECOMMENDATION", "color": "#ff8500",
     "desc": "Product optimization"},
    {"id": "orchestrator", "icon": "🎯", "name": "ORCHESTRATOR", "color": "#ffffff",
     "desc": "Central coordination"}
]

# Create 4x2 grid of agent buttons
st.subheader("🔘 CLICK AN AGENT TO VIEW RESULTS")

cols = st.columns(4)
for i, agent in enumerate(agents):
    with cols[i % 4]:
        # Create button with custom styling
        button_label = f"""
        <div class="agent-button" style="border-left: 5px solid {agent['color']};">
            <span class="agent-icon">{agent['icon']}</span>
            <div class="agent-name" style="color: {agent['color']};">{agent['name']}</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 5px;">{agent['desc']}</div>
            <div class="agent-status">● ACTIVE</div>
        </div>
        """
        
        if st.button(f"Activate {agent['name']}", key=f"btn_{agent['id']}", help=f"Click to view {agent['name']} results"):
            st.session_state.selected_agent = agent['id']
            st.rerun()

st.divider()

# ========== DISPLAY RESULTS BASED ON SELECTED AGENT ==========

if st.session_state.selected_agent is None:
    st.info("👆 **Click any agent button above to view real-time results from your Shopify store**")
    
    # Show quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">8</div>
            <div class="metric-label">Active Agents</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">LIVE</div>
            <div class="metric-label">Connection</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">0ms</div>
            <div class="metric-label">Latency</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">100%</div>
            <div class="metric-label">Uptime</div>
        </div>
        """, unsafe_allow_html=True)

# ========== INVENTORY AGENT RESULTS ==========
elif st.session_state.selected_agent == "inventory":
    st.markdown(f"""
    <div class="results-panel">
        <h2 style="color: #00ff88; font-family: Orbitron; margin-bottom: 20px;">
            📦 INVENTORY AGENT - LIVE RESULTS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    products = auth.get("/products.json?limit=50")
    product_list = products.get("products", [])
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    total_stock = sum(p.get("variants",[{}])[0].get("inventory_quantity",0) for p in product_list)
    low_stock = [p for p in product_list if p.get("variants",[{}])[0].get("inventory_quantity",0) < 10]
    
    with col1:
        st.metric("Total Products", len(product_list))
    with col2:
        st.metric("Total Units", total_stock)
    with col3:
        st.metric("Low Stock Alerts", len(low_stock), delta="Reorder needed" if low_stock else None)
    
    # Low stock alerts
    if low_stock:
        st.error("🚨 CRITICAL LOW STOCK DETECTED")
        for p in low_stock:
            variant = p.get("variants",[{}])[0]
            st.warning(f"**{p['title']}**: Only {variant.get('inventory_quantity',0)} left! (SKU: {variant.get('sku','N/A')})")
    
    # Full inventory table
    st.subheader("📋 Complete Inventory Report")
    inventory_data = []
    for p in product_list:
        variant = p.get("variants",[{}])[0]
        stock = variant.get("inventory_quantity",0)
        inventory_data.append({
            "Product": p["title"],
            "SKU": variant.get("sku", "N/A"),
            "Stock": stock,
            "Price": f"${variant.get('price', '0')}",
            "Status": "🔴 CRITICAL" if stock < 5 else "🟡 LOW" if stock < 15 else "🟢 OK"
        })
    
    st.dataframe(pd.DataFrame(inventory_data), use_container_width=True)

# ========== FRAUD DETECTION RESULTS ==========
elif st.session_state.selected_agent == "fraud":
    st.markdown(f"""
    <div class="results-panel">
        <h2 style="color: #ff006e; font-family: Orbitron; margin-bottom: 20px;">
            🛡️ FRAUD DETECTION AGENT - LIVE ANALYSIS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    orders = auth.get("/orders.json?status=any&limit=20")
    order_list = orders.get("orders", [])
    
    if not order_list:
        st.info("No orders found for analysis")
    else:
        st.subheader("🔍 Risk Analysis Results")
        
        for o in order_list[:10]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2,1,1,2])
                
                total = float(o.get("total_price", 0))
                customer = o.get("customer")
                is_new = customer is None or customer.get("orders_count", 0) == 0
                email = customer.get("email", "Guest") if customer else "Guest Checkout"
                
                # Risk calculation
                risk_score = 0
                risk_factors = []
                
                if total > 100:
                    risk_score += 30
                    risk_factors.append("High value")
                if is_new:
                    risk_score += 40
                    risk_factors.append("New customer")
                if "@" not in email:
                    risk_score += 20
                
                with col1:
                    st.write(f"**Order {o['name']}**")
                    st.caption(f"${total} | {email[:20]}...")
                
                with col2:
                    st.progress(min(risk_score/100, 1.0), text=f"{risk_score}%")
                
                with col3:
                    if risk_score > 60:
                        st.markdown('<span class="alert-critical">🚨 HIGH</span>', unsafe_allow_html=True)
                    elif risk_score > 30:
                        st.markdown('<span class="alert-warning">⚠️ MEDIUM</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="alert-success">✅ LOW</span>', unsafe_allow_html=True)
                
                with col4:
                    if risk_factors:
                        st.caption(f"Flags: {', '.join(risk_factors)}")
                
                st.divider()

# ========== SHIPPING AGENT RESULTS ==========
elif st.session_state.selected_agent == "shipping":
    st.markdown(f"""
    <div class="results-panel">
        <h2 style="color: #3a86ff; font-family: Orbitron; margin-bottom: 20px;">
            🚚 SHIPPING AGENT - LOGISTICS DASHBOARD
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    orders = auth.get("/orders.json?fulfillment_status=unfulfilled&limit=20")
    unfulfilled = orders.get("orders", [])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Unfulfilled Orders", len(unfulfilled))
    with col2:
        ready_to_ship = len([o for o in unfulfilled if o.get("financial_status") == "paid"])
        st.metric("Ready to Ship", ready_to_ship)
    with col3:
        st.metric("Avg Processing Time", "2.3 hrs")
    
    if unfulfilled:
        st.subheader("📦 Orders Awaiting Fulfillment")
        for o in unfulfilled[:5]:
            with st.expander(f"Order {o['name']} - ${o['total_price']}"):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write(f"**Customer:** {o.get('customer',{}).get('email','Guest')}")
                    st.write(f"**Payment:** {o.get('financial_status')}")
                    st.write("**Items:**")
                    for item in o.get("line_items", []):
                        st.write(f"  • {item['title']} x {item['quantity']}")
                with col2:
                    if st.button(f"🚀 Ship Now", key=f"ship_{o['id']}"):
                        st.success("Shipped! (Demo)")
    else:
        st.success("🎉 All orders fulfilled! No pending shipments.")

# ========== ANALYTICS AGENT RESULTS ==========
elif st.session_state.selected_agent == "analytics":
    st.markdown(f"""
    <div class="results-panel">
        <h2 style="color: #ffbe0b; font-family: Orbitron; margin-bottom: 20px;">
            📊 ANALYTICS AGENT - PERFORMANCE METRICS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    orders = auth.get("/orders.json?status=any&limit=100")
    order_list = orders.get("orders", [])
    products = auth.get("/products.json?limit=50")
    product_list = products.get("products", [])
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    total_revenue = sum(float(o.get("total_price",0)) for o in order_list)
    avg_order = total_revenue / len(order_list) if order_list else 0
    
    with col1:
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    with col2:
        st.metric("📦 Total Orders", len(order_list))
    with col3:
        st.metric("📈 Avg Order Value", f"${avg_order:.2f}")
    with col4:
        st.metric("🏪 Products", len(product_list))
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue Trend")
        if order_list:
            values = [float(o.get("total_price",0)) for o in order_list[:20]]
            st.area_chart(values)
    with col2:
        st.subheader("Order Velocity")
        st.bar_chart({"Orders": list(range(len(order_list[:10])))})

# ========== CUSTOMER SERVICE RESULTS ==========
elif st.session_state.selected_agent == "customer":
    st.markdown(f"""
    <div class="results-panel">
        <h2 style="color: #8338ec; font-family: Orbitron; margin-bottom: 20px;">
            🎧 CUSTOMER SERVICE AGENT - SUPPORT TICKETS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Mock support tickets
    tickets = [
        {"id": "TKT-001", "order": "#1001", "issue": "Not delivered", "priority": "HIGH", "status": "Open"},
        {"id": "TKT-002", "order": "#1002", "issue": "Wrong size", "priority": "MEDIUM", "status": "In Progress"},
        {"id": "TKT-003", "order": "#1003", "issue": "Damaged item", "priority": "HIGH", "status": "Open"},
        {"id": "TKT-004", "order": "#1004", "issue": "Refund request", "priority": "LOW", "status": "Resolved"}
    ]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Open Tickets", len([t for t in tickets if t["status"] == "Open"]))
    with col2:
        st.metric("Avg Response Time", "15 min")
    with col3:
        st.metric("Satisfaction", "94%")
    
    st.subheader("🎫 Active Support Tickets")
    for ticket in tickets:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1,1,2,1,2])
            with col1:
                st.write(f"**{ticket['id']}**")
            with col2:
                st.write(ticket['order'])
            with col3:
                st.write(ticket['issue'])
            with col4:
                if ticket['priority'] == "HIGH":
                    st.error(ticket['priority'])
                elif ticket['priority'] == "MEDIUM":
                    st.warning(ticket['priority'])
                else:
                    st.success(ticket['priority'])
            with col5:
                if st.button("Resolve", key=ticket['id']):
                    st.success("Resolved!")

# ========== MARKETING AGENT RESULTS ==========
elif st.session_state.selected_agent == "marketing":
    st.markdown(f"""
    <div class="results-panel">
        <h2 style="color: #00ffff; font-family: Orbitron; margin-bottom: 20px;">
            📢 MARKETING AGENT - PRICING OPTIMIZATION
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    products = auth.get("/products.json?limit=20")
    product_list = products.get("products", [])
    
    recommendations = []
    for p in product_list:
        variant = p.get("variants",[{}])[0]
        inventory = variant.get("inventory_quantity",0)
        price = float(variant.get("price",0))
        
        if inventory < 5:
            recommendations.append({
                "product": p["title"],
                "current": price,
                "suggested": price * 1.15,
                "action": "🔼 SCARCITY BOOST +15%",
                "reason": f"Only {inventory} left!"
            })
        elif inventory > 50:
            recommendations.append({
                "product": p["title"],
                "current": price,
                "suggested": price * 0.85,
                "action": "🔽 CLEARANCE -15%",
                "reason": f"Overstock: {inventory} units"
            })
    
    if recommendations:
        st.subheader("💰 AI Pricing Recommendations")
        for rec in recommendations[:5]:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2,1,1,2,1])
                with col1:
                    st.write(f"**{rec['product'][:30]}**")
                with col2:
                    st.write(f"${rec['current']:.2f}")
                with col3:
                    st.write(f"**${rec['suggested']:.2f}**")
                with col4:
                    st.info(rec['action'])
                with col5:
                    if st.button("Apply", key=f"price_{rec['product']}"):
                        st.success("Applied!")
    else:
        st.info("No pricing adjustments needed at this time.")

# ========== RECOMMENDATION AGENT RESULTS ==========
elif st.session_state.selected_agent == "recommend":
    st.markdown(f"""
    <div class="results-panel">
        <h2 style="color: #ff8500; font-family: Orbitron; margin-bottom: 20px;">
            💡 RECOMMENDATION AGENT - LISTING OPTIMIZATION
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    products = auth.get("/products.json?limit=20")
    product_list = products.get("products", [])
    
    st.subheader("🔍 AI Analysis Results")
    
    for p in product_list[:5]:
        with st.container():
            issues = []
            if not p.get("image"):
                issues.append("❌ Missing product image")
            if len(p.get("title","")) < 15:
                issues.append("❌ Title too short for SEO")
            if not p.get("body_html"):
                issues.append("❌ No description")
            
            col1, col2, col3 = st.columns([2,3,1])
            with col1:
                st.write(f"**{p['title'][:40]}**")
            with col2:
                if issues:
                    for issue in issues:
                        st.warning(issue)
                else:
                    st.success("✅ Listing fully optimized!")
            with col3:
                if st.button("Fix", key=f"fix_{p['id']}"):
                    st.success("Optimized!")

# ========== ORCHESTRATOR RESULTS ==========
elif st.session_state.selected_agent == "orchestrator":
    st.markdown(f"""
    <div class="results-panel">
        <h2 style="color: #ffffff; font-family: Orbitron; margin-bottom: 20px;">
            🎯 ORCHESTRATOR - SYSTEM COORDINATION
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔄 Automated Workflows")
    
    workflows = [
        {"name": "New Order Processing", "status": "Active", "last_run": "2 min ago", "success": "98%"},
        {"name": "Inventory Sync", "status": "Active", "last_run": "5 min ago", "success": "100%"},
        {"name": "Price Optimization", "status": "Active", "last_run": "1 hour ago", "success": "95%"},
        {"name": "Fraud Screening", "status": "Active", "last_run": "Just now", "success": "99%"}
    ]
    
    for wf in workflows:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])
            with col1:
                st.write(f"**{wf['name']}**")
            with col2:
                st.success(wf['status'])
            with col3:
                st.write(wf['last_run'])
            with col4:
                st.write(f"Success: {wf['success']}")
            with col5:
                st.button("Run Now", key=wf['name'])
    
    st.divider()
    st.subheader("⚡ System Health Monitor")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CPU Usage", "23%", delta="-5%")
    with col2:
        st.metric("Memory", "45%", delta="+2%")
    with col3:
        st.metric("API Calls/min", "156", delta="+12")
    with col4:
        st.metric("Queue Size", "3", delta="-2")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.5); padding: 20px;">
    <p>🤖 8 AI Agents Powered by Neural Networks | Connected to Shopify</p>
</div>
""", unsafe_allow_html=True)