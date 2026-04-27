from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

members = [
    {"id": 1, "name": "Aarav", "plan": "Gold", "trainer": "Riya"},
    {"id": 2, "name": "Meera", "plan": "Silver", "trainer": "Karan"},
]

plans = [
    {"id": 1, "name": "Basic", "price": 999},
    {"id": 2, "name": "Silver", "price": 1499},
    {"id": 3, "name": "Gold", "price": 2499},
]

HOME_PAGE = """
<!doctype html>
<title>ACEest Fitness & Gym</title>
<h1>ACEest Fitness & Gym Management System</h1>
<p>DevOps CI/CD Assignment Flask Application</p>
<ul>
  <li><a href='/health'>Health Check</a></li>
  <li><a href='/members'>Members API</a></li>
  <li><a href='/plans'>Plans API</a></li>
</ul>
"""

@app.route("/")
def home():
    return render_template_string(HOME_PAGE)

@app.route("/health")
def health():
    return jsonify({"status": "UP", "service": "ACEest Fitness"}), 200

@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(members), 200

@app.route("/members", methods=["POST"])
def add_member():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    plan = data.get("plan")
    trainer = data.get("trainer", "Not Assigned")

    if not name or not plan:
        return jsonify({"error": "name and plan are required"}), 400

    new_member = {
        "id": len(members) + 1,
        "name": name,
        "plan": plan,
        "trainer": trainer,
    }
    members.append(new_member)
    return jsonify(new_member), 201

@app.route("/plans")
def get_plans():
    return jsonify(plans), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
