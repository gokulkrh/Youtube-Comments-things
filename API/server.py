from flask import Flask, jsonify
import mock_responses

app = Flask(__name__)


@app.route("/youtube-fyp/emo_stats/<videoid>")
def return_emo_stats(videoid):
    return jsonify(mock_responses.mock_emotion)


@app.route("/youtube-fyp/comments_summary/<videoid>")
def return_comments_summary(videoid):
    return jsonify(mock_responses.mock_summary)


@app.route("/youtube-fyp/all/<videoid>")
def return_everything(videoid):
    return jsonify(mock_responses.mock_all)


if __name__=="__main__":
    app.run(debug=True)
