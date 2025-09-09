from flask import Flask, jsonify
from flask_cors import CORS
from teams import teams

app = Flask(__name__)
CORS(app)

# ✅ كل المنتخبات
@app.route("/teams", methods=["GET"])
def get_teams():
    return jsonify(teams)

# ✅ منتخبات حسب القارة
@app.route("/teams/continent/<continent>", methods=["GET"])
def get_teams_by_continent(continent):
    result = [t for t in teams if t["قارة"] == continent]
    return jsonify(result)

# ✅ البحث عن منتخب بالاسم
@app.route("/teams/search/<name>", methods=["GET"])
def search_team(name):
    result = [t for t in teams if name in t["اسم"]]
    return jsonify(result if result else {"رسالة": "المنتخب غير موجود"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)