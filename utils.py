import openai

# Set your OpenAI API key
openai.api_key = '<API key>'


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
            res += column["name"] + " (" +  column["dtype"] +") " + " (" +   column["condition"] +") ,"
        res += "\n"
    return res




def text_to_prompt(content, requirement):
    prompt =  content + "\n Question: " + requirement

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