import openai
import sqlparse
import os

# # Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]
print(openai.api_key)
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



sql_string = "select name, studentid, email from student join department d on student.id = d.id where student.id = 75"

# Use sqlparse to format the SQL query
formatted_sql = sqlparse.format(sql_string,
                                use_space_around_operators = True,
                                reindent_aligned = True, 
                                indent_width = 4,
                                keyword_case='upper')

print(formatted_sql)