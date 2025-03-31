import time
import pyperclip
import argparse
import uuid
import os
import peewee
from datetime import datetime

# Set up database path in .clipyt directory inside the user's home folder
home_dir = os.path.expanduser("~")
app_data_dir = os.path.join(home_dir, ".clipyt")
os.makedirs(app_data_dir, exist_ok=True)
db_path = os.path.join(app_data_dir, "clipyt.db")

db = peewee.SqliteDatabase(db_path)

class ClipboardEntry(peewee.Model):
	id = peewee.UUIDField(primary_key=True, default=uuid.uuid4)
	timestamp = peewee.IntegerField()
	content = peewee.TextField()

	class Meta:
		database = db

# Create table if not exists
db.connect()
db.create_tables([ClipboardEntry], safe=True)

def record_clipboard():
	last_clipboard = ""
	while True:
		current_clipboard = pyperclip.paste()
		if current_clipboard and current_clipboard != last_clipboard:
			ClipboardEntry.create(id=uuid.uuid4(), timestamp=int(time.time()), content=current_clipboard)
			print(f"Recorded: {current_clipboard}")
			last_clipboard = current_clipboard
		time.sleep(1)

def list_entries():
	entries = ClipboardEntry.select().order_by(ClipboardEntry.timestamp.desc()).limit(10)
	for i, entry in enumerate(entries, start=1):
		print(f"{i}. {datetime.fromtimestamp(entry.timestamp)} - {entry.content}")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("command", choices=["RECORD", "LIST"], help="Command to execute")
	args = parser.parse_args()

	if args.command == "RECORD":
		record_clipboard()
	elif args.command == "LIST":
		list_entries()

if __name__ == "__main__":
	main()
