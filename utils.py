import openai
import os
import sqlparse

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]


tables = [{'name': 'Student', 
                'columns': [{'name': 'id', 'condition': 'primary_key', 'dtype': 'int'}, 
                            {'name': 'name', 'condition': 'not_null', 'dtype': 'txt'}, 
                            {'name': 'email', 'condition': 'not_null', 'dtype': 'txt'}
                            ]},
            {'name': 'Department', 
                'columns': [{'name': 'Name', 'condition': 'not_null', 'dtype': 'txt'}, 
                            {'name': 'code', 'condition': 'primary_key', 'dtype': 'int'}, 
                            {'name': 'NumProf', 'condition': 'not_null', 'dtype': 'int'}]}         
         ]

def schema_to_txt(tables):
    res= ""

    for table in tables:
        res += "Table: " + table['name'] + "\n"
        res += "Columns: "
        for i, column in enumerate(table['columns']):
            if column["condition"] == "foreign_key":
                res += column["name"] + " (" +  column["dtype"] +") " + " (" +   column["condition"] +"), reference to " + column["referTo"] +" table."
            else:
                res += column["name"] + " (" +  column["dtype"] +") " + " (" +   column["condition"] +") ,"
        res += "\n"
    return res




def text_to_message(content, requirement):
    prompt =  content + "\n ####: " + requirement

    # Generate SQL query using GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100  # Adjust as needed
    )

    # Generate SQL query using GPT-3

    # Extract and print the generated SQL query
    generated_query = response.choices[0].text.strip()
    print(generated_query)
    return prompt


def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]

def message_to_prompt(schema, requirement):
    delimiter = "####"
    table_schema = schema
    system_message = f"""
        You will be provided with database schema. \
        Each table has specific columns do not make up column name\
        {table_schema}\
        The user query will be delimited with \
        {delimiter} characters. \
        Generate The SQL query based on user requirement and database schema. \
        Provide your output in String format.
    """

    user_message = requirement

    messages =  [  
        {'role':'system', 
        'content': system_message},    
        {'role':'user', 
        'content': f"{delimiter}{user_message}{delimiter}"},  
    ] 
    response = get_completion_from_messages(messages)
    # Use sqlparse to format the SQL query
    formatted_sql = sqlparse.format(response,
                                    use_space_around_operators = True,
                                    reindent_aligned = True, 
                                    indent_width = 4,
                                    keyword_case='upper')

    return formatted_sql

# a = message_to_prompt(schema_to_txt(tables), "Get number of student for each department")
# print(a)
