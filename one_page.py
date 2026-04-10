import streamlit as st
import pandas as pd
import sqlite3

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="UberEats Dashboard", layout="wide")

# --------------------------------------------------
# DB FUNCTION
# --------------------------------------------------
def run_query(db, query, params=None):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Select Page", [
    "🍔 Filter Data",
    "📊 Restaurant Analysis",
    "📦 Orders Analysis"
])

# ==================================================
# 🍔 PAGE 1: FILTER DATA
# ==================================================
if page == "🍔 Filter Data":

    st.title("🍔 Filtered Uber Eats Data")

    try:
        conn = sqlite3.connect('ubereats_data.db')

        cols_df = pd.read_sql_query("PRAGMA table_info(restaurants)", conn)
        column_list = [col for col in cols_df['name'] if col != 'restaurant_id']

        selected_col = st.sidebar.selectbox("1. Choose Column", column_list)

        val_query = f'SELECT DISTINCT "{selected_col}" FROM restaurants WHERE "{selected_col}" IS NOT NULL'
        unique_values = pd.read_sql_query(val_query, conn)[selected_col].tolist()

        selected_val = st.sidebar.selectbox("2. Choose Value", unique_values)

        left, middle, right = st.columns([1, 8, 1])

        with middle:
            query = f'SELECT * FROM restaurants WHERE "{selected_col}" = ?'
            df = pd.read_sql_query(query, conn, params=[selected_val])

            st.write(f"Results for **{selected_col}**: {selected_val}")
            st.dataframe(df, use_container_width=True)

        conn.close()

    except Exception as e:
        st.error(f"Error: {e}")


# ==================================================
# 📊 PAGE 2: RESTAURANT ANALYSIS (10 QUESTIONS)
# ==================================================
elif page == "📊 Restaurant Analysis":

    st.title("📊 Restaurant Business Analysis Q&A")

    analysis_queries = {
        "1. Highest rating locations":
        "SELECT location, ROUND(avg(rate),2) as avg_rate FROM restaurants GROUP BY location ORDER BY avg_rate DESC LIMIT 10;",

        "2. Over-saturated locations":
        "SELECT location, COUNT(*) as rest_count FROM restaurants GROUP BY location ORDER BY rest_count DESC LIMIT 10;",

        "3. Online ordering vs rating":
        "SELECT online_order , ROUND(avg(rate),2) as avg_rate FROM restaurants GROUP BY online_order ORDER BY avg_rate;",

        "4. Table booking vs rating":
        "SELECT book_table , ROUND(avg(rate),2) as avg_rate FROM restaurants GROUP BY book_table ORDER BY avg_rate;",

        "5. Price segment vs rating":
        """SELECT 
        CASE 
        WHEN approx_two_person_cost <= 500 THEN 'Low'
        WHEN approx_two_person_cost BETWEEN 501 AND 1500 THEN 'Mid'
        ELSE 'Premium'
        END AS segment,
        ROUND(AVG(rate),2) as avg_rating
        FROM restaurants
        GROUP BY segment;""",

        "6. Most common cuisines":
        """WITH RECURSIVE split(cuisine, rest) AS (
        SELECT NULL, cuisines || ',' FROM restaurants
        UNION ALL
        SELECT 
        TRIM(SUBSTR(rest,1,INSTR(rest,',')-1)),
        SUBSTR(rest,INSTR(rest,',')+1)
        FROM split WHERE rest!='')
        SELECT cuisine, COUNT(*) as count
        FROM split
        WHERE cuisine!=''
        GROUP BY cuisine
        ORDER BY count DESC LIMIT 10;""",

        "7. Cost vs rating":
        """SELECT 
        CASE 
        WHEN approx_two_person_cost <= 500 THEN 'Budget'
        WHEN approx_two_person_cost <= 1000 THEN 'Mid'
        ELSE 'Premium'
        END AS segment,
        ROUND(AVG(rate),2) as avg_rating
        FROM restaurants
        GROUP BY segment;""",

        "8. Premium locations":
        """SELECT location,
        ROUND(AVG(approx_two_person_cost),2) as avg_cost,
        ROUND(AVG(rate),2) as avg_rating
        FROM restaurants
        GROUP BY location
        ORDER BY avg_cost DESC, avg_rating DESC LIMIT 10;""",

        "9. Online + table booking performance":
        """SELECT online_order, book_table,
        ROUND(AVG(rate),2) as avg_rating,
        COUNT(*) as count
        FROM restaurants
        GROUP BY online_order, book_table;""",

        "10. Top restaurants by segment":
        """SELECT restaurant_name, rate, votes
        FROM restaurants
        ORDER BY rate DESC, votes DESC LIMIT 10;"""
    }

    selected_q = st.selectbox("Select Question", list(analysis_queries.keys()))

    if selected_q:
        query = analysis_queries[selected_q]

        with st.spinner("Running Query..."):
            df = run_query("UberEats_data.db", query)

        st.dataframe(df, use_container_width=True)

        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "restaurant_analysis.csv", "text/csv")


# ==================================================
# 📦 PAGE 3: ORDERS ANALYSIS (5 QUESTIONS)
# ==================================================
elif page == "📦 Orders Analysis":

    st.title("📦 Orders Business Analysis Q&A")

    order_queries = {
        "1. Revenue by restaurant":
        "SELECT restaurant_name, SUM(order_value) as total_revenue FROM orders GROUP BY restaurant_name ORDER BY total_revenue DESC;",

        "2. Popular payment method":
        "SELECT payment_method, COUNT(*) as count FROM orders GROUP BY payment_method ORDER BY count DESC;",

        "3. Discount usage":
        "SELECT COUNT(*) as total_orders, ROUND(AVG(order_value),2) as avg_value FROM orders WHERE discount_used='Yes';",

        "4. Daily orders trend":
        "SELECT order_date, COUNT(*) as daily_orders FROM orders GROUP BY order_date ORDER BY order_date;",

        "5. High AOV restaurants":
        "SELECT restaurant_name, ROUND(AVG(order_value),2) as aov FROM orders GROUP BY restaurant_name HAVING aov > 50;"
    }

    selected_q = st.selectbox("Select Question", list(order_queries.keys()))

    if selected_q:
        query = order_queries[selected_q]

        with st.spinner("Running Query..."):
            df = run_query("UberEats_data.db", query)

        st.dataframe(df, use_container_width=True)

        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "orders_analysis.csv", "text/csv")