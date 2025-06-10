import streamlit as st
import pandas as pd

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
Use the search bar below to filter questions and answers.
""")

# --- Main Application Logic ---
try:
    # Load the data from the local CSV file, assuming no header
    df = pd.read_csv('./index.csv', header=None)
    
    # --- Data Cleaning and Preparation ---
    # Assign names to only the columns we need: Question and Answer
    # This effectively ignores the first 'Category' column
    df = df.iloc[:, 1:] # Keep only the second and third columns
    df.columns = ["Question", "Answer"]
    
    # Handle potential missing answers
    df["Answer"] = df["Answer"].fillna("No answer provided.")
    df.dropna(subset=["Question"], inplace=True) # Only drop rows if the question itself is empty

    # Create a sortable numeric column from the question number.
    # This is more robust and won't drop rows if a question number is missing.
    df['Question_Num'] = pd.to_numeric(df['Question'].str.split('.').str[0], errors='coerce')
    
    # --- Search Functionality (in main panel) ---
    search_term = st.text_input(
        "Search for a specific question or answer:",
        placeholder="e.g., 'event loop' or 'What is npm?'"
    )

    filtered_df = df
    if search_term:
        # Case-insensitive search
        filtered_df = df[
            df['Question'].str.contains(search_term, case=False, na=False) |
            df['Answer'].str.contains(search_term, case=False, na=False)
        ]

    # --- Main Panel Display ---
    st.header("Explore the Questions")
    st.write(f"Displaying {len(filtered_df)} of 500 total questions.")
    
    if not filtered_df.empty:
        # Sort the filtered dataframe by the extracted question number
        # Rows where Question_Num is NaN will be placed last, but not dropped
        sorted_df = filtered_df.sort_values(by='Question_Num')

        # Display the filtered and sorted data in a question/answer format
        for index, row in sorted_df.iterrows():
            st.markdown(f"## {row['Question']}")
            st.markdown(f"**Answer:** {row['Answer']}")
            st.divider() # Adds a visual separator between questions
    
    else:
        st.warning("No questions match your search criteria.")

except FileNotFoundError:
    st.error("Error: `index.csv` not found.")
    st.info("Please make sure the `index.csv` file is in the same directory as your Streamlit app (`app.py`).")
except Exception as e:
    st.error(f"An error occurred while processing the file: {e}")
    st.warning("Please ensure your CSV file is formatted correctly.")
