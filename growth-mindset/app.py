import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO 

# Title of the app
st.title("Growth Mindset Challenge 🚀💡")
st.write("Welcome! 🌱")


# File upload functionality
uploaded_file = st.file_uploader("Upload your CSV, Excel or any sheet file📈", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # Read the file (Pandas can handle both CSV and Excel)
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Display data preview
    st.write("Data Preview📝:")
    st.dataframe(df.head())  # Shows the first few rows of the uploaded file

    # Data analysis options
    st.sidebar.header("Analyze Data🔍")
    chart_type = st.sidebar.selectbox("Select chart type", ["Line Chart", "Bar Chart", "Pie Chart", "Scatter Plot"])

    if chart_type == "Line Chart":
        st.subheader("Line Chart📊")
        st.line_chart(df)

    elif chart_type == "Bar Chart":
        st.subheader("Bar Chart📊")
        st.bar_chart(df)

    elif chart_type == "Pie Chart":
        st.subheader("Pie Chart🍰")
        # Assuming the user wants to plot a pie chart of a specific column
        column_name = st.selectbox("Select Column for Pie Chart", df.columns)
        pie_data = df[column_name].value_counts()
        fig = plt.figure(figsize=(6, 6))
        plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        st.pyplot(fig)

    elif chart_type == "Scatter Plot":
        st.subheader("Scatter Plot📍")
        x_axis = st.selectbox("Select X-axis", df.columns)
        y_axis = st.selectbox("Select Y-axis", df.columns)
        fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
        st.plotly_chart(fig)

    # Allow users to download the data
    st.sidebar.subheader("Export Data📥")
    file_format = st.sidebar.selectbox("Select export format", ["CSV", "Excel"])
    
    if file_format == "CSV":
        st.sidebar.download_button(
            label="Download CSV 🗂️",
            data=df.to_csv(index=False),
            file_name="data.csv",
            mime="text/csv"
        )
    elif file_format == "Excel":
        # Create a BytesIO buffer
        excel_buffer = BytesIO()

        # Use ExcelWriter to write the DataFrame to the buffer
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Get the Excel file as bytes
        excel_data = excel_buffer.getvalue()

        # Provide the download button for Excel
        st.sidebar.download_button(
            label="Download Excel 📄",
            data=excel_data,
            file_name="data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )