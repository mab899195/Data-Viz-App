import streamlit as st
import plotly.express as px
import pandas as pd

# Add a title
st.title("Data Analytics App")
st.subheader("Data visualization")

st.sidebar.image(r"Sixense_digital_logo.jpg", width=280)  # Adjust the width as needed

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

# Data overview function
def data_overview():
    if st.session_state.df is not None:  # Check if the DataFrame exists
        
        # Sidebar checkboxes for each section
        st.sidebar.divider()
        st.sidebar.subheader("Overview Settings")
        show_head = st.sidebar.checkbox("Show the first rows of the dataset")
        show_columns = st.sidebar.checkbox("Show the dataset columns")
        show_summary = st.sidebar.checkbox("Show data summarization")
        show_missing = st.sidebar.checkbox("Show missing values by column")
        show_duplicates = st.sidebar.checkbox("Show duplicate rows")
        show_correlation_matrix = st.sidebar.checkbox("Show correlation matrix")
        show_correlation_heatmap = st.sidebar.checkbox("Show correlation heatmap")
        
        if show_head:
            st.subheader("**Data Overview**")
            st.write("The first rows of your dataset look like this:")
            st.write(st.session_state.df.head())
        
        if show_columns:
            st.write("The different columns of the dataset are:")
            # Convert the column names to a DataFrame
            columns_df = pd.DataFrame(st.session_state.df.columns)
            # Rename the index to 'Column #' and the second column to 'Name'
            columns_df.rename_axis('Column #', inplace=True)
            columns_df.columns = ['Name']  # Rename the columns of the DataFrame
            
            st.write(columns_df)
        
        if show_summary:
            st.write("**Data Summarization**")
            st.write(st.session_state.df.describe())
        
        if show_missing:
            # Calculate and display missing values
            missing_values_per_column = st.session_state.df.isnull().sum()
            st.write("**Missing Values by Column**")
            st.write(missing_values_per_column)
            
            total_missing_values = missing_values_per_column.sum()
            st.write(f"There are {total_missing_values} missing values in this dataset.")
        
        if show_duplicates:
            # Check for and display duplicates
            st.write("**Duplicate Rows**")
            duplicate_rows = st.session_state.df[st.session_state.df.duplicated()]
            if not duplicate_rows.empty:
                st.write(f"There are {len(duplicate_rows)} duplicate rows in the dataset.")
                st.write("The duplicate rows are:")
                st.write(duplicate_rows)
            else:
                st.write("There are no duplicate rows in the dataset.")
        
        if show_correlation_matrix:
            # Calculate and display correlations
            st.write("**Correlation Matrix**")
            correlation_matrix = st.session_state.df.corr()
            st.write(correlation_matrix)
        else:
            correlation_matrix = None
        
        if show_correlation_heatmap and show_correlation_matrix:
            # Visualize the correlation matrix using a heatmap
            st.write("**Correlation Heatmap**")
            if correlation_matrix is not None:
                fig = px.imshow(correlation_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
                st.plotly_chart(fig)
    
    else:
        st.write("No data available. Please upload a file to see the overview.")

data_overview()




