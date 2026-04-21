import sys
import os

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add backend to Python path
backend_dir = os.path.join(current_dir, "backend")
sys.path.insert(0, backend_dir)

# Change to backend directory
os.chdir(backend_dir)

# Now run uvicorn
import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=False)
