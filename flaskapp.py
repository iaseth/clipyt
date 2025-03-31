from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from clipyt import ClipboardEntry



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/entries", methods=["GET"])
@cross_origin()
def get_entries():
	try:
		start_date = int(request.args.get("start", 0))
		end_date = int(request.args.get("end", 0))

		if end_date - start_date > 604800:  # 7 days in seconds
			return jsonify({"error": "Date range exceeds 7 days"}), 400

		entries = (ClipboardEntry
		   .select()
		   .where((ClipboardEntry.timestamp >= start_date) & (ClipboardEntry.timestamp <= end_date))
		   .order_by(ClipboardEntry.timestamp.desc()))
		return jsonify([{ "id": str(entry.id), "timestamp": entry.timestamp, "content": entry.content } for entry in entries])
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route("/delete/<uuid:entry_id>", methods=["DELETE"])
@cross_origin()
def delete_entry(entry_id):
	try:
		query = ClipboardEntry.get_or_none(ClipboardEntry.id == entry_id)
		if query:
			query.delete_instance()
			return jsonify({"message": "Entry deleted"})
		return jsonify({"error": "Entry not found"}), 404
	except Exception as e:
		return jsonify({"error": str(e)}), 500


