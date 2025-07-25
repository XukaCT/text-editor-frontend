from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

client = MongoClient('mongodb+srv://TextEditor:3dKw1b7chPWDjpsf@cluster0.o9jjzyp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['TextEditor']
collection = db['notes']

app = Flask(__name__)   
CORS(app)

@app.route("/save", methods=["POST"])
def save_file():
    data = request.json
    filename = data.get("filename", "").strip()
    content = data.get("content", "")

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    collection  .update_one(
        {"filename": filename},
        {"$set": {"content": content}},
        upsert=True
    )
    return jsonify({"status": "saved"}), 200

@app.route("/open/<filename>", methods=["GET"])
def open_file(filename):
    note = collection.find_one({"filename": filename})
    if note:
        return jsonify({
            "filename": filename,
            "content": note["content"]
        })
    else:
        return jsonify({"error": "Note not found"}), 404

@app.route("/files", methods=["GET"])
def list_files():
    filenames = collection.distinct("filename")
    return jsonify(filenames), 200


if __name__ == "__main__":
    app.run(debug=True)
