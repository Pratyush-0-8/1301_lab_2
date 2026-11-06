# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)


st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")


with st.form("survey_form"):

    category_input = st.text_input("What is your favorite music genre?")
    value_input = st.text_input("How many hours do you listen to music per week?")


    submitted = st.form_submit_button("Submit Data")


    if submitted:
        if category_input.strip() == "" or value_input.strip() == "":
            st.warning("Please fill out both fields.")

        elif not value_input.isdigit():
            st.warning("Please enter a valid number of hours.")

        else:
            with open("data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([category_input, value_input])

            st.success("Your data has been submitted!")
            st.write(f"Genre: {category_input}, Hours: {value_input}")



st.divider() 
st.header("Current Data in CSV")


if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:

    current_data_df = pd.read_csv('data.csv')

    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")