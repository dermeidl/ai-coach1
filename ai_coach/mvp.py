import pickle
from pathlib import Path
import streamlit_authenticator as stauth 
# all for authentication

import streamlit as st
from langchain.llms import OpenAI
import pandas as pd
import numpy as np
from datetime import datetime
import os

#--- USER AUTHENTICATION ---
# file_path = Path(__file__).parent / "hased_pw.pkl"
# with file_path.open("rb") as file:
#     hased_passwords = pickle.load(file)

names = ['John Smith','Rebecca Briggs']
usernames = ['patrick','leon']
passwords = ['test123','pushups']

hashed_passwords = stauth.Hasher(passwords).generate()
   
authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
     'ai_coach', 'abcdef', cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
if authentication_status == None:
    st.warning("Please enter your nusername and password")
if authentication_status == True:
    

# def check_password():
#     """Returns `True` if the user had a correct password."""

#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if (
#             st.session_state["username"] in st.secrets["passwords"]
#             and st.session_state["password"]
#             == st.secrets["passwords"][st.session_state["username"]]
#         ):
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # don't store username + password
#             del st.session_state["username"]
#         else:
#             st.session_state["password_correct"] = False

#     if "password_correct" not in st.session_state:
#         # First run, show inputs for username + password.
#         st.text_input("Username", on_change=password_entered, key="username")
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
#         return False
#     elif not st.session_state["password_correct"]:
#         # Password not correct, show input + error.
#         st.text_input("Username", on_change=password_entered, key="username")
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
#         st.error("😕 User not known or password incorrect")
#         return False
#     else:
#         # Password correct.
#         return True

# if check_password():
#     # 0. streamlit settings/page configuration
    st.set_page_config(page_title="GPT-3 Chatbot", page_icon=":rocket:", layout="wide")
    #st.markdown("# Main page")
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.markdown("#  Main page")
    
    
    st.title("AI-Coach")

    st.sidebar.header("Instuctions")
    st.sidebar.info("This is a demo of an AI-Coach. You can ask it anything, but it's best at answering questions about the world and its current state.")
    API_0 = st.secrets["api_key"]
    modus = st.sidebar.selectbox(label= 'Modus', options=["Journaling questions", "Analysis", "Therapy Chatbot"])
    # automatisches auswählen? Word embeddings immer ada.
    model = st.sidebar.selectbox(label= 'Model', options=["gpt-3.5-turbo", "text-davinci-003", "text-ada-001"])
    st.sidebar.info("Select a model according your task.")

    # 1. get text input from user

    def get_text():

        journal_text = st.text_input("Please import your Journal entries here as plain text: ", placeholder="Your journal text here.") #, label_visibility="hidden")
        return journal_text



    def journal_analytics(journal_entry):
        prompt = f"""You are in the position of a therapist reading over journal entries.
                    Goals:
                    1. Help people to overcome the things which are holding them back.
                    2. Discover recurring patterns.
                    3. Read over journal entries, analyze and find patterns the patient is struggling with.

                    Journal entry: {journal_entry}

                    Tasks:
                    1. What patterns can you discover?
                    2. Give me the sentiment related to people occuring in the journal.
        """

        st.text("\nOutput:\n" + llm(prompt))
        return prompt

    def ich_aktie(table):

        st.line_chart(table)

    # 2. create OpenAI instance

    llm = OpenAI(
        temperature=0,
        openai_api_key=API_0,
        model_name = model
    )

    # get user input
    #user_input = get_text()

    # generate output
    #if user_input:
     #   st.text(llm(user_input))


    def main():

        # get journal entries from user
        ## copy and paste from journal
        user_input = get_text()
        if st.button("Send"):
            #st.text("Prompt: " + new_prompt + "\n\nPrompt for GPT: " + journal_analytics(user_input))
            st.text("This is the original prompt: " + journal_analytics(user_input))

        ## upload file
        uploaded_file = st.file_uploader("Choose a .txt file", type="txt")
        if uploaded_file is not None:
            for line in uploaded_file:
                st.text(line)


        # slider for datetime for chart
        timeframe = st.slider("Select timeframe of Journal entries",
                              value=(datetime(2021, 1, 1), datetime(2021, 1, 31)),
                                format="DD/MM/YYYY")
        #st.write("Select start and end date: ", timeframe)

        # call function to generate linechart
        if st.button("Generate chart"):
            st.text("This is the chart: ")
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c'])
            ich_aktie(chart_data)





    if __name__ == "__main__":
        main()



    # TODO:
    # chatbot anpassen
    # jounrnal in langzeit speicher (langchain, pinecone, etc.)
    # Analyse, auch grafisch
    # tabelle



