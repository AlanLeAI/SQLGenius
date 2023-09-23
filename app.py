from flask import Flask, render_template, request, redirect, url_for
from utils import *
import openai

# Set your OpenAI API key
openai.api_key = '<API Key>'

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', tables = tables, skills = skills)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedbacks')
def feedback():
    return render_template('feedback.html')

@app.route('/sqlgen', methods=['GET', 'POST'])
def sqlgen():
    if request.method == 'POST':
        req = request.form["requirement"]
        res = schema_to_txt(tables=tables)
        prompt = text_to_prompt(res, req)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100  # Adjust as needed
        )
        sql = response.choices[0].text.strip()
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

@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    if request.method == 'POST':
        # generated_sql = None
        table_name = request.form['table_name']
        columns = []
        for key in request.form.keys():
            if key.startswith('column_name_'):
                column_name = request.form[key]
                column_condition = request.form.get(key.replace('name', 'condition'))
                column_datatype = request.form.get(key.replace('name', 'datatype'))
                columns.append({"name": column_name, "condition": column_condition, "dtype": column_datatype})
        tables.append({"name": table_name, "columns": columns})
        return redirect(url_for('sqlgen'))
    return redirect(url_for('sqlgen'))



if __name__ == '__main__':
    app.run(debug=True)
