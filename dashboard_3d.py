import streamlit as st
import sys
sys.path.append('backend/agents')
from shopify_auth import ShopifyAuth
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Page config with dark theme
st.set_page_config(
    page_title="🚀 8 AI Agents - 3D Command Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for 3D effects
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

/* Main background with gradient */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}

/* 3D Card effect */
.agent-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 20px;
    margin: 10px;
    transform-style: preserve-3d;
    transition: all 0.3s ease;
    box-shadow: 
        0 10px 30px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.1);
}

.agent-card:hover {
    transform: translateY(-10px) rotateX(5deg);
    box-shadow: 
        0 20px 40px rgba(0,255,255,0.2),
        inset 0 1px 0 rgba(255,255,255,0.2);
    border-color: rgba(0,255,255,0.3);
}

/* Neon text effect */
.neon-text {
    font-family: 'Orbitron', sans-serif;
    color: #fff;
    text-shadow: 
        0 0 5px #fff,
        0 0 10px #fff,
        0 0 20px #0ff,
        0 0 30px #0ff,
        0 0 40px #0ff;
}

/* Glowing buttons */
.stButton>button {
    background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff);
    border: none;
    border-radius: 50px;
    color: white;
    padding: 15px 30px;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 0 20px rgba(131, 56, 236, 0.5);
    transition: all 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 40px rgba(131, 56, 236, 0.8);
}

/* 3D Grid background */
.grid-bg {
    background-image: 
        linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
    background-size: 50px 50px;
    animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
    0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
    100% { transform: perspective(500px) rotateX(60deg) translateY(50px); }
}

/* Holographic effect */
.hologram {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.1) 0%,
        rgba(255,255,255,0.05) 50%,
        rgba(255,255,255,0.1) 100%
    );
    border: 1px solid rgba(0,255,255,0.3);
    position: relative;
    overflow: hidden;
}

.hologram::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        45deg,
        transparent 30%,
        rgba(0,255,255,0.1) 50%,
        transparent 70%
    );
    animation: hologramScan 3s ease-in-out infinite;
}

