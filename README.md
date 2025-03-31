# Clipyt

Clipyt is a Python-based clipboard monitoring tool that records clipboard changes, stores them in a SQLite database, and provides a web interface for viewing and managing clipboard history.

## Features

- **Clipboard Monitoring**: Continuously monitors the clipboard for changes and records each new entry with a timestamp.
- **Database Storage**: Stores clipboard contents in a SQLite database using a Peewee model with UUIDs as primary keys.
- **Command Interface**: Supports commands to start recording (`RECORD`) and to list the latest 10 entries (`LIST`).
- **Web Interface**: Provides a Flask-based API with routes to retrieve clipboard entries between two dates and to delete specific entries.
- **Cross-Platform Support**: Stores the SQLite database in a `.clipster` directory inside the user's home directory, ensuring compatibility across different operating systems.
- **Modern UI**: Includes a Svelte-based web application that allows users to view and manage clipboard entries by day or week, with options to copy or delete individual entries.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/iaseth/clipyt.git
   ```


2. **Navigate to the Project Directory**:
   ```bash
   cd clipyt
   ```


3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```


   *Note: Ensure you have Python and pip installed on your system.*

## Usage

1. **Start Clipboard Monitoring**:
   ```bash
   python clipyt.py RECORD
   ```


   This command will start monitoring the clipboard and recording changes into the SQLite database.

2. **List the Latest 10 Entries**:
   ```bash
   python clipyt.py LIST
   ```


   This command will display the 10 most recent clipboard entries along with their timestamps.

3. **Run the Flask Web Server**:
   ```bash
   python flaskapp.py
   ```


   This will start the Flask server, making the API endpoints accessible for retrieving and managing clipboard entries.

4. **Access the Svelte Web Application**:
   Navigate to the appropriate directory and start the Svelte development server:
   ```bash
   cd svelteclip
   npm install
   npm run dev
   ```


   Then, open the provided local URL in your browser to interact with the web application.

## API Endpoints

- **Retrieve Entries Between Two Dates**:
  
```
  GET /entries?start=YYYY-MM-DD&end=YYYY-MM-DD
  ```


  Returns clipboard entries between the specified dates. The maximum span allowed is 7 days.

- **Delete a Specific Entry**:
  
```
  DELETE /entries/<entry_id>
  ```


  Deletes the clipboard entry with the specified UUID.

## Database Storage

The SQLite database is stored in a `.clipster` directory within the user's home directory, ensuring that the application works seamlessly across different platforms.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
