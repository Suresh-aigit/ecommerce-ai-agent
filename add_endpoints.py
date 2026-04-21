from fastapi import FastAPI
import os

# Read current main.py
main_file = 'backend/api/main.py'
with open(main_file, 'r') as f:
    content = f.read()

# Check if endpoints already exist
if '/api/agent/shipping' in content:
    print('Shipping endpoint already exists!')
else:
    # Add imports if missing
    if 'from backend.agents.shipping_agent import ShippingAgent' not in content:
        # Add after other imports
        content = content.replace(
            'from backend.agents.marketing_agent import MarketingAgent',
            '''from backend.agents.marketing_agent import MarketingAgent
from backend.agents.shipping_agent import ShippingAgent
from backend.agents.analytics_agent import AnalyticsAgent'''
        )
    
    # Add endpoints before if __name__ or at end
    endpoints = '''

@app.post("/api/agent/shipping")
async def shipping_endpoint(request: dict):
    agent = ShippingAgent()
    return await agent.process(request)

@app.post("/api/agent/analytics")
async def analytics_endpoint(request: dict):
    agent = AnalyticsAgent()
    return await agent.process(request)
'''
    
    # Find a good place to add (before if __name__ or at end)
    if 'if __name__' in content:
        content = content.replace('if __name__', endpoints + '\\nif __name__')
    else:
        content += endpoints
    
    with open(main_file, 'w') as f:
        f.write(content)
    print('Added shipping and analytics endpoints!')

print('Fix complete. Restart your backend with: python run.py')
