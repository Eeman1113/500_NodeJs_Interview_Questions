import streamlit as st
import pandas as pd
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Node.js Interview Questions Explorer",
    page_icon="❓",
    layout="wide",
)

# --- Title and Description ---
st.title("Node.js Interview Questions Explorer")
st.markdown("""
Welcome to the interactive explorer for all 500 Node.js interview questions. 
Use the sidebar to filter by category or the search bar to find specific questions.
""")

# --- Main Application Logic ---
try:
    # Load the data from the local CSV file, using the first row as the header
    df = pd.read_csv('./index.csv', header=0)
    
    # --- Data Cleaning and Preparation ---
    # Assign names to all three columns to ensure consistency
    df.columns = ["Category", "Question", "Answer"]
    
    # FIX: Forward-fill the category to associate it with all questions in a group.
    # First, replace any blank strings in 'Category' with NaN so ffill works
    df['Category'].replace('', np.nan, inplace=True)
    df['Category'].ffill(inplace=True)

    # Ensure all data in 'Category' column is treated as a string
    df['Category'] = df['Category'].astype(str)
    
    # Clean the data by stripping whitespace
    df['Category'] = df['Category'].str.strip()
    df['Question'] = df['Question'].str.strip()

    # Handle potential missing answers
    df["Answer"] = df["Answer"].fillna("No answer provided.")
    # Only drop rows if the question itself is empty to avoid data loss
    df.dropna(subset=["Question"], inplace=True) 

    # Create a sortable numeric column from the question number.
    df['Question_Num'] = pd.to_numeric(df['Question'].str.split('.').str[0], errors='coerce')
    
    # --- Sidebar Filters ---
    st.sidebar.header("Category")

    # Filter by Category using radio buttons
    # FIX: Use .unique() to preserve the original order from the file, preventing incorrect alphabetical sorting
    categories = df['Category'].unique().tolist()
    category_options = ["All Categories"] + categories
    
    selected_category = st.sidebar.radio(
        'Filter by Category:',
        options=category_options,
        label_visibility="collapsed" # Hides the 'Filter by Category:' label for a cleaner look
    )

    # Filter the dataframe based on the selected category
    if selected_category == "All Categories":
        filtered_df = df
    else:
        filtered_df = df[df['Category'] == selected_category]

    # --- Search Functionality (in main panel) ---
    search_term = st.text_input(
        "Search within the selected category:",
        placeholder="e.g., 'event loop' or 'What is npm?'"
    )

    if search_term:
        # Apply search on the already category-filtered dataframe
        filtered_df = filtered_df[
            filtered_df['Question'].str.contains(search_term, case=False, na=False) |
            filtered_df['Answer'].str.contains(search_term, case=False, na=False)
        ]

    # --- Main Panel Display ---
    st.header("Explore the Questions")
    st.write(f"Displaying {len(filtered_df)} of 500 total questions.")
    
    if not filtered_df.empty:
        # Sort the filtered dataframe by the extracted question number
        sorted_df = filtered_df.sort_values(by='Question_Num')

        # Display the filtered and sorted data in a question/answer format
        for index, row in sorted_df.iterrows():
            st.markdown(f"### {row['Question']}")
            # Use markdown with custom styling for a larger answer font
            st.markdown(f"<div style='font-size: 1.1em;'><b>Answer:</b> {row['Answer']}</div>", unsafe_allow_html=True)
            st.divider() # Adds a visual separator between questions
    
    else:
        st.warning("No questions match your current filter or search criteria.")

except FileNotFoundError:
    st.error("Error: `index.csv` not found.")
    st.info("Please make sure the `index.csv` file is in the same directory as your Streamlit app (`app.py`).")
except Exception as e:
    st.error(f"An error occurred while processing the file: {e}")
    st.warning("Please ensure your CSV file is formatted correctly.")
