import streamlit as st
import pandas as pd
import altair as alt

# --- Page Configuration ---
st.set_page_config(
    page_title="Node.js Interview Questions Explorer",
    page_icon="❓",
    layout="wide",
)

# --- Title and Description ---
st.title("Node.js Interview Questions Explorer")
st.markdown("""
Welcome to the interactive explorer for Node.js interview questions. 
This app helps you browse, search, and visualize questions from the `index.csv` dataset.
""")

# --- Main Application Logic ---
try:
    # Load the data from the local CSV file
    # Ensure 'index.csv' is in the same directory as this script.
    df = pd.read_csv('./index.csv')
    
    # --- Data Cleaning and Preparation ---
    # Rename columns for better readability and to handle potential whitespace issues
    df.columns = ["Category", "Question", "Answer"]
    df.columns = df.columns.str.strip()
    
    # Handle potential missing values
    df.dropna(subset=["Category", "Question"], inplace=True)
    df["Answer"] = df["Answer"].fillna("No answer provided.")

    st.success("`index.csv` loaded and processed successfully!")
    
    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")

    # Filter by Category
    categories = sorted(df['Category'].unique())
    selected_categories = st.sidebar.multiselect(
        'Filter by Category:',
        options=categories,
        default=categories
    )

    if not selected_categories:
        st.sidebar.warning("Please select at least one category.")
        filtered_df = pd.DataFrame() # Empty dataframe if nothing is selected
    else:
        filtered_df = df[df['Category'].isin(selected_categories)]

    # Search functionality
    search_term = st.sidebar.text_input("Search in Questions or Answers:")
    if search_term:
        # Case-insensitive search
        filtered_df = filtered_df[
            filtered_df['Question'].str.contains(search_term, case=False, na=False) |
            filtered_df['Answer'].str.contains(search_term, case=False, na=False)
        ]

    # --- Main Panel Display ---
    st.header("Explore the Questions")
    st.write(f"Displaying {len(filtered_df)} of {len(df)} total questions.")
    
    if not filtered_df.empty:
        # Display the filtered data in an interactive table
        st.dataframe(filtered_df, height=600, use_container_width=True)
        
        # --- Visualizations ---
        st.header("Visual Insights")
        
        # Bar chart for question count by category
        st.subheader("Questions per Category")
        
        category_counts = df['Category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        
        chart = alt.Chart(category_counts).mark_bar().encode(
            x=alt.X('Category:N', sort='-y', title="Category"),
            y=alt.Y('Count:Q', title="Number of Questions"),
            tooltip=['Category', 'Count']
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)

    else:
        st.warning("No questions match your current filter or search criteria.")

except FileNotFoundError:
    st.error("Error: `index.csv` not found.")
    st.info("Please make sure the `index.csv` file is in the same directory as your Streamlit app (`app.py`).")
except Exception as e:
    st.error(f"An error occurred while processing the file: {e}")
    st.warning("Please ensure `index.csv` is a valid CSV with the expected columns: Category, Question, Answer.")
