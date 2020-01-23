from flask import Flask, render_template, Response,jsonify,request
from flask_sendgrid import SendGrid
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from flask_cors import CORS,cross_origin
from sqlalchemy.orm import sessionmaker
import os
import json
from models import Teacher,Student,InitiatorContact

import sqlalchemy
import datetime
load_dotenv()
app = Flask(__name__)
CORS(app)

db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

# print(cloud_sql_connection_name)

try:
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

except Exception:
    raise Exception('You must define API_KEY and API_SECRET environment variables')

try:
    db = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgres+pg8000://<db_user>:<db_pass>@/<db_name>?unix_sock=/cloudsql/<cloud_sql_instance_name>/.s.PGSQL.5432
        sqlalchemy.engine.url.URL(
            drivername='postgres+pg8000',
            username=db_user,
            password=db_pass,
            database=db_name,
            query={
                'unix_sock': '/cloudsql/{}/.s.PGSQL.5432'.format(
                    cloud_sql_connection_name)
            }
        ),
        # ... Specify additional properties here.
        # [START_EXCLUDE]

        # [START cloud_sql_postgres_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        pool_size=5,
        # Temporarily exceeds the set pool_size if no connections are available.
        max_overflow=2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_postgres_sqlalchemy_limit]

        # [START cloud_sql_postgres_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_postgres_sqlalchemy_backoff]

        # [START cloud_sql_postgres_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        pool_timeout=30,  # 30 seconds
        # [END cloud_sql_postgres_sqlalchemy_timeout]

        # [START cloud_sql_postgres_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        pool_recycle=1800,  # 30 minutes
        # [END cloud_sql_postgres_sqlalchemy_lifetime]

        # [END_EXCLUDE]
    )
except Exception as e:
    print(e)



try:
    db_session = sessionmaker(bind=db)
except Exception as e:
    print(e)

@app.route('/api/v1/email/initiator-selection', methods=['POST','OPTIONS'])
def session():
    try:
        initiator = InitiatorContact(firstname=request.form.get('firstname'),lastname=request.form.get('lastname'),email=request.form.get('email'),initiator_type=request.form.get('type'))
        db_session.add(initiator)
        db_session.commit()
    except Exception as e:
        print(e)
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

@app.route('/teachers', methods=['POST','OPTIONS'])
def teachers():
    print(request.form)
    class_code = request.form.get('class_code')
    try:
        teacher = Teacher(
        firstname=request.form.get('first_name'),
        lastname=request.form.get('last_name'),
        email=request.form.get('email'),
        grade=request.form.get('grade'),
        county=request.form.get('county'),
        state=request.form.get('state'),
        city=request.form.get('city'),
        zipcode=request.form.get('zip_code'),
        classcode=''
        )
        db_session.add(teacher)
        db_session.commit()
    except Exception as e:
        print(e)
    message = Mail(
    from_email='from_email@example.com',
    to_emails='to@example.com',
    html_content='<strong>Thank you from Grandy</strong>')
    message.dynamic_template_data = {
        'subject': 'Thank you from Grandy',
        'first_name': request.form.get('first_name'),
        'school': request.form.get('school'),
        'class_code':class_code
    }
    message.template_id = 'd-cb512bdefbf54e1ba9a71804d7a3dcbd'
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        print(request.form)

@app.route('/students', methods=['POST','OPTIONS'])
# {{first_name}} {{last_name}}
# Your class code for school:  {{ school }}
# is {{ class_code }}
def students():
    print(request.form)

    try:
        student = Student(
        firstname=request.form.get('first_name'),
        lastname=request.form.get('last_name'),
        email=request.form.get('email'),
        grade=request.form.get('grade'),
        county=request.form.get('county'),
        state=request.form.get('state'),
        city=request.form.get('city'),
        zipcode=request.form.get('zip_code'),
        classcode=request.form.get('class_code')
        )
        db_session.add(student)
        db_session.commit()
    except Exception as e:
        print(e)

    print(request.form)
    message = Mail(
    from_email='hub@grandy.com',
    to_emails=request.form.get('email'),
    html_content='<strong>Thank you from Grandy</strong>')
    message.dynamic_template_data = {
        'subject': 'Thank you from Grandy',
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'school':request.form.get('school'),
        'class_code': request.form.get('class_code')
    }
    message.template_id = 'd-e2cb30520f6d4633a271aa5130502cd7'
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        print(request.form)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True,ssl_context=('cert.pem', 'key.pem'))

