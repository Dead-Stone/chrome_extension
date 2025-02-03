import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import neo4j_db
import multiagent  # New multiagent module

load_dotenv()

app = Flask(__name__)
CORS(app, max_age=3600)

# Get Neo4j connection settings from environment variables.
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

db = neo4j_db.Neo4jDB(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
manager_agent = multiagent.ManagerAgent(db)

@app.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()
    user_email = data.get("userId")
    if not user_email:
        return jsonify({"error": "userId is required"}), 400
    try:
        user = db.create_user(user_email)
        return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/summarizeAndStore', methods=['POST'])
def summarize_and_store():
    data = request.get_json()
    bookmark_id = data.get("id")
    title = data.get("title")
    url = data.get("url")
    if not all([bookmark_id, title, url]):
        return jsonify({"error": "id, title, and url are required"}), 400
    user_email = data.get("userEmail", "default@example.com")
    try:
        bookmark = manager_agent.handle_summarization(data, user_email)
        return jsonify(bookmark)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/randomBookmarks', methods=['GET'])
def random_bookmarks():
    try:
        bookmarks = db.get_random_bookmarks(count=1)
        print("Random bookmarks:", bookmarks)
        return jsonify(bookmarks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    bookmark_id = data.get("bookmarkId")
    feedback_val = data.get("feedback")
    user_email = data.get("userId")  # Expecting userId (e.g. Google email)
    if not bookmark_id or feedback_val not in ("like", "dislike") or not user_email:
        return jsonify({"error": "bookmarkId, userId, and valid feedback (like/dislike) are required"}), 400
    try:
        result = manager_agent.handle_feedback(bookmark_id, user_email, feedback_val)
        return jsonify({"relationship": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    bookmark_id = data.get("bookmarkId")
    query = data.get("query")
    if not bookmark_id or not query:
        return jsonify({"error": "bookmarkId and query are required"}), 400
    try:
        response_text = manager_agent.handle_chat(bookmark_id, query)
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
