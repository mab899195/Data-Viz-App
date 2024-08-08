import streamlit as st
import plotly.express as px
import pandas as pd

# Add a title
st.title("Data Visualization App")

st.sidebar.image(r"https://www.sixense-group.com/wp-content/themes/sixense/img/logo-2.png", width=280)  # Adjust the width as needed

# Add a subheader in the sidebar
st.sidebar.subheader("Visualization Settings")

# Add a file uploader
uploaded_file = st.sidebar.file_uploader(
    label="Upload your CSV or Excel file here",
    type=['csv', 'xlsx']
)

# Add a checkbox to display the dataset
display_data = st.sidebar.checkbox("View the dataset")

# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'numeric_columns' not in st.session_state:
    st.session_state.numeric_columns = []
if 'non_numeric_columns' not in st.session_state:
    st.session_state.non_numeric_columns = []

# Account for cases where uploaded file is not None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            st.session_state.df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            st.session_state.df = pd.read_excel(uploaded_file)
        
        if display_data:
            st.write(st.session_state.df)

        # Extract numeric columns as list
        st.session_state.numeric_columns = list(st.session_state.df.select_dtypes(['float', 'int']).columns)

        # Extract the non-numeric columns
        st.session_state.non_numeric_columns = list(st.session_state.df.select_dtypes(['object']).columns)

        # Append None value to non_numeric list for the color option
        st.session_state.non_numeric_columns.append('None')

    except Exception as e:
        st.error(f"Error: {e}")

# Add a selectbox widget
chart_select = st.sidebar.selectbox(
    label="Select the visualization type",
    options=['Scatterplots', 'Lineplots', 'Histograms']
)

# Create plots based on selection
try:
    if chart_select == 'Scatterplots' and st.session_state.df is not None:
        st.sidebar.subheader("Settings for Scatterplots")
        x_value = st.sidebar.selectbox(label="X axis", options=st.session_state.numeric_columns)
        y_value = st.sidebar.selectbox(label="Y axis", options=st.session_state.numeric_columns)

        specify_color = st.sidebar.checkbox(label="Would you like to specify the color?")

        color_value = 'None'  # Initialize color_value
        if specify_color:
            color_value = st.sidebar.selectbox(label='Color', options=st.session_state.non_numeric_columns)

        if color_value == 'None':
            plot = px.scatter(data_frame=st.session_state.df, x=x_value, y=y_value)
        else:
            plot = px.scatter(data_frame=st.session_state.df, x=x_value, y=y_value, color=color_value)

        # Display chart in Streamlit
        st.plotly_chart(plot)

    if chart_select == 'Histograms' and st.session_state.df is not None:
        st.sidebar.subheader("Settings for Histograms")
        x = st.sidebar.selectbox(label="Feature", options=st.session_state.numeric_columns)
        bin_size = st.sidebar.slider(label="Number of bins", min_value=10, max_value=100, value=50)
        plot = px.histogram(data_frame=st.session_state.df, x=x, nbins=bin_size)
        st.plotly_chart(plot)

    if chart_select == 'Lineplots' and st.session_state.df is not None:
        st.sidebar.subheader("Settings for Lineplots")
        x_value = st.sidebar.selectbox(label='X axis', options=st.session_state.numeric_columns)
        y_value = st.sidebar.selectbox(label='Y axis', options=st.session_state.numeric_columns)

        plot = px.line(data_frame=st.session_state.df, x=x_value, y=y_value)

        # Display the chart
        st.plotly_chart(plot)

except Exception as e:
    st.error(f"Error: {e}")
