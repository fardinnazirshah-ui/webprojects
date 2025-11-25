from flask import Flask, render_template, request, g
from database import Database

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = Database()


@app.before_request
def getStatsBefore():
    stats_info = db.get_stats()
    g.stats = stats_info


@app.after_request
def stopCache(r):
    r.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return r


@app.route("/")
def home():
    return render_template("index.html", stats=g.stats)


def convert_rank(rankText):
    if rankText == None or rankText == "":
        return None
    try:
        number = int(rankText)
    except:
        return None
    if number <= 0:
        return None
    return number


@app.route("/predict", methods=["POST"])
def predict():
    rankStr = request.form.get("rank")
    examType = request.form.get("exam_type")
    cat = request.form.get("category")

    if cat is None:
        cat = "OPEN"

    if rankStr is None or rankStr == "" or examType is None or examType == "":
        return render_template("index.html", error="Please fill everything.", stats=g.stats)

    cleaned_rank = convert_rank(rankStr)

    if cleaned_rank is None:
        return render_template("index.html", error="Rank must be a positive number (under 30000).", stats=g.stats)

    try:
        result_data = db.get_predictions(cleaned_rank, examType, cat)
    except Exception as e:
        return render_template("index.html", error="Something went wrong, sorry!!", stats=g.stats)

    return render_template("index.html",
                           results=result_data,
                           rank=cleaned_rank, exam_type=examType, category=cat,
                           stats=g.stats)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

