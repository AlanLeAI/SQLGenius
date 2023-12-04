from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from utils import *
import pandas as pd
import openai
import os

from flask_mail import Mail, Message
from flask_session import Session

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)
sess = Session()

# Configure Flask Mail for Gmail
app.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='tuanle_2024@depauw.edu',
    MAIL_PASSWORD='jmmwglrirwdyinac'
))


UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mail = Mail(app)

skills = [
    {
      'name': 'HTML',
      'src': './static/images/html.svg',
    },
    {
      'name': 'CSS',
      'src': './static/images/CSS..svg',
    },
    {
      'name': 'JavaScript',
      'src': './static/images/javascript.svg',
    },
    {
      'name': 'Python',
      'src': './static/images/python.svg',
    },
    {
      'name': 'Flask',
      'src': './static/images/flask.svg',
    },
   
    
  ]
tables = []
sql = ""
previous = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', tables = tables, skills = skills)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedbacks')
def feedback():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        major = request.form['major']
        feedback = request.form['feedback']

        message = Message("SQL Genius - User's feedback", sender='tuanle_2024@depauw.edu', recipients=['tuanle_2024@depauw.edu'])
        message.body = f'''
SQL GENIUS WEB APPLICATION
There is 1 new user's feedback!

Customer's Name: {name}

Customer's Email: {email}

Customer's Feedbacks: {feedback}
        '''
        mail.send(message)

        flash('Feedback submitted successfully!')
        return redirect(url_for('feedback'))

@app.route('/sqlgen', methods=['GET', 'POST'])
def sqlgen():
    global previous
    if request.method == 'POST':
        req = request.form["requirement"]
        req = previous if req == "" else req
        previous = req if req != "" else previous
        res = schema_to_txt(tables=tables)
        sql = message_to_prompt(res, req)
        return render_template('sqlgen.html', tables = tables,generated_sql = sql)
    return render_template('sqlgen.html', tables = tables,generated_sql = None)

@app.route('/update_sql',  methods=['GET', 'POST'])
def update_sql():
    global previous
    if request.method == 'POST':
        req =previous
        res = schema_to_txt(tables=tables)
        sql = message_to_prompt(res, req)
        return render_template('sqlgen.html', tables = tables,generated_sql = sql)
    return render_template('sqlgen.html', tables = tables,generated_sql = None)

@app.route('/reset', methods=['POST'])
def reset():
    global tables
    tables = []  # Clear all tables
    return redirect(url_for('sqlgen'))

@app.route('/pop', methods=['POST'])
def pop():
    global tables
    if len(tables) > 0:
        tables.pop() # Clear all tables
    return redirect(url_for('sqlgen'))

@app.route('/edit', methods=['POST'])
def edit():
    if request.method == 'POST':
        # generated_sql = None
        table_name_edit = request.form.get('table_name_edit')
        column_name_edit = request.form['column_name_edit']
        data_type_edit = request.form.get('column_datatype_edit')
        condition_edit = request.form.get('column_condition_edit')
        foreing_key_edit = ""
        if condition_edit == "foreign_key":
            foreing_key_edit = request.form.get('column_reference_table_edit')
        temp = None
        idx = -1
        for i,ele in enumerate(tables):
            if ele["name"].lower() == table_name_edit.lower():
                temp = ele
                idx = i
                break
        
        if temp is not None:
            for i,col in enumerate(temp["columns"]):
                if temp["columns"][i]["name"].lower() == column_name_edit.lower():
                    temp["columns"][i]["dtype"] =data_type_edit
                    temp["columns"][i]["condition"] = condition_edit
                    temp["columns"][i]["referTo"] = foreing_key_edit
                    break
        return redirect(url_for('sqlgen'))
    return redirect(url_for('sqlgen'))

@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    if request.method == 'POST':
        # generated_sql = None
        table_name = request.form['table_name']
        columns = []
        for key in request.form.keys():
            if key.startswith('column_name_'):
                column_name = request.form[key]
                reference_to = ""
                column_condition = request.form.get(key.replace('name', 'condition'))
                if column_condition == "foreign_key":
                    reference_to = request.form.get(key.replace('name', 'reference_table'))
                column_datatype = request.form.get(key.replace('name', 'datatype'))
                columns.append({"name": column_name, "condition": column_condition, "dtype": column_datatype, "referTo": reference_to})
        tables.append({"name": table_name, "columns": columns})
        return redirect(url_for('sqlgen'))
    return redirect(url_for('sqlgen'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            # Save the file to the UPLOAD_FOLDER
            temp = file.filename[:-4]
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            df = pd.read_csv(filename)
            columns = []
            for col in df.columns:
                tempname = col.lower()
                column_condition = "Null"
                column_datatype = "Text"
                if "id" in tempname:
                    column_condition = "primary_key"
                    column_datatype = "int"
                column_name = col
                
                columns.append({"name": column_name, "condition": column_condition, "dtype": column_datatype})
            tables.append({"name": temp, "columns": columns})

            return redirect(url_for('sqlgen'))
        else:
            return redirect(url_for('sqlgen'))
    return redirect(url_for('sqlgen'))


@app.route('/get_columns', methods=['POST'])
def get_columns():
    data = request.get_json()

    # Get the selected table name from the request
    table_name = data.get('table_name')

    # Find the table with the selected name
    selected_table = next((table for table in tables if table['name'] == table_name), None)

    if selected_table:
        # Return the columns for the selected table
        return jsonify({'columns': selected_table['columns']})
    else:
        # Return an empty list if the table is not found
        return jsonify({'columns': []})


@app.route('/get_tables', methods=['GET'])
def get_tables():
    return jsonify({'tables': tables})




if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run(debug=True)
