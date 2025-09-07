from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "9536f9ee307a4e6489d9d2bbee50f67e"

# الدوريات المدعومة
COMPETITIONS = {
    "PL": "🏴 الدوري الإنجليزي الممتاز",
    "PD": "🇪🇸 الدوري الإسباني (La Liga)",
    "SA": "🇮🇹 الدوري الإيطالي (Serie A)",
    "BL1": "🇩🇪 الدوري الألماني (Bundesliga)",
    "FL1": "🇫🇷 الدوري الفرنسي (Ligue 1)",
    "CL": "⭐ دوري أبطال أوروبا"
}


def get_matches(competition="PL"):
    url = f"https://api.football-data.org/v4/competitions/{competition}/matches"
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()
    matches = []
    for m in data.get("matches", []):
        matches.append({
            "date": m["utcDate"][:10],
            "status": m["status"],
            "matchday": m["matchday"],
            "homeTeam": m["homeTeam"]["name"],
            "homeCrest": m["homeTeam"]["crest"],
            "awayTeam": m["awayTeam"]["name"],
            "awayCrest": m["awayTeam"]["crest"],
            "score_home": m["score"]["fullTime"]["home"],
            "score_away": m["score"]["fullTime"]["away"]
        })
    return matches


@app.route("/", methods=["GET"])
def index():
    comp = request.args.get("competition", "PL")
    matches = get_matches(comp)

    # فلترة حسب الفريق
    team_query = request.args.get("team", "").lower()
    if team_query:
        matches = [m for m in matches if team_query in m["homeTeam"].lower() or team_query in m["awayTeam"].lower()]

    # ترتيب حسب الجولة
    matches_by_day = {}
    for m in matches:
        md = m["matchday"]
        if md not in matches_by_day:
            matches_by_day[md] = []
        matches_by_day[md].append(m)

    return render_template("index.html", competitions=COMPETITIONS, current_comp=comp, matches_by_day=matches_by_day)


if __name__ == "__main__":
    app.run(debug=True)