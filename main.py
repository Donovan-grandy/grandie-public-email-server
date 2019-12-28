from flask import Flask, render_template, Response,jsonify,request
from flask_sendgrid import SendGrid
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from flask_cors import CORS,cross_origin
import os
import json
import sqlalchemy
import datetime
from db import connect_to_db
load_dotenv()
app = Flask(__name__)
CORS(app)

try:
    SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']

except Exception:
    raise Exception('You must define API_KEY and API_SECRET environment variables')

@app.before_first_request
def create_tables():
    # Create tables (if they don't already exist)
    db = connect_to_db()
    with db.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS signup_emails "
            "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
            "candidate VARCHAR(6) NOT NULL, PRIMARY KEY (vote_id) );"
        )




@app.route('/api/v1/email/initiator-selection', methods=['POST','OPTIONS'])
def session():
    sg = SendGridAPIClient()
    campaign_id = "d-784e10076c6644eb86ab5d80ff5d1485"
    response = sg.client.templates._(campaign_id).get()
    html_content = json.loads(response.body)['versions'][0]['html_content']
    if request.method == 'POST':
        message= Mail(
            from_email='hub@grandy.com',
            to_emails=request.form.get('email'),
            subject='Welcome to Grandy',
            html_content=html_content
        )
        try:
            response = sg.send(message)
            response = jsonify({'status':200,'text':'Sucesss'})
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
        except Exception as e:
            print(str(e))

    return ''


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)

