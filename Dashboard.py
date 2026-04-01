import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="UberEats DashBoard", layout="wide")

#st.set_page_config(layout="wide")
st.title("🍔 Filtered Uber Eats Data")

try:
    conn = sqlite3.connect('ubereats_data.db')
    # we have used Dynamic Query to filter the data in the data table based on the 
    # data selected in the dropdown lists
    # 1. Fetch all column names
    cols_query = "PRAGMA table_info(restaurants)"
    cols_df = pd.read_sql_query(cols_query, conn)
    all_columns = cols_df['name'].tolist()

    # 2. REMOVE 'restaurant_id' from the list
    # This filters out the ID so users don't see it in the dropdown
    column_list = [col for col in all_columns if col != 'restaurant_id']

    # --- Sidebar Filters ---
    selected_col = st.sidebar.selectbox("1. Choose Column", column_list)

    # 3. Fetch unique values for the selected column
    val_query = f"SELECT DISTINCT \"{selected_col}\" FROM restaurants WHERE \"{selected_col}\" IS NOT NULL"
    unique_values = pd.read_sql_query(val_query, conn)[selected_col].tolist()
    selected_val = st.sidebar.selectbox(f"2. Choose Value", unique_values)

    # --- Display in 80% Width ---
    left, middle, right = st.columns([1, 8, 1])

    with middle:
        # Run the final filtered query
        filter_query = f"SELECT * FROM restaurants WHERE \"{selected_col}\" = ?"
        df_result = pd.read_sql_query(filter_query, conn, params=[selected_val])
        
        st.write(f"Results for **{selected_col}**: {selected_val}")
        st.dataframe(df_result, use_container_width=True)

    conn.close()

except Exception as e:
    st.error(f"Error: {e}")