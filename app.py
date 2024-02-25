from urllib.parse import quote, unquote
from flask import Flask, request, redirect, url_for, render_template, jsonify, session
import os
from werkzeug.utils import secure_filename
from backend import get_scores
import json
import pandas as pd

app = Flask("JobHat")
app.config['url'] = "https://github.com/SimplifyJobs/Summer2024-Internships"  # Default URL

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return redirect(request.url)
    file = request.files['resume']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Process your file here (e.g., save it somewhere or analyze it)
        filename = secure_filename(file.filename)
        filename = os.path.join(filename)
        file.save(filename)

        # Process the uploaded file to get job matches
        # print(app.config['url'])
        df = get_scores(app.config['url'], filename)

        # Delete resume as we believe in Data Privacy
        os.remove(filename)

        job_matches_json = df.to_json(orient='records')
        encoded_json = quote(job_matches_json)
        return redirect(url_for('job_matches', job_matches=encoded_json))

@app.route('/job-matches')
def job_matches():
    job_matches_json = request.args.get('job_matches', '[]')
    decoded_json = unquote(job_matches_json)
    df = pd.read_json(decoded_json)
    return render_template('job_matches.html', jobs=df.to_dict(orient='records'))

@app.route('/change-url', methods=['POST'])
def change_url():
    data = request.json
    app.config['url'] = data.get('url')  # Update the URL in application configuration
    return jsonify({'message': 'URL changed successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
