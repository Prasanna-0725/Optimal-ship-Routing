from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import subprocess

# Define base directory
BASE_DIR = "C:/g2/sih/"

# Initialize Flask application
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

# Load port data from CSV
ports_df = pd.read_csv(os.path.join(BASE_DIR, 'ports_coordinates.csv'))

# Function to safely load the CSV file for ocean points
def load_csv_safe(filepath):
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            raise ValueError("CSV file is empty.")
        df.columns = df.columns.str.strip()  # Ensure column names are clean
        return df
    except (pd.errors.EmptyDataError, ValueError) as e:
        print(f"Error loading CSV file: {e}")
        return None

# Route for the homepage
@app.route('/')
def home():
    # Get the list of ports
    ports = ports_df['Port_Name'].tolist()
    return render_template('index.html', ports=ports)

# Route for handling form submission
@app.route('/set_route', methods=['POST'])
def set_route():
    source_port = request.form.get('source')
    destination_port = request.form.get('destination')

    # Check if the source and destination ports are the same
    if source_port == destination_port:
        return "Source and destination ports cannot be the same.", 400

    # Get coordinates for the selected ports
    source_coords = ports_df[ports_df['Port_Name'] == source_port][['Latitude', 'Longitude']].values[0]
    destination_coords = ports_df[ports_df['Port_Name'] == destination_port][['Latitude', 'Longitude']].values[0]

    # Save the coordinates to a text file
    selected_ports_file = os.path.join(BASE_DIR, 'selected_ports.txt')
    with open(selected_ports_file, 'w') as f:
        f.write(f"{source_coords[0]},{source_coords[1]}\n")
        f.write(f"{destination_coords[0]},{destination_coords[1]}")

    script_path = os.path.join(BASE_DIR, 'pathfinding.py')

    if not os.path.isfile(script_path):
        print(f"File not found: {script_path}")
        return "Pathfinding script not found.", 500

    try:
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")
        print(e.stderr)

    return redirect(url_for('path_confirmation'))

# Route for path confirmation
@app.route('/path_confirmation')
def path_confirmation():
    return "The route has been set. The server will now calculate the path."

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
