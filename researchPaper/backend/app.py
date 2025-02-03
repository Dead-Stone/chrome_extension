import sys
import os

# Ensure the parent directory of 'backend' is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
