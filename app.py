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

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")

    # Filter by Category using radio buttons
    categories = sorted(df['Category'].unique())
    # Add an 'All' option to the list of categories
    category_options = ["All Categories"] + categories
    
    selected_category = st.sidebar.radio(
        'Filter by Category:',
        options=category_options,
    )

    # Filter the dataframe based on the selected category
    if selected_category == "All Categories":
        filtered_df = df
    else:
        filtered_df = df[df['Category'] == selected_category]

    # Search functionality
    search_term = st.sidebar.text_input("Search in Questions or Answers:")
    if search_term:
        # Apply search on the already category-filtered dataframe
        # Case-insensitive search
        filtered_df = filtered_df[
            filtered_df['Question'].str.contains(search_term, case=False, na=False) |
            filtered_df['Answer'].str.contains(search_term, case=False, na=False)
        ]

    # --- Main Panel Display ---
    st.header("Explore the Questions")
    # Updated the total question count to 500 as requested
    st.write(f"Displaying {len(filtered_df)} of 500 total questions.")
    
    if not filtered_df.empty:
        # Display the filtered data in a question/answer format
        for index, row in filtered_df.iterrows():
            st.markdown(f"## {row['Question']}")
            st.markdown(f"**Answer:** {row['Answer']}")
            st.divider() # Adds a visual separator between questions
        
        # --- Visualizations ---
        st.header("Visual Insights")
        
        # Bar chart for question count by category (based on the original full dataframe)
        st.subheader("Total Questions per Category")
        
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