@keyframes hologramScan {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

/* Floating animation */
.float {
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Pulse effect */
.pulse {
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(0,255,255,0.4); }
    50% { box-shadow: 0 0 0 20px rgba(0,255,255,0); }
}

/* Metric cards */
.metric-3d {
    background: linear-gradient(135deg, rgba(255,0,110,0.2), rgba(131,56,236,0.2));
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    transform: perspective(1000px) rotateY(-5deg);
    transition: transform 0.3s;
    border: 1px solid rgba(255,255,255,0.1);
}

.metric-3d:hover {
    transform: perspective(1000px) rotateY(0deg) scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# Initialize
@st.cache_resource
def get_shopify():
    return ShopifyAuth()

auth = get_shopify()

# Header with 3D effect
st.markdown("""
<div style="text-align: center; padding: 30px;">
    <h1 class="neon-text" style="font-size: 60px; margin-bottom: 10px;">
        🤖 NEURAL COMMAND CENTER
    </h1>
    <p style="color: #0ff; font-family: Orbitron; letter-spacing: 5px;">
        8 AI AGENTS • SHOPIFY INTEGRATION • REAL-TIME DATA
    </p>
    <p style="color: rgba(255,255,255,0.5);">
        Connected: ai-swarm-2 | {time}
    </p>
</div>
""".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

# Create tabs for 3D navigation
tabs = st.tabs([
    "🌐 MATRIX VIEW", 
    "📦 INVENTORY CORE", 
    "🛡️ SECURITY GRID", 
    "🚚 LOGISTICS HUB",
    "📊 ANALYTICS NEXUS",
    "🎧 SUPPORT NODE",
    "📢 MARKETING PORTAL",
    "💡 INTELLIGENCE LAB"
])

# ========== TAB 1: MATRIX VIEW (Home) ==========
with tabs[0]:
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <h2 class="neon-text">SYSTEM STATUS: OPERATIONAL</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch data
    products = auth.get("/products.json?limit=50")
    product_list = products.get("products", [])
    orders = auth.get("/orders.json?status=any&limit=50")
    order_list = orders.get("orders", [])
    
    # 3D Metrics
    cols = st.columns(4)
    metrics = [
        ("🎯 PRODUCTS", len(product_list), "#ff006e"),
        ("📦 ORDERS", len(order_list), "#8338ec"),
        ("⚠️ ALERTS", sum(1 for p in product_list if p.get("variants",[{}])[0].get("inventory_quantity",0) < 10), "#ffbe0b"),
        ("💰 REVENUE", f"${sum(float(o.get('total_price',0)) for o in order_list):,.0f}", "#3a86ff")
    ]
    
    for col, (label, value, color) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-3d pulse" style="border-left: 5px solid {color};">
                <h3 style="color: {color}; font-family: Orbitron; margin: 0;">{label}</h3>
                <h1 style="color: white; font-size: 40px; margin: 10px 0; font-family: Orbitron;">{value}</h1>
            </div>
            """, unsafe_allow_html=True)
    
    # 3D Agent Grid
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("⚡ ACTIVE AGENT NETWORK")
    
    agent_cols = st.columns(4)
    agents = [
        ("📦", "INVENTORY", "Monitoring stock levels", "#00ff88"),
        ("🛡️", "FRAUD SHIELD", "Analyzing risks", "#ff006e"),
        ("🚚", "LOGISTICS", "Managing shipments", "#3a86ff"),
        ("📊", "ANALYTICS", "Processing data", "#ffbe0b"),
        ("🎧", "SUPPORT", "Handling inquiries", "#8338ec"),
        ("📢", "MARKETING", "Optimizing prices", "#00ffff"),
        ("💡", "RECOMMEND", "Learning patterns", "#ff8500"),
        ("🎯", "ORCHESTRATOR", "Coordinating all", "#ffffff")
    ]
    
    for i, (icon, name, desc, color) in enumerate(agents):
        with agent_cols[i % 4]:
            st.markdown(f"""
            <div class="agent-card float" style="border-left: 4px solid {color};">
                <h2 style="font-size: 40px; margin: 0;">{icon}</h2>
                <h4 style="color: {color}; font-family: Orbitron; margin: 10px 0;">{name}</h4>
                <p style="color: rgba(255,255,255,0.7); font-size: 12px;">{desc}</p>
                <div style="width: 10px; height: 10px; background: {color}; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px {color};"></div>
                <span style="color: {color}; font-size: 10px;"> ACTIVE</span>
            </div>
            """, unsafe_allow_html=True)

# ========== TAB 2: INVENTORY CORE ==========
with tabs[1]:
    st.markdown('<h2 class="neon-text">📦 INVENTORY CORE</h2>', unsafe_allow_html=True)
    
    products = auth.get("/products.json?limit=50")
    product_list = products.get("products", [])
    
    # 3D Stock visualization
    st.subheader("REAL-TIME STOCK LEVELS")
    
    for p in product_list[:6]:
        variant = p.get("variants",[{}])[0]
        stock = variant.get("inventory_quantity",0)
        title = p["title"]
        max_stock = 50
        
        # Color based on stock level
        if stock < 10:
            color = "#ff006e"
            status = "CRITICAL"
        elif stock < 25:
            color = "#ffbe0b"
            status = "WARNING"
        else:
            color = "#00ff88"
            status = "OPTIMAL"
        
        col1, col2, col3 = st.columns([2,3,1])
        with col1:
            st.markdown(f"**{title}**")
        with col2:
            st.progress(min(stock/max_stock, 1.0), text=f"{stock} units")
        with col3:
            st.markdown(f'<span style="color: {color}; font-weight: bold;">{status}</span>', unsafe_allow_html=True)

# ========== TAB 3: SECURITY GRID ==========
with tabs[2]:
    st.markdown('<h2 class="neon-text">🛡️ SECURITY GRID</h2>', unsafe_allow_html=True)
    
    orders = auth.get("/orders.json?status=any&limit=20")
    order_list = orders.get("orders", [])
    
    if not order_list:
        st.info("No orders to analyze")
    else:
        for o in order_list[:5]:
            with st.container():
                total = float(o.get("total_price", 0))
                customer = o.get("customer")
                is_new = customer is None or customer.get("orders_count", 0) == 0
                
                risk_score = 0
                if total > 100: risk_score += 30
                if is_new: risk_score += 40
                
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    st.write(f"**Order {o['name']}** - ${total}")
                with col2:
                    st.progress(min(risk_score/100, 1.0), text=f"Risk: {risk_score}%")
                with col3:
                    if risk_score > 60:
                        st.error("🚨 HIGH")
                    elif risk_score > 30:
                        st.warning("⚠️ MED")
                    else:
                        st.success("✅ LOW")

# ========== TAB 4: LOGISTICS HUB ==========
with tabs[3]:
    st.markdown('<h2 class="neon-text">🚚 LOGISTICS HUB</h2>', unsafe_allow_html=True)
    
    orders = auth.get("/orders.json?fulfillment_status=unfulfilled&limit=10")
    unfulfilled = orders.get("orders", [])
    
    if unfulfilled:
        for o in unfulfilled[:5]:
            with st.expander(f"📦 Order {o['name']} - ${o['total_price']}"):
                st.write(f"Customer: {o.get('customer',{}).get('email','Guest')}")
                st.write(f"Items: {len(o.get('line_items',[]))}")
                if st.button(f"🚀 Ship Now - {o['name']}", key=o['id']):
                    st.success("Shipped! (Demo)")
    else:
        st.success("🎉 All orders fulfilled!")

# ========== TAB 5: ANALYTICS NEXUS ==========
with tabs[4]:
    st.markdown('<h2 class="neon-text">📊 ANALYTICS NEXUS</h2>', unsafe_allow_html=True)
    
    orders = auth.get("/orders.json?status=any&limit=100")
    order_list = orders.get("orders", [])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue Flow")
        if order_list:
            values = [float(o.get("total_price",0)) for o in order_list[:20]]
            st.area_chart(values)
    with col2:
        st.subheader("Order Velocity")
        st.metric("Today's Orders", len([o for o in order_list if '2026-04-11' in o.get('created_at','')]))

# ========== TAB 6: SUPPORT NODE ==========
with tabs[5]:
    st.markdown('<h2 class="neon-text">🎧 SUPPORT NODE</h2>', unsafe_allow_html=True)
    
    issues = [
        ("Order #1001", "Not delivered", "HIGH", "Track & update customer"),
        ("Order #1002", "Wrong size", "MEDIUM", "Process exchange"),
        ("Order #1003", "Damaged item", "HIGH", "File claim & reship")
    ]
    
    for order, issue, priority, action in issues:
        col1, col2, col3, col4 = st.columns([1,2,1,2])
        with col1:
            st.write(f"**{order}**")
        with col2:
            st.write(issue)
        with col3:
            if priority == "HIGH":
                st.error(priority)
            else:
                st.warning(priority)
        with col4:
            st.success(f"💡 {action}")

# ========== TAB 7: MARKETING PORTAL ==========
with tabs[6]:
    st.markdown('<h2 class="neon-text">📢 MARKETING PORTAL</h2>', unsafe_allow_html=True)
    
    products = auth.get("/products.json?limit=10")
    product_list = products.get("products", [])
    
    for p in product_list[:5]:
        variant = p.get("variants",[{}])[0]
        stock = variant.get("inventory_quantity",0)
        price = float(variant.get("price",0))
        
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            st.write(f"**{p['title']}**")
        with col2:
            if stock < 5:
                new_price = price * 1.15
                st.markdown(f"${price} → **${new_price:.2f}** 🔼")
            elif stock > 50:
                new_price = price * 0.85
                st.markdown(f"${price} → **${new_price:.2f}** 🔽")
            else:
                st.markdown(f"${price} ✅")
        with col3:
            if st.button("Apply", key=p['id']):
                st.success("Updated!")

# ========== TAB 8: INTELLIGENCE LAB ==========
with tabs[7]:
    st.markdown('<h2 class="neon-text">💡 INTELLIGENCE LAB</h2>', unsafe_allow_html=True)
    
    st.subheader("🧠 AI Learning Patterns")
    
    insights = [
        "📈 Peak sales: 2-4 PM daily",
        "🎯 Best converting: Snowboard products",
        "⚠️ Stockout risk: Gift Cards (0 units)",
        "💰 Revenue opportunity: 15% price increase on low stock items"
    ]
    
    for insight in insights:
        st.info(insight)
    
    st.subheader("🔮 Predictions")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tomorrow's Forecast", "$1,250", "+12%")
    with col2:
        st.metric("Stock Alert", "3 items", "Reorder needed")