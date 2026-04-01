#SELECT location, avg(rate) as avg_rate from restaurants GROUP By location ORDER BY avg_rate DESC limit 10;
#SELECT location, COUNT(*) as rest_count from restaurants GROUP By location ORDER BY rest_count DESC limit 10;
#SELECT online_order , avg(rate) as avg_rate from restaurants Group By online_order ORDER By avg_rate;
#SELECT book_table , avg(rate) as avg_rate from restaurants Group By book_table ORDER By avg_rate;
# SELECT 
#     CASE 
#         WHEN approx_two_person_cost <= 500 THEN 'Low-Priced (<₹500)'
#         WHEN approx_two_person_cost BETWEEN 501 AND 1500 THEN 'Mid-Priced (₹500-₹1500)'
#         ELSE 'Premium-Priced (>₹1500)'
#     END AS price_segment,
#     ROUND(AVG(rate), 2) AS average_rating,
#     COUNT(restaurant_id) AS total_restaurants
# FROM restaurants
# WHERE rate IS NOT NULL
# GROUP BY price_segment
# ORDER BY average_rating DESC;
# WITH RECURSIVE split_cuisines(cuisine, remaining) AS (
#     -- Initial Step: Get the full string and append a comma to help with parsing
#     SELECT 
#         NULL, 
#         cuisines || ',' 
#     FROM restaurants 
   
#     UNION ALL
    
#     -- Recursive Step: Extract the first cuisine before the first comma
#     SELECT 
#         TRIM(SUBSTR(remaining, 1, INSTR(remaining, ',') - 1)),
#         SUBSTR(remaining, INSTR(remaining, ',') + 1)
#     FROM split_cuisines
#     WHERE remaining != ''
# )
# -- Final Output: Group by the extracted unique cuisines
# SELECT 
#     cuisine, 
#     COUNT(*) AS restaurant_count
# FROM split_cuisines
# WHERE cuisine IS NOT NULL AND cuisine != ''
# GROUP BY cuisine
# ORDER BY restaurant_count DESC limit 10;
# SELECT 
#     CASE 
#         WHEN approx_two_person_cost <= 500 THEN 'Budget (0-500)'
#         WHEN approx_two_person_cost <= 1000 THEN 'Mid-Range (501-1000)'
#         WHEN approx_two_person_cost <= 2000 THEN 'Premium (1001-2000)'
#         ELSE 'Luxury (2000+)'
#     END AS price_segment,
#     ROUND(AVG(rate), 2) AS average_rating,
#     COUNT(*) AS restaurant_count
# FROM 
#     restaurants
# WHERE 
#     rate IS NOT NULL 
  
# GROUP BY 
#     price_segment
# ORDER BY 
#     AVG(approx_two_person_cost) ASC;

#     SELECT 
#     location, 
#     ROUND(AVG(approx_two_person_cost),2) AS avg_cost, 
#     ROUND(AVG(rate),2) AS avg_rating,
#     COUNT(*) AS restaurant_count
# FROM 
#     restaurants

# GROUP BY 
#     location

# ORDER BY 
#     avg_cost DESC,
#     avg_rating DESC
#     LIMIT 10;

#  SELECT 
#     online_order,
#     book_table,
#     ROUND(AVG(rate), 2) AS average_rating,
#     ROUND(AVG(votes), 2) AS average_votes,
#     COUNT(*) AS restaurant_count
# FROM restaurants
# WHERE rate IS NOT NULL
# GROUP BY online_order, book_table
# ORDER BY average_rating DESC;

# SELECT * FROM (
#     SELECT 'Low' AS segment, restaurant_name, rate, votes 
#     FROM restaurants WHERE approx_two_person_cost <= 500 
#     ORDER BY rate DESC, votes DESC LIMIT 3
# ) AS low_tier

# UNION ALL

# SELECT * FROM (
#     SELECT 'Mid' AS segment, restaurant_name, rate, votes 
#     FROM restaurants WHERE approx_two_person_cost BETWEEN 501 AND 1500 
#     ORDER BY rate DESC, votes DESC LIMIT 3
# ) AS mid_tier

# UNION ALL

# SELECT * FROM (
#     SELECT 'Premium' AS segment, restaurant_name, rate, votes 
#     FROM restaurants WHERE approx_two_person_cost > 1500 
#     ORDER BY rate DESC, votes DESC LIMIT 3
# ) AS premium_tier;


import streamlit as st
import pandas as pd
import sqlite3

# We have used the Dictionary object to populate the dropdown list
# And to execute the query for the business analysis questions
# 1. Configuration & Styling
st.set_page_config(page_title="UberEats Business Intelligence Q&A", layout="wide")

# 2. Database Connection Helper
def run_query(query):
    # Replace 'business_data.db' with your actual database file or connection string
    conn = sqlite3.connect('UberEats_data.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 3. Define the 10 Predefined Business Questions & SQL
# Format: { "Display Question": "SQL Query" }
analysis_queries = {
    """1.	Which Bangalore locations have the highest average restaurant ratings?
            Business Value: Identifies premium-performing areas suitable for brand positioning and new partner onboarding."""
 
            : "SELECT location, ROUND(avg(rate),2) as avg_rate from restaurants GROUP By location ORDER BY avg_rate DESC limit 10;",
        
    """2.	Which locations are over-saturated with restaurants?
            Business Value: Helps avoid overcrowded markets and guides smarter expansion decisions."""

            : "SELECT location, COUNT(*) as rest_count from restaurants GROUP By location ORDER BY rest_count DESC limit 10;",
            
    """ 3.	Does online ordering improve restaurant ratings?
            Business Value: Evaluates the ROI of Uber Eats online ordering feature for partners."""
            
            : "SELECT online_order , ROUND(avg(rate),2) as avg_rate from restaurants Group By online_order ORDER By avg_rate;",
            
            
    """ 4 .	Does table booking correlate with higher customer ratings?
            Business Value: Measures the effectiveness of table booking as a premium feature."""

            : "SELECT book_table , ROUND(avg(rate),2) as avg_rate from restaurants Group By book_table ORDER By avg_rate;",
            
    """ 6.	How do low, mid, and premium-priced restaurants perform in terms of ratings?
            Business Value: Supports pricing-based market segmentation strategies."""

            
            : """SELECT 
              CASE 
              WHEN approx_two_person_cost <= 500 THEN 'Low-Priced (<₹500)'
              WHEN approx_two_person_cost BETWEEN 501 AND 1500 THEN 'Mid-Priced (₹500-₹1500)'
              ELSE 'Premium-Priced (>₹1500)'
              END AS price_segment,
              ROUND(AVG(rate), 2) AS average_rating,
              COUNT(restaurant_id) AS total_restaurants
              FROM restaurants
              WHERE rate IS NOT NULL
              GROUP BY price_segment
              ORDER BY average_rating DESC;""",
              
    """ 7.	Which cuisines are most common in Bangalore?
            Business Value: Reveals market demand and cuisine saturation levels."""
            
           : """
            WITH RECURSIVE split_cuisines(cuisine, remaining) AS (
                -- Initial Step: Get the full string and append a comma
                SELECT 
                    NULL, 
                    cuisines || ',' 
                FROM restaurants 
                    UNION ALL
                
                -- Recursive Step: Extract the first cuisine before the first comma
                SELECT 
                    TRIM(SUBSTR(remaining, 1, INSTR(remaining, ',') - 1)),
                    SUBSTR(remaining, INSTR(remaining, ',') + 1)
                FROM split_cuisines
                        WHERE remaining != ''
                    )
                    -- Final Output: Group by the extracted unique cuisines
                    SELECT 
                        cuisine, 
                        COUNT(*) AS restaurant_count
                    FROM split_cuisines
                    WHERE cuisine IS NOT NULL AND cuisine != ''
                    GROUP BY cuisine
                    ORDER BY restaurant_count DESC 
                    LIMIT 10;
                    """,
                    
    """ 10.	What is the relationship between restaurant cost and rating?
                Business Value: Determines whether higher pricing translates to better customer perception"""
                
            :"""SELECT 
                CASE 
                    WHEN approx_two_person_cost <= 500 THEN 'Budget (0-500)'
                    WHEN approx_two_person_cost <= 1000 THEN 'Mid-Range (501-1000)'
                    WHEN approx_two_person_cost <= 2000 THEN 'Premium (1001-2000)'
                    ELSE 'Luxury (2000+)'
                END AS price_segment,
                ROUND(AVG(rate), 2) AS average_rating,
                COUNT(*) AS restaurant_count
                FROM  restaurants
                WHERE rate IS NOT NULL 
                GROUP BY price_segment
                ORDER BY AVG(approx_two_person_cost) ASC;""" ,
                
                
    """11.	Which locations are ideal for premium restaurant onboarding?
            Business Value: Combines cost, rating, and location insights to guide premium """
            
            :""" SELECT 
                location, 
                ROUND(AVG(approx_two_person_cost),2) AS avg_cost, 
                ROUND(AVG(rate),2) AS avg_rating,
                COUNT(*) AS restaurant_count
                FROM 
                    restaurants

                GROUP BY 
                    location

                ORDER BY 
                    avg_cost DESC,
                    avg_rating DESC
                    LIMIT 10; """,
                    
        """13.	Do restaurants offering both online ordering and table booking perform better?
                Business Value: Validates bundled feature adoption for partners."""


             : """SELECT 
                    online_order,
                    book_table,
                    ROUND(AVG(rate), 2) AS average_rating,
                    ROUND(AVG(votes), 2) AS average_votes,
                    COUNT(*) AS restaurant_count
                    FROM restaurants
                    WHERE rate IS NOT NULL
                    GROUP BY online_order, book_table
                    ORDER BY average_rating DESC;""",
        """15.	Which restaurants are top performers within each pricing segment?
                Business Value: Helps identify benchmark partners and best practices."""
            
                   
            :""" SELECT * FROM (
                        SELECT 'Low' AS segment, restaurant_name, rate, votes 
                        FROM restaurants WHERE approx_two_person_cost <= 500 
                        ORDER BY rate DESC, votes DESC LIMIT 3
                    ) AS low_tier

                    UNION ALL

                    SELECT * FROM (
                        SELECT 'Mid' AS segment, restaurant_name, rate, votes 
                        FROM restaurants WHERE approx_two_person_cost BETWEEN 501 AND 1500 
                        ORDER BY rate DESC, votes DESC LIMIT 3
                    ) AS mid_tier

                    UNION ALL

                    SELECT * FROM (
                        SELECT 'Premium' AS segment, restaurant_name, rate, votes 
                        FROM restaurants WHERE approx_two_person_cost > 1500 
                        ORDER BY rate DESC, votes DESC LIMIT 3
                    ) AS premium_tier;""" 
}

def main():
    st.title("📊 Uber Eats Business Analysis Q&A")
    st.info("Select a question from the list below to run the real-time SQL analysis.")
    
    

    # 4. Dropdown Selection
    selected_question = st.selectbox(
        "Which analysis would you like to view?",
        options=list(analysis_queries.keys())
    )

    # 5. Computation & Result Display
    if selected_question:
        st.subheader(f"Analysis: {selected_question}")
        
        query = analysis_queries[selected_question]
        
        try:
            # SQL-based computation
            with st.spinner('Running SQL Query...'):
                results_df = run_query(query)
            
            # Presentation in structured table
            st.dataframe(
                results_df, 
                use_container_width=True, 
                hide_index=True
            )
            
            # Optional: Add a CSV download button for the specific result
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results as CSV", csv, "analysis.csv", "text/csv")

        except Exception as e:
            st.error(f"Execution Error: {e}")

if __name__ == "__main__":
    main()