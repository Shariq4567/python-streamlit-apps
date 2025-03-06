import streamlit as st
import numpy as np
from io import BytesIO
import os
import pandas as pd

st.set_page_config(page_title="Extension Changer", layout="wide")
st.title("Change Extension of Files")
st.subheader("Interchange between .csv and .xlsx files")
uploaded_files = st.file_uploader("Upload Files", type=['csv', 'xlsx'], accept_multiple_files=True)
if(uploaded_files):
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1]
        if(file_ext == ".csv"):
            df = pd.read_csv(file)
        elif(file_ext == ".xlsx"):
            df = pd.read_excel(file)
        else:
            st.error("Please upload csv or xlsx files only")
            continue

    st.write("**First 5 Rows of the Dataframe**")
    st.dataframe(df.head())

    st.subheader("Data Cleaning Options")
    
    if st.checkbox(f"Clean Data for {file.name}"):
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates Removed")

        with col2:
            if st.button(f"Fill Missing Values from {file.name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing Values Filled")

    st.subheader("Select columns to save")
    selected_columns = st.multiselect("Select Columns", df.columns, default=df.columns)
    df = df[selected_columns]

    st.subheader("Data Visualization Options")
    if st.checkbox("Show Data Summary"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

    st.subheader("Conversion Options")
    convert_to = st.selectbox("Convert to", [".csv", ".xlsx"], key=file.name)
    if st.button(f"Convert to {convert_to}"):
        buffer = BytesIO()
        if convert_to == ".csv":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(".xlsx", ".csv")
            mime_type = "text/csv"
        elif convert_to == ".xlsx":
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(".csv", ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)
    
        st.download_button(label=f"Click to Download {file_name}", data=buffer, file_name=file_name, mime=mime_type)