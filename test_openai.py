import openai
import sqlparse

# # Set your OpenAI API key
# openai.api_key = 'API key'

# # Define the prompt
# prompt = """
# what is 1 + 1
# """

# # Generate SQL query using GPT-3
# response = openai.Completion.create(
#     engine="text-davinci-003",
#     prompt=prompt,
#     max_tokens=100  # Adjust as needed
# )

# # Extract and print the generated SQL query
# generated_query = response.choices[0].text.strip()
# print(generated_query)



sql_string = "select * from student join department d on student.id = d.id where student.id = 75"

# Use sqlparse to format the SQL query
formatted_sql = sqlparse.format(sql_string, reindent=True, keyword_case='upper')

print(formatted_sql)