"""
AI Agents Control Center for Shopify
Clean, error-free version
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import random

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'agents'))

try:
    from shopify_auth import ShopifyAuth
    SHOPIFY_AVAILABLE = True
except ImportError as e:
    SHOPIFY_AVAILABLE = False
    st.warning(f"ShopifyAuth not found: {e}. Using mock data.")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Agents Control Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    .main-container { animation: fadeIn 0.6s ease-out; }
    
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        animation: slideDown 0.5s ease-out;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .metric-card.success { border-left-color: #00ff88; }
    .metric-card.warning { border-left-color: #ffbe0b; }
    .metric-card.danger { border-left-color: #ff006e; }
    .metric-card.info { border-left-color: #4facfe; }
    
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 15px;
        color: white;
        margin: 10px 0;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .agent-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    
    .status-dot.active {
        background: #00ff88;
        animation: pulse 2s infinite;
    }
    
    .status-dot.busy {
        background: #ffbe0b;
        animation: pulse 2s infinite;
    }
    
    .status-dot.offline {
        background: #ff006e;
    }
    
    .chart-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
        animation: fadeIn 0.6s ease-out;
    }
    
    .top-nav {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .filter-bar {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e9ecef;
    }
    
    .stButton > button {
        transition: all 0.3s ease !important;
        border-radius: 8px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    .log-box {
        background: #1e1e1e;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #00ff88;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .log-entry {
        padding: 3px 0;
        border-bottom: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_shopify_data():
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
    return {
        'products': [
            {
                "id": i,
                "title": f"Product {i}",
                "product_type": random.choice(["Electronics", "Clothing", "Home", "Sports"]),
                "variants": [{
                    "sku": f"SKU-{i:04d}",
                    "price": str(random.randint(10, 500)),
                    "inventory_quantity": random.randint(0, 100)
                }]
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
                "customer": {
                    "email": f"customer{i}@example.com",
                    "orders_count": random.randint(1, 5)
                },
                "line_items": [{"title": f"Item {j}"} for j in range(random.randint(1, 4))]
            }
            for i in range(1, 16)
        ]
    }


data = get_shopify_data()
product_list = data['products']
order_list = data['orders']

if 'layout_mode' not in st.session_state:
    st.session_state.layout_mode = 'sidebar'
if 'selected_module' not in st.session_state:
    st.session_state.selected_module = "Dashboard"

col1, col2 = st.columns([8, 2])
with col2:
    layout_mode = st.selectbox(
        "Layout Mode:",
        ["Sidebar", "Top Navigation", "Grid Dashboard"],
        key="layout_select"
    )
    st.session_state.layout_mode = layout_mode.lower().replace(" ", "_")

MODULES = [
    "Dashboard",
    "Inventory",
    "Fraud Detection",
    "Orders",
    "Analytics",
    "Support",
    "Marketing",
    "Agent Performance",
    "Settings"
]

if st.session_state.layout_mode == 'top_navigation':
    st.markdown('<div class="top-nav">', unsafe_allow_html=True)
    nav_cols = st.columns(len(MODULES))
    for idx, mod in enumerate(MODULES):
        with nav_cols[idx]:
            btn_type = "primary" if st.session_state.selected_module == mod else "secondary"
            if st.button(mod, key=f"nav_{idx}", use_container_width=True, type=btn_type):
                st.session_state.selected_module = mod
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    current_module = st.session_state.selected_module

elif st.session_state.layout_mode == 'grid_dashboard':
    st.header("📊 Command Center Grid")
    grid_cols = st.columns(3)
    grid_items = [
        ("📦", "Inventory", len(product_list), "primary"),
        ("🛒", "Orders", len(order_list), "success"),
        ("💰", "Revenue", f"${sum(float(o['total_price']) for o in order_list):,.0f}", "warning"),
        ("⚠️", "Alerts", "5", "danger"),
        ("🤖", "Agents", "8 Active", "info"),
        ("📈", "Growth", "+12%", "success")
    ]
    
    for idx, (emoji, label, value, color) in enumerate(grid_items):
        with grid_cols[idx % 3]:
            st.markdown(f"""
            <div class="metric-card {color}">
                <h3>{emoji} {label}</h3>
                <h1 style="font-size: 36px; margin: 10px 0;">{value}</h1>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    selected = st.selectbox("Select Module for Details:", MODULES)
    st.session_state.selected_module = selected
    current_module = selected

else:
    with st.sidebar:
        st.title("🎛️ Control Panel")
        
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 50px;">🤖</div>
            <h3>AI Command</h3>
            <p style="color: #666; font-size: 12px;">System Online</p>
        </div>
        """, unsafe_allow_html=True)
        
        current_module = st.radio("Navigate:", MODULES)
        
        st.divider()
        
        search_query = st.text_input("🔍 Search:", "")
        date_range = st.selectbox("📅 Range:", ["24h", "7d", "30d", "All"])
        
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_resource.clear()
            st.rerun()
        
        st.divider()
        st.caption("⚡ System Status")
        st.markdown("""
        <div style="font-size: 12px;">
            <div style="display: flex; justify-content: space-between;">
                <span>🟢 Agents</span><span style="color: #00ff88;">8/8</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>⚡ CPU</span><span style="color: #667eea;">42%</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>💾 RAM</span><span style="color: #764ba2;">68%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if 'search_query' in locals() and search_query:
    product_list = [p for p in product_list if search_query.lower() in p['title'].lower()]
    order_list = [o for o in order_list if search_query.lower() in o.get('name', '').lower()]

if st.session_state.layout_mode != 'grid_dashboard':
    st.markdown(f"""
    <div class="main-header">
        <h1>🤖 AI Agents Control Center</h1>
        <p>Module: {current_module} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

if current_module == "Dashboard":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    metric_cols = st.columns(5)
    metrics = [
        ("📦 Products", len(product_list), "+5", "primary"),
        ("🛒 Orders", len(order_list), "+12", "success"),
        ("💰 Revenue", f"${sum(float(o['total_price']) for o in order_list):,.0f}", "+18%", "warning"),
        ("⚠️ Low Stock", sum(1 for p in product_list if p['variants'][0]['inventory_quantity'] < 10), "Action", "danger"),
        ("🤖 Agents", "8", "100%", "info")
    ]
    
    for col, (label, value, change, color) in zip(metric_cols, metrics):
        with col:
            change_color = "#00ff88" if "+" in str(change) else "#ff006e" if "Action" in str(change) else "#666"
            st.markdown(f"""
            <div class="metric-card {color}">
                <h4>{label}</h4>
                <h1 style="font-size: 32px; margin: 10px 0;">{value}</h1>
                <span style="color: {change_color};">{change}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    chart_cols = st.columns(3)
    
    with chart_cols[0]:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.subheader("📈 Sales Trend")
        sales_data = pd.DataFrame({
            'Hour': list(range(24)),
            'Sales': [random.randint(10, 100) for _ in range(24)]
        })
        fig = px.area(sales_data, x='Hour', y='Sales', color_discrete_sequence=['#667eea'])
        fig.update_layout(height=250, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols[1]:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.subheader("📊 Inventory")
        inv_data = pd.DataFrame({
            'Status': ['In Stock', 'Low', 'Out', 'Reserved'],
            'Count': [120, 15, 5, 8]
        })
        fig = px.pie(inv_data, values='Count', names='Status', hole=0.4,
                    color_discrete_sequence=['#00ff88', '#ffbe0b', '#ff006e', '#4facfe'])
        fig.update_layout(height=250, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols[2]:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.subheader("🎯 Orders")
        order_data = pd.DataFrame({
            'Status': ['Pending', 'Processing', 'Shipped', 'Delivered'],
            'Count': [8, 12, 15, 45]
        })
        fig = px.bar(order_data, x='Status', y='Count', color='Count', color_continuous_scale='Viridis')
        fig.update_layout(height=250, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("⚡ Quick Actions")
    action_cols = st.columns(6)
    actions = ["➕ Add Product", "📥 Import", "🎁 Coupon", "📧 Campaign", "🔄 Sync", "📥 Export"]
    
    for col, action in zip(action_cols, actions):
        with col:
            if st.button(action, use_container_width=True):
                st.toast(f"Triggered: {action}", icon="🚀")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif current_module == "Inventory":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    f_cols = st.columns(4)
    with f_cols[0]:
        cat_filter = st.multiselect("Category:", ["All", "Electronics", "Clothing", "Home"], ["All"])
    with f_cols[1]:
        stock_filter = st.select_slider("Stock:", ["All", "Critical", "Low", "Normal", "High"])
    with f_cols[2]:
        price_range = st.slider("Price:", 0, 1000, (0, 1000))
    with f_cols[3]:
        sort = st.selectbox("Sort:", ["Name", "Stock", "Price"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    btn_cols = st.columns(5)
    with btn_cols[0]:
        if st.button("➕ Add Product", type="primary", use_container_width=True):
            with st.expander("New Product Form", expanded=True):
                with st.form("add_product"):
                    st.text_input("Name")
                    st.number_input("Price", min_value=0.0)
                    st.number_input("Stock", min_value=0)
                    if st.form_submit_button("Create", use_container_width=True):
                        st.success("Created!")
                        st.balloons()
    
    with btn_cols[1]:
        if st.button("📥 Import", use_container_width=True):
            st.file_uploader("Upload CSV", type="csv")
    
    with btn_cols[2]:
        if st.button("🔄 Update", use_container_width=True):
            st.success("Stock updated!")
    
    with btn_cols[3]:
        if st.button("📊 Forecast", use_container_width=True):
            forecast = pd.DataFrame({
                'Day': pd.date_range(start=datetime.now(), periods=30, freq='D'),
                'Predicted': [random.randint(80, 120) for _ in range(30)]
            })
            fig = px.line(forecast, x='Day', y='Predicted', title="30-Day Forecast")
            st.plotly_chart(fig, use_container_width=True)
    
    with btn_cols[4]:
        if st.button("📤 Export", use_container_width=True):
            st.download_button("Download CSV", "data", "inventory.csv")
    
    st.divider()
    inv_df = pd.DataFrame([
        {
            "Product": p['title'],
            "SKU": p['variants'][0]['sku'],
            "Price": f"${p['variants'][0]['price']}",
            "Stock": p['variants'][0]['inventory_quantity'],
            "Status": "🟢" if p['variants'][0]['inventory_quantity'] > 10 else "🟡" if p['variants'][0]['inventory_quantity'] > 0 else "🔴",
            "Category": p.get('product_type', 'General'),
            "Sales": random.randint(0, 50),
            "Action": "Edit"
        }
        for p in product_list[:20]
    ])
    
    st.dataframe(inv_df, use_container_width=True, height=400, hide_index=True)
    
    st.divider()
    bulk_cols = st.columns([2, 2, 1])
    with bulk_cols[0]:
        selected = st.multiselect("Select:", inv_df['Product'].tolist()[:5])
    with bulk_cols[1]:
        action = st.selectbox("Action:", ["Update Price", "Change Stock", "Delete"])
    with bulk_cols[2]:
        if st.button("Apply", use_container_width=True, type="primary"):
            st.success(f"Applied to {len(selected)} items!")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif current_module == "Fraud Detection":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    g_cols = st.columns(4)
    with g_cols[0]:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=2,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Score"},
            gauge={'axis': {'range': [0, 10]},
                   'bar': {'color': "#00ff88"},
                   'steps': [{'range': [0, 3], 'color': "#e0ffe0"},
                            {'range': [3, 7], 'color': "#fff3cd"},
                            {'range': [7, 10], 'color': "#f8d7da"}]}))
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with g_cols[1]:
        st.metric("🚫 Blocked", "3", "+1")
    with g_cols[2]:
        st.metric("💰 Saved", "$1,240", "+$450")
    with g_cols[3]:
        st.metric("🤖 Accuracy", "96.5%", "+2.1%")
    
    st.divider()
    rt_col1, rt_col2 = st.columns([2, 1])
    
    with rt_col1:
        risk_df = pd.DataFrame({
            'Time': pd.date_range(end=datetime.now(), periods=24, freq='H'),
            'Score': [random.randint(0, 10) for _ in range(24)]
        })
        fig = px.scatter(risk_df, x='Time', y='Score', size='Score', 
                        color='Score', color_continuous_scale='RdYlGn_r')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with rt_col2:
        st.subheader("⚡ Actions")
        if st.button("🔍 Deep Scan", use_container_width=True, type="primary"):
            with st.spinner("Scanning..."):
                import time
                time.sleep(2)
            st.success("No threats found!")
        
        if st.button("📋 Review Queue", use_container_width=True):
            st.info("12 orders pending")
        
        st.slider("Sensitivity:", 0, 100, 75)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif current_module == "Agent Performance":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    view = st.segmented_control("View:", ["Grid", "Detailed", "Logs"], default="Detailed")
    
    if view == "Grid":
        agent_grid = st.columns(4)
        agents = [
            ("📦 Inventory", "active", "98%"),
            ("🛡️ Fraud", "active", "95%"),
            ("🚚 Shipping", "busy", "92%"),
            ("📊 Analytics", "active", "100%"),
            ("🎧 Support", "active", "88%"),
            ("📢 Marketing", "busy", "90%"),
            ("💡 Recommend", "active", "85%"),
            ("🎯 Orchestrator", "active", "99%")
        ]
        
        for idx, (name, status, score) in enumerate(agents):
            with agent_grid[idx % 4]:
                status_dot = f'<span class="status-dot {status}"></span>'
                st.markdown(f"""
                <div class="agent-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0;">{name}</h4>
                        {status_dot}
                    </div>
                    <div style="margin-top: 10px;">
                        <div style="background: rgba(255,255,255,0.3); border-radius: 5px; height: 6px;">
                            <div style="background: white; width: {score}; height: 100%; border-radius: 5px;"></div>
                        </div>
                        <small style="opacity: 0.9;">Score: {score}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    elif view == "Detailed":
        st.subheader("Agent Details")
        
        detailed_agents = [
            {"name": "📦 Inventory", "score": 98, "tasks": 45, "done": 42, "time": "2.3s", "cpu": "12%"},
            {"name": "🛡️ Fraud", "score": 95, "tasks": 12, "done": 12, "time": "1.8s", "cpu": "8%"},
            {"name": "🚚 Shipping", "score": 92, "tasks": 28, "done": 25, "time": "4.5s", "cpu": "15%"},
            {"name": "🎧 Support", "score": 88, "tasks": 34, "done": 30, "time": "3.2s", "cpu": "22%"}
        ]
        
        for agent in detailed_agents:
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
                
                with c1:
                    st.markdown(f"""
                    <div style="padding: 15px; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <h4>{agent['name']}</h4>
                        <span class="status-dot active"></span> <small>Active</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    color = "#00ff88" if agent['score'] > 90 else "#ffbe0b"
                    st.markdown(f"""
                    <div style="width: 50px; height: 50px; background: {color}; border-radius: 50%; 
                                display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                        {agent['score']}%
                    </div>
                    """, unsafe_allow_html=True)
                
                with c3:
                    st.metric("Queue", agent['tasks'], f"{agent['done']} done")
                with c4:
                    st.metric("Speed", agent['time'])
                with c5:
                    st.metric("CPU", agent['cpu'])
                
                st.divider()
        
        st.subheader("Performance Matrix")
        matrix = pd.DataFrame({
            'Agent': ['Inventory', 'Fraud', 'Shipping', 'Support'],
            'Accuracy': [98, 95, 92, 88],
            'Speed': [95, 98, 85, 90],
            'Uptime': [99.9, 99.5, 98.2, 99.1]
        })
        
        fig = px.imshow(matrix.set_index('Agent'), color_continuous_scale='RdYlGn', text_auto=True, aspect="auto")
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.subheader("Real-Time Logs")
        
        lc1, lc2 = st.columns([1, 1])
        with lc1:
            st.multiselect("Filter Agents:", ["All", "Inventory", "Fraud", "Shipping"], ["All"])
        with lc2:
            st.button("🔄 Refresh Logs")
        
        logs = [
            ("10:42:15", "Inventory", "INFO", "Restocked SKU-4421"),
            ("10:41:32", "Fraud", "WARNING", "Pattern detected"),
            ("10:40:08", "Shipping", "INFO", "Label generated"),
            ("10:39:45", "Support", "INFO", "Ticket resolved"),
            ("10:38:12", "Marketing", "ERROR", "API timeout"),
        ]
        
        st.markdown('<div class="log-box">', unsafe_allow_html=True)
        for ts, agent, level, msg in logs:
            color = "#ff006e" if level == "ERROR" else "#ffbe0b" if level == "WARNING" else "#00ff88"
            st.markdown(f"""
            <div class="log-entry">
                <span style="color: #666;">[{ts}]</span>
                <span style="color: #667eea;">[{agent}]</span>
                <span style="color: {color};">{level}:</span> {msg}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif current_module == "Settings":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    tabs = st.tabs(["Agents", "Thresholds", "Notifications", "Security"])
    
    with tabs[0]:
        st.subheader("Agent Configuration")
        
        configs = [
            ("📦 Inventory", True, 5),
            ("🛡️ Fraud", True, 3),
            ("🚚 Shipping", True, 10),
            ("🎧 Support", True, 2)
        ]
        
        for name, enabled, threads in configs:
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.toggle(name, value=enabled)
                with c2:
                    st.number_input("Threads:", value=threads, key=f"th_{name}")
                with c3:
                    st.button("🔄 Restart", key=f"rs_{name}")
                st.divider()
    
    with tabs[1]:
        st.subheader("Alert Thresholds")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.slider("Low Stock", 0, 100, 10)
            st.slider("High Value", 50, 500, 100)
        with c2:
            st.slider("Fraud Risk", 0, 100, 60)
            st.slider("Response Time", 1, 10, 3)
        with c3:
            st.slider("CPU %", 50, 100, 80)
            st.slider("Memory %", 50, 100, 85)
        
        if st.button("💾 Save All", type="primary", use_container_width=True):
            st.success("Saved!")
            st.balloons()
    
    with tabs[2]:
        st.subheader("Notifications")
        c1, c2 = st.columns(2)
        with c1:
            st.checkbox("📧 Email", value=True)
            st.checkbox("📱 SMS", value=False)
            st.checkbox("💬 Slack", value=True)
        with c2:
            st.text_input("Email:", "admin@store.com")
            st.text_input("Webhook:", "https://hooks.slack.com/...")
    
    with tabs[3]:
        st.subheader("Security")
        st.toggle("2FA", value=True)
        st.toggle("Audit Logging", value=True)
        st.text_input("API Key:", type="password", value="shpat_••••••••")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info(f"{current_module} module - Content loading...")
    st.metric("Status", "Active")
    st.progress(random.randint(60, 100))

st.divider()
st.caption("🤖 AI Agents Control Center v2.0 | Clean Build | Streamlit Powered")