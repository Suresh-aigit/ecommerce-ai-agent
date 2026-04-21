import streamlit as st
import requests

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="E-Commerce AI Agents", page_icon="🤖", layout="wide")

# 2. Global Constants
API_URL = "http://localhost:8000"

# 3. Sidebar Navigation (Consolidated to include all 8 agents + system tools)
st.sidebar.title("Navigation")
agent_type = st.sidebar.radio(
    "Select Agent",
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
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("**Project:** MCA Final Year | **Version:** 3.0.0 | **Agents:** 8 Active")

# 4. Main Title
st.title("🛒 E-Commerce AI Agent Dashboard")
st.markdown("### Autonomous AI Agent Swarm")

# --- AGENT LOGIC ---

if agent_type == "🏠 Home":
    st.header("Welcome to AI E-Commerce System")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Agents", "8")
    with col2:
        st.metric("API Status", "Online", "✅")
    with col3:
        st.metric("Version", "3.0.0")
    
    st.info("**NEW AGENTS ADDED:** Shipping & Logistics, Business Analytics")

elif agent_type == "💬 Customer Service":
    st.header("💬 Customer Service Agent")
    with st.form("customer_query_form"):
        customer_query = st.text_area("Customer Query", "Where is my order #12345?")
        customer_id = st.number_input("Customer ID", min_value=1, value=1)
        submit_button = st.form_submit_button("Process Query", type="primary")
    
    if submit_button:
        with st.spinner("🤖 AI Agent thinking..."):
            try:
                response = requests.post(f"{API_URL}/api/agent/customer-service", 
                                       json={"query": customer_query, "customer_id": customer_id})
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success("✅ Response Generated!")
                        data = result["data"]
                        st.metric("Intent", data.get("intent", "N/A"))
                        st.info(data.get("response", "No response"))
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

elif agent_type == "📦 Inventory & Pricing":
    st.header("📦 Inventory & Pricing Agent")
    task_type = st.selectbox("Select Task", ["check_stock", "update_price", "forecast_demand"])
    product_id = st.number_input("Product ID", min_value=1, value=1)
    
    if st.button("Execute Task", type="primary"):
        with st.spinner("📊 Analyzing..."):
            try:
                response = requests.post(f"{API_URL}/api/agent/inventory", 
                                       json={"task_type": task_type, "product_id": product_id})
                if response.status_code == 200:
                    st.success("✅ Analysis Complete!")
                    st.json(response.json())
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

elif agent_type == "🎯 Recommendations":
    st.header("🎯 Product Recommendation Agent")
    with st.form("recommendation_form"):
        customer_id = st.number_input("Customer ID", min_value=1, value=1)
        browsing_history = st.text_input("Recent Browsing (comma-separated)", "laptops, headphones")
        submit_button = st.form_submit_button("Generate Recommendations", type="primary")
    
    if submit_button:
        with st.spinner("🎯 Analyzing..."):
            try:
                browsing_list = [b.strip() for b in browsing_history.split(",") if b.strip()]
                response = requests.post(f"{API_URL}/api/agent/recommendations", 
                                       json={"customer_id": customer_id, "browsing_history": browsing_list})
                if response.status_code == 200:
                    st.success("✅ Recommendations Generated!")
                    st.write(response.json().get("recommendations", "No recommendations"))
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

elif agent_type == "🛡️ Fraud Detection":
    st.header("🛡️ Fraud Detection Agent")
    with st.form("fraud_form"):
        task_type = st.selectbox("Select Task", ["analyze_transaction", "risk_assessment"])
        transaction_id = st.number_input("Transaction ID", min_value=1, value=1001)
        amount = st.number_input("Amount ($)", min_value=0.0, value=150.0)
        submit_button = st.form_submit_button("Analyze", type="primary")
    
    if submit_button:
        try:
            response = requests.post(f"{API_URL}/api/agent/fraud-detection", 
                                   json={"task_type": task_type, "transaction_id": transaction_id, "amount": amount})
            if response.status_code == 200:
                result = response.json().get("analysis", {})
                col1, col2, col3 = st.columns(3)
                col1.metric("Risk Score", result.get("risk_score", 0))
                col2.metric("Risk Level", result.get("risk_level", "N/A"))
                col3.metric("Status", result.get("status", "N/A"))
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")

elif agent_type == "📢 Marketing":
    st.header("📢 Marketing Agent")
    with st.form("marketing_form"):
        task_type = st.selectbox("Select Task", ["generate_campaign", "customer_segmentation"])
        submit_button = st.form_submit_button("Execute", type="primary")
    
    if submit_button:
        try:
            response = requests.post(f"{API_URL}/api/agent/marketing", json={"task_type": task_type})
            if response.status_code == 200:
                st.json(response.json())
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")

elif agent_type == "🚚 Shipping & Logistics":
    st.header("🚚 Shipping & Logistics Agent")
    with st.form("shipping_form"):
        task_type = st.selectbox("Select Task", ["track_shipment", "estimate_delivery", "optimize_route"])
        tracking_number = st.text_input("Tracking Number", "TRK123456789")
        order_id = st.number_input("Order ID", min_value=1, value=1)
        submit_button = st.form_submit_button("Execute", type="primary")
    
    if submit_button:
        with st.spinner("🚚 Processing..."):
            try:
                response = requests.post(f"{API_URL}/api/agent/shipping", 
                                       json={"task_type": task_type, "tracking_number": tracking_number, "order_id": order_id})
                if response.status_code == 200:
                    st.success("✅ Shipping Task Complete!")
                    result = response.json()
                    if "current_status" in result:
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Status", result.get("current_status"))
                        col2.metric("Progress", f"{result.get('progress_percent', 0)}%")
                        col3.metric("ETA", result.get("estimated_delivery"))
                    st.json(result)
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

elif agent_type == "📊 Analytics":
    st.header("📊 Business Analytics Agent")
    with st.form("analytics_form"):
        task_type = st.selectbox("Select Task", ["sales_report", "predictive_forecast"])
        period = st.selectbox("Period", ["last_7_days", "last_30_days", "last_quarter"])
        submit_button = st.form_submit_button("Generate Report", type="primary")
    
    if submit_button:
        with st.spinner("📊 Analyzing..."):
            try:
                response = requests.post(f"{API_URL}/api/agent/analytics", json={"task_type": task_type, "period": period})
                if response.status_code == 200:
                    result = response.json()
                    if "summary" in result:
                        summary = result["summary"]
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Revenue", f"${summary.get('total_revenue', 0):,.0f}")
                        c2.metric("Orders", summary.get('total_orders', 0))
                        c3.metric("Growth", summary.get('growth_vs_last_period', '0%'))
                    st.json(result)
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

elif agent_type == "📜 Conversation History":
    st.header("📜 Conversation History")
    customer_id = st.number_input("Customer ID", min_value=1, value=1)
    if st.button("View History"):
        try:
            response = requests.get(f"{API_URL}/api/conversations/{customer_id}")
            if response.status_code == 200:
                st.json(response.json())
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif agent_type == "🔍 System Status":
    st.header("🔍 System Health Check")
    if st.button("Refresh Status"):
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                st.success("✅ All Systems Operational")
                st.json(response.json())
        except Exception as e:
            st.error(f"Cannot connect to backend: {str(e)}")