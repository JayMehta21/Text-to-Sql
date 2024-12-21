from dotenv import load_dotenv
load_dotenv()  # Load all environment variables

import streamlit as st 
import os 
import sqlite3
import google.generativeai as genai

# Configure the Google API key
# Manually pass the API key
genai.configure(api_key='AIzaSyA_vpb2GS-Wpq0h0aLjScpMA_c5z_DrAwI')

# Function to load the Google Gemini model and provide an SQL query as a response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    full_input = prompt + "\n" + question  # Concatenate the prompt and question
    response = model.generate_content([full_input])  # Pass the full input as a single argument
    return response.text.strip()  # Return the response after stripping unwanted whitespace


# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


# Define Your Prompt
prompt = """
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION, and MARKS.

For example:
Example 1 - How many entries of records are present? 
The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;

Example 2 - Tell me all the students studying in Data Science class? 
The SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS="Data Science"; 

Also, the SQL code should not have backticks at the beginning or end, and the word "SQL" should not be present in the output.
"""

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input:", key="input")

submit = st.button("Ask the question")

# If submit is clicked
if submit:
    if question:  # Ensure the question is not empty
        response = get_gemini_response(question, prompt)
        if response:  # Ensure response is not empty
            st.subheader("Generated SQL Query:")
            st.code(response, language="sql")  # Display the SQL query

            # Execute the SQL query on the database
            try:
                query_result = read_sql_query(response, "student.db")
                st.subheader("Query Results:")
                if query_result:
                    for row in query_result:
                        st.write(row)  # Display each row of the result
                else:
                    st.write("No results found.")
            except Exception as e:
                st.error(f"Error executing the query: {e}")
        else:
            st.warning("No valid SQL query generated.")
    else:
        st.warning("Please enter a question.")

