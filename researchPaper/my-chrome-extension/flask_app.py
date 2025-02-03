from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id')
    recommendations = recommend_papers(user_id)  # Assuming this function is defined in your backend logic
    return jsonify(recommendations)

@app.route('/interact', methods=['POST'])
def interact():
    data = request.json
    user_id = data['user_id']
    paper_id = data['paper_id']
    interaction_type = data['interaction_type']
    add_interaction(user_id, paper_id, interaction_type)  # Assuming this function is defined in your backend logic
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
