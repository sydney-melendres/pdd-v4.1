import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Demographics Analysis", page_icon="📊")

# File path
csv_file = 'survey-data/demographics.csv'

# Function to plot pie chart for a categorical column
def plot_pie_chart(column_name, df):
    # Count unique values for the column, excluding NaN
    counts = df[column_name].value_counts(dropna=True)
    
    # Create a new figure
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plotting the pie chart
    counts.plot.pie(autopct='%1.1f%%', startangle=140, ax=ax)
    ax.set_title(f'Distribution of {column_name}')
    ax.set_ylabel('')  # Remove the default ylabel 'column_name'
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    return fig

# Load data
@st.cache_data
def load_data():
    return pd.read_csv(csv_file)

# Main content
st.title('Participant Demographics Analysis')
st.info('Pie Charts of Demographics Data')

# Load the data
df = load_data()

if df is not None:
    # Display column selection and pie charts
    columns_to_plot = st.multiselect(
        'Select Columns to Plot', 
        df.columns, 
        default="What platforms do you use to play games? (e.g., PC, console, mobile)"
    )
    
    if columns_to_plot:
        for column in columns_to_plot:
            fig = plot_pie_chart(column, df)
            st.pyplot(fig)
else:
    st.error("Failed to load the data. Please check the file path and try again.")