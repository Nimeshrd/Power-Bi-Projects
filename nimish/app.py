import subprocess
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_session import Session
from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv
import identity.web
import requests

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Microsoft Azure AD configuration
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}"
REDIRECT_PATH = "/getAToken"
ENDPOINT = 'https://graph.microsoft.com/v1.0/me'
SCOPE = ["User.Read"]

# MSAL setup
msal_app = ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
    token_cache=None
)
auth = identity.web.Auth(
    session=session,
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
)

@app.route("/login")
def login():
    return render_template("login.html", **auth.log_in(
        scopes=SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth_response", _external=True)
    ))

@app.route(REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    # Redirect to index or any other endpoint after successful login
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))

@app.route("/")
def index():
    user = auth.get_user()
    if not user:
        return redirect(url_for("login"))
    
    return render_template("index.html", user=user)

@app.route("/call_downstream_api")
def call_downstream_api():
    token = auth.get_token_for_user(SCOPE)
    if "error" in token:
        return redirect(url_for("login"))
    # Use access token to call downstream api
    api_result = requests.get(
        ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).json()
    return render_template('display.html', result=api_result)

def execute_podman_command(command):
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True)
        return result.stdout, result.returncode
    except Exception as e:
        return str(e), 1

@app.route('/process_candidate')
def process_candidate():
    # Check if user is authenticated
    user = auth.get_user()
    if not user:
        return redirect(url_for("login"))

    try:
        # Get parameters from request or use defaults
        num_candidates = request.args.get('numcandidates', default=int(os.getenv('NUM_CANDIDATES', 5)), type=int)
        batch_size = request.args.get('batchsize', default=int(os.getenv('BATCH_SIZE', 50)), type=int)

        if num_candidates <= 0:
            num_candidates = int(os.getenv('NUM_CANDIDATES', 5))
        if batch_size <= 0:
            batch_size = int(os.getenv('BATCH_SIZE', 50))
    except ValueError:
        return jsonify({"message": "Invalid input. Please enter valid integers for numcandidates and batchsize."}), 400

    # Form the Podman command with the provided values
    command = f"podman run --env NUM_CANDIDATES={num_candidates} --env BATCH_SIZE={batch_size} your_image_name"

    # Execute the Podman command
    output, returncode = execute_podman_command(command)
    if returncode == 0:
        return render_template('process_output.html', message=f"Podman image started successfully with {num_candidates} candidates and batch size {batch_size}.", output=output)
    else:
        return jsonify({"message": "Failed to start Podman image.", "output": output}), 500

@app.route('/stop')
def stop():
    command = "podman stop your_container_name"
    output, returncode = execute_podman_command(command)
    if returncode == 0:
        return render_template('stopped.html', message="Podman image stopped successfully.")
    else:
        return jsonify({"message": "Failed to stop Podman image.", "output": output}), 500

if __name__ == "__main__":
    app.run()
