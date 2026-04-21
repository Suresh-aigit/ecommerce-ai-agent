import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

st.set_page_config(page_title='AI Agents Control Center', page_icon='🤖', layout='wide')

st.title('🤖 AI Agents Control Center')
st.write('Dashboard is working!')

col1, col2, col3 = st.columns(3)
col1.metric('Products', '20', '+5')
col2.metric('Orders', '15', '+3')
col3.metric('Revenue', ',200', '+12%')

data = pd.DataFrame({'x': range(10), 'y': [random.randint(10,100) for _ in range(10)]})
fig = px.line(data, x='x', y='y')
st.plotly_chart(fig)

st.success('Dashboard is running successfully!')
