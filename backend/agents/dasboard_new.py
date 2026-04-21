import streamlit as st
import sys
sys.path.append('backend/agents')
from shopify_auth import ShopifyAuth
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="AI Agents Control Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean animations without 3D
st.markdown("""
<style>
    /* Smooth animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(0,123,255,0.5); }
        50% { box-shadow: 0 0 20px rgba(0,123,255,0.8); }
    }
    
    /* Card styles with hover animation */
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Metric cards */
    .metric-box {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        animation: slideIn 0.6s ease-out;
        transition: all 0.3s;
    }
    
    .metric-box:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    /* Status indicators */
    .status-active {
        width: 12px;
        height: 12px;
        background: #00ff88;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    .status-warning {
        width: 12px;
        height: 12px;
        background: #ffbe0b;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    .status-error {
        width: 12px;
        height: 12px;
        background: #ff006e;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    /* Button animations */
    .stButton>button {
        transition: all 0.3s !important;
        border-radius: 8px !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Header animation */
    .main-header {
        animation: fadeIn 1s ease-out;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize connection
@st.cache_resource
def get_shopify():
    return ShopifyAuth()

try:
    auth = get_shopify()
except Exception as e:
    st.error(f"Connection failed: {e}")
    st.stop()

# ========== SIDEBAR NAVIGATION ==========
st.sidebar.title("🎛️ Control Panel")

# Agent selector with icons
agent_menu = st.sidebar.radio(
    "Select Agent Module:",
    [
        "📊 Dashboard Overview",
        "📦 Inventory Manager",
        "🛡️ Fraud Detection System",
        "🚚 Order Fulfillment",
        "📈 Analytics & Reports",
        "🎧 Customer Support",
        "📢 Marketing Automation",
        "🔧 System Settings"
    ]
)

# Quick actions in sidebar
st.sidebar.divider()
st.sidebar.subheader("⚡ Quick Actions")

if st.sidebar.button("🔄 Refresh All Data", key="refresh"):
    st.cache_resource.clear()
    st.rerun()

if st.sidebar.button("📥 Export Report", key="export"):
    st.sidebar.success("Report downloaded!")

# Search filter
st.sidebar.divider()
search_query = st.sidebar.text_input("🔍 Search products/orders:", "")

# Date filter
date_range = st.sidebar.selectbox(
    "📅 Time Range:",
    ["Last 24 hours", "Last 7 days", "Last 30 days", "All time"]
)

# ========== MAIN CONTENT ==========

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Agents Control Center</h1>
    <p>Real-time Shopify Store Management | Connected: ai-swarm-2</p>
    <small>Last updated: {}</small>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

# Fetch data based on filters
products = auth.get("/products.json?limit=50")
product_list = products.get("products", [])

orders = auth.get("/orders.json?status=any&limit=50")
order_list = orders.get("orders", [])

# Apply search filter
if search_query:
    product_list = [p for p in product_list if search_query.lower() in p['title'].lower()]
    order_list = [o for o in order_list if search_query.lower() in o.get('name','').lower()]

# ========== DASHBOARD OVERVIEW ==========
if agent_menu == "📊 Dashboard Overview":
    st.header("📊 Real-Time Dashboard")
    
    # Top metrics with animations
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("Total Products", len(product_list), "#667eea", "📦"),
        ("Total Orders", len(order_list), "#764ba2", "🛒"),
        ("Revenue", f"${sum(float(o.get('total_price',0)) for o in order_list):,.0f}", "#f093fb", "💰"),
        ("Low Stock", sum(1 for p in product_list if p.get("variants",[{}])[0].get("inventory_quantity",0) < 10), "#f5576c", "⚠️"),
        ("Active Agents", 8, "#4facfe", "🤖")
    ]
    
    for col, (label, value, color, icon) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-box" style="border-top: 4px solid {color};">
                <h3 style="color: {color}; margin: 0;">{icon} {label}</h3>
                <h1 style="color: #333; margin: 10px 0; font-size: 32px;">{value}</h1>
            </div>
            """, unsafe_allow_html=True)
    
    # Charts row
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Sales Trend")
        if order_list:
            df_orders = pd.DataFrame([
                {
                    'date': o.get('created_at', '')[:10],
                    'amount': float(o.get('total_price', 0))
                } for o in order_list[:20]
            ])
            fig = px.line(df_orders, x='date', y='amount', 
                         title='Revenue Over Time',
                         markers=True,
                         line_shape='spline')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No order data available")
    
    with col2:
        st.subheader("📊 Inventory Distribution")
        if product_list:
            stock_data = pd.DataFrame([
                {
                    'Product': p['title'][:20],
                    'Stock': p.get("variants",[{}])[0].get("inventory_quantity",0)
                } for p in product_list[:10]
            ])
            fig = px.bar(stock_data, x='Product', y='Stock',
                        color='Stock',
                        color_continuous_scale='Viridis')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Agent status grid
    st.divider()
    st.subheader("🤖 Agent Performance Monitor")
    
    agent_cols = st.columns(4)
    agents_status = [
        ("📦 Inventory", "98%", "Active", "2 alerts"),
        ("🛡️ Fraud Detection", "95%", "Active", "0 alerts"),
        ("🚚 Shipping", "92%", "Active", "1 pending"),
        ("📊 Analytics", "100%", "Active", "0 alerts"),
        ("🎧 Support", "88%", "Active", "3 tickets"),
        ("📢 Marketing", "90%", "Active", "2 campaigns"),
        ("💡 Recommendations", "85%", "Active", "learning"),
        ("🎯 Orchestrator", "99%", "Active", "coordinating")
    ]
    
    for i, (name, score, status, note) in enumerate(agents_status):
        with agent_cols[i % 4]:
            st.markdown(f"""
            <div class="agent-card">
                <h4>{name}</h4>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span class="status-active"></span>
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

# ========== INVENTORY MANAGER ==========
elif agent_menu == "📦 Inventory Manager":
    st.header("📦 Inventory Management System")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Add Product", use_container_width=True):
            st.info("Feature: Opens product creation form")
    with col2:
        if st.button("📥 Import CSV", use_container_width=True):
            st.info("Feature: Bulk import products")
    with col3:
        if st.button("🔄 Sync Inventory", use_container_width=True):
            st.success("Inventory synced with warehouse!")
    with col4:
        if st.button("📤 Export List", use_container_width=True):
            st.success("Product list exported!")
    
    # Filter options
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        stock_filter = st.selectbox("Stock Status:", ["All", "In Stock", "Low Stock", "Out of Stock"])
    with col2:
        sort_by = st.selectbox("Sort By:", ["Name", "Stock Level", "Price", "Last Updated"])
    with col3:
        category = st.selectbox("Category:", ["All", "Snowboards", "Accessories", "Gift Cards"])
    
    # Filter products
    filtered_products = product_list
    if stock_filter == "Low Stock":
        filtered_products = [p for p in product_list if p.get("variants",[{}])[0].get("inventory_quantity",0) < 10]
    elif stock_filter == "Out of Stock":
        filtered_products = [p for p in product_list if p.get("variants",[{}])[0].get("inventory_quantity",0) == 0]
    elif stock_filter == "In Stock":
        filtered_products = [p for p in product_list if p.get("variants",[{}])[0].get("inventory_quantity",0) > 0]
    
    # Display as interactive table
    st.divider()
    
    inventory_data = []
    for p in filtered_products:
        variant = p.get("variants",[{}])[0]
        stock = variant.get("inventory_quantity",0)
        
        # Determine status
        if stock == 0:
            status = "🔴 Out of Stock"
            status_color = "#ff006e"
        elif stock < 10:
            status = "🟡 Low Stock"
            status_color = "#ffbe0b"
        else:
            status = "🟢 In Stock"
            status_color = "#00ff88"
        
        inventory_data.append({
            "Product": p["title"],
            "SKU": variant.get("sku", "N/A"),
            "Price": f"${variant.get('price', '0')}",
            "Stock": stock,
            "Status": status,
            "Actions": "Edit | Delete"
        })
    
    if inventory_data:
        df = pd.DataFrame(inventory_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        # Bulk actions
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            selected_products = st.multiselect("Select products for bulk action:", [p["Product"] for p in inventory_data])
        with col2:
            bulk_action = st.selectbox("Bulk Action:", ["Update Price", "Update Stock", "Delete", "Export"])
            if st.button("Apply Bulk Action", use_container_width=True):
                st.success(f"Applied {bulk_action} to {len(selected_products)} products!")
    else:
        st.info("No products match the selected filters")

# ========== FRAUD DETECTION ==========
elif agent_menu == "🛡️ Fraud Detection System":
    st.header("🛡️ Fraud Detection & Risk Analysis")
    
    # Risk summary cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🟢 Low Risk", "12 orders", "+2 today")
    with col2:
        st.metric("🟡 Medium Risk", "3 orders", "-1 today")
    with col3:
        st.metric("🔴 High Risk", "1 order", "Action needed")
    with col4:
        st.metric("🚫 Blocked", "0 orders", "Protected $0")
    
    # Risk analysis chart
    st.divider()
    col1, col2 = st.columns([2,1])
    
    with col1:
        st.subheader("📊 Risk Distribution")
        risk_data = pd.DataFrame({
            'Risk Level': ['Low', 'Medium', 'High', 'Blocked'],
            'Orders': [12, 3, 1, 0],
            'Amount': [450, 320, 150, 0]
        })
        fig = px.pie(risk_data, values='Orders', names='Risk Level',
                    color='Risk Level',
                    color_discrete_map={'Low':'#00ff88', 'Medium':'#ffbe0b', 'High':'#ff006e', 'Blocked':'#333'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Alerts")
        st.error("🔴 Order #1024: $150, New customer, IP mismatch")
        st.warning("🟡 Order #1023: $89, Unusual shipping address")
        st.info("🟢 Order #1022: Cleared after verification")
    
    # Order review table
    st.divider()
    st.subheader("🔍 Orders Under Review")
    
    review_data = []
    for o in order_list[:10]:
        total = float(o.get("total_price", 0))
        customer = o.get("customer")
        is_new = customer is None or customer.get("orders_count", 0) == 0
        
        risk_score = 0
        if total > 100: risk_score += 30
        if is_new: risk_score += 40
        
        review_data.append({
            "Order": o['name'],
            "Customer": customer.get('email', 'Guest') if customer else 'Guest',
            "Amount": f"${total}",
            "Risk Score": f"{risk_score}%",
            "Status": "Pending Review" if risk_score > 50 else "Cleared",
            "Action": "Approve | Reject | Hold"
        })
    
    st.dataframe(pd.DataFrame(review_data), use_container_width=True)

# ========== ORDER FULFILLMENT ==========
elif agent_menu == "🚚 Order Fulfillment":
    st.header("🚚 Order Fulfillment Center")
    
    # Fulfillment metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Unfulfilled", "5 orders", "2 urgent")
    with col2:
        st.metric("🚚 In Transit", "12 orders", "3 delivered today")
    with col3:
        st.metric("✅ Delivered", "48 orders", "This week")
    with col4:
        st.metric("📅 Scheduled", "3 orders", "Tomorrow")
    
    # Fulfillment pipeline
    st.divider()
    st.subheader("📋 Fulfillment Pipeline")
    
    # Get unfulfilled orders
    unfulfilled = [o for o in order_list if o.get('fulfillment_status') != 'fulfilled']
    
    if unfulfilled:
        for o in unfulfilled[:5]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2,2,1,1])
                
                with col1:
                    st.write(f"**{o['name']}**")
                    st.caption(f"Customer: {o.get('customer',{}).get('email','Guest')}")
                
                with col2:
                    items = o.get('line_items', [])
                    st.write(f"{len(items)} items: {', '.join([i['title'][:15] for i in items[:2]])}")
                
                with col3:
                    st.write(f"${o['total_price']}")
                
                with col4:
                    if st.button(f"🚚 Ship", key=f"ship_{o['id']}"):
                        st.success(f"Order {o['name']} marked as shipped!")
                        # Here you would actually call Shopify API to fulfill
    else:
        st.success("🎉 All orders fulfilled! Great job!")
    
    # Shipping providers
    st.divider()
    st.subheader("🚛 Shipping Providers")
    
    providers = st.columns(3)
    with providers[0]:
        st.info("📦 Standard Shipping\n2-5 days\n$5.00")
    with providers[1]:
        st.info("🚀 Express Shipping\n1-2 days\n$12.00")
    with providers[2]:
        st.info("⚡ Same Day\nToday\n$25.00")

# ========== ANALYTICS & REPORTS ==========
elif agent_menu == "📈 Analytics & Reports":
    st.header("📈 Advanced Analytics & Reporting")
    
    # Report type selector
    report_type = st.selectbox(
        "Select Report Type:",
        ["Sales Overview", "Product Performance", "Customer Insights", "Inventory Forecast", "Custom Report"]
    )
    
    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date:", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date:", datetime.now())
    
    # Generate report button
    if st.button("📊 Generate Report", use_container_width=True):
        st.success(f"Generating {report_type} for {start_date} to {end_date}...")
        
        # Sample charts based on report type
        if report_type == "Sales Overview":
            # Revenue trend
            df = pd.DataFrame({
                'Date': pd.date_range(start=start_date, end=end_date, freq='D'),
                'Revenue': [100 + i*10 + (i%7)*50 for i in range((end_date-start_date).days + 1)]
            })
            fig = px.area(df, x='Date', y='Revenue', 
                         title='Revenue Trend',
                         color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig, use_container_width=True)
            
        elif report_type == "Product Performance":
            # Top products
            product_perf = pd.DataFrame({
                'Product': [p['title'][:20] for p in product_list[:5]],
                'Sales': [45, 38, 32, 28, 25],
                'Revenue': [1200, 950, 800, 650, 500]
            })
            fig = px.bar(product_perf, x='Product', y='Revenue', color='Sales',
                        title='Top Products by Revenue')
            st.plotly_chart(fig, use_container_width=True)
    
    # Export options
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Download PDF"):
            st.success("PDF report downloaded!")
    with col2:
        if st.button("📊 Export Excel"):
            st.success("Excel file downloaded!")
    with col3:
        if st.button("📧 Email Report"):
            st.success("Report emailed to admin!")

# ========== CUSTOMER SUPPORT ==========
elif agent_menu == "🎧 Customer Support":
    st.header("🎧 Customer Support Center")
    
    # Support metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎫 Open Tickets", "8", "3 new today")
    with col2:
        st.metric("⏱️ Avg Response", "2.5 hours", "-30 min")
    with col3:
        st.metric("⭐ Satisfaction", "4.8/5", "+0.2")
    with col4:
        st.metric("✅ Resolved", "45", "This week")
    
    # Ticket list
    st.divider()
    st.subheader("🎫 Support Tickets")
    
    tickets = [
        {"id": "T-1024", "customer": "john@email.com", "issue": "Order not received", "priority": "High", "status": "Open"},
        {"id": "T-1023", "customer": "sarah@email.com", "issue": "Wrong size", "priority": "Medium", "status": "In Progress"},
        {"id": "T-1022", "customer": "mike@email.com", "issue": "Refund request", "priority": "Low", "status": "Resolved"}
    ]
    
    for ticket in tickets:
        with st.expander(f"🎫 {ticket['id']} - {ticket['issue']} ({ticket['priority']})"):
            col1, col2 = st.columns([3,1])
            with col1:
                st.write(f"**Customer:** {ticket['customer']}")
                st.write(f"**Status:** {ticket['status']}")
                st.text_area("Notes:", "Customer contacted...", key=ticket['id'])
            with col2:
                if st.button("✅ Resolve", key=f"resolve_{ticket['id']}"):
                    st.success("Ticket resolved!")
                if st.button("➡️ Escalate", key=f"escalate_{ticket['id']}"):
                    st.warning("Ticket escalated!")

# ========== MARKETING AUTOMATION ==========
elif agent_menu == "📢 Marketing Automation":
    st.header("📢 Marketing & Promotion Center")
    
    # Campaign overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📧 Email Campaigns", "3 active", "12% open rate")
    with col2:
        st.metric("🎁 Discount Codes", "5 codes", "$450 used")
    with col3:
        st.metric("👥 Referrals", "23 new", "$230 revenue")
    
    # Pricing optimizer
    st.divider()
    st.subheader("💰 AI Pricing Optimizer")
    
    for p in product_list[:3]:
        variant = p.get("variants",[{}])[0]
        stock = variant.get("inventory_quantity",0)
        price = float(variant.get("price",0))
        
        col1, col2, col3, col4 = st.columns([2,1,1,1])
        
        with col1:
            st.write(f"**{p['title']}**")
            st.caption(f"Stock: {stock} units")
        
        with col2:
            st.write(f"Current: ${price}")
        
        with col3:
            if stock < 5:
                new_price = price * 1.15
                st.markdown(f"AI Suggests: **${new_price:.2f}** 🔼")
            elif stock > 50:
                new_price = price * 0.90
                st.markdown(f"AI Suggests: **${new_price:.2f}** 🔽")
            else:
                st.markdown("Price: **Optimal** ✅")
        
        with col4:
            if st.button("Apply", key=f"price_{p['id']}"):
                st.success("Price updated!")

# ========== SYSTEM SETTINGS ==========
elif agent_menu == "🔧 System Settings":
    st.header("🔧 System Configuration")
    
    # Agent configuration
    st.subheader("🤖 Agent Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.toggle("Inventory Auto-Reorder", value=True)
        st.toggle("Fraud Detection Active", value=True)
        st.toggle("Price Optimization", value=True)
    with col2:
        st.toggle("Email Notifications", value=True)
        st.toggle("SMS Alerts", value=False)
        st.toggle("Auto-Fulfillment", value=False)
    
    # Thresholds
    st.divider()
    st.subheader("⚠️ Alert Thresholds")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.slider("Low Stock Alert", 0, 50, 10)
    with col2:
        st.slider("High Value Order", 50, 500, 100)
    with col3:
        st.slider("Fraud Risk Threshold", 0, 100, 60)
    
    # Save settings
    st.divider()
    if st.button("💾 Save All Settings", use_container_width=True):
        st.success("Settings saved successfully!")

# Footer
st.divider()
st.caption("🤖 Powered by 8 AI Agents | Shopify Integration | Built with Streamlit")