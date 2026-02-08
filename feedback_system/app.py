import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(layout="wide", page_title="Feedback System")

tab1, tab2 = st.tabs(["User Dashboard", "Admin Dashboard"])

# ---------------- USER DASHBOARD ----------------
with tab1:
    st.header("Submit Your Review")

    rating = st.selectbox("Rating", [1, 2, 3, 4, 5])
    review = st.text_area("Write your review", height=150)

    if st.button("Submit Review"):
        if not review.strip():
            st.error("Please write a review before submitting!")
        else:
            try:
                with st.spinner("Processing your review with AI..."):
                    res = requests.post(
                        f"{API_URL}/submit",
                        json={"rating": rating, "review": review},
                        timeout=120
                    )
                    res.raise_for_status()
                    
                st.success("Review submitted successfully!")
                st.write("**AI Response:**")
                st.write(res.json().get("ai_response", "No response generated"))
            except requests.exceptions.ConnectionError:
                st.error("Error: Cannot connect to backend API. Make sure the backend is running on http://localhost:8000")
            except Exception as e:
                st.error(f"Error submitting review: {str(e)}")

# ---------------- ADMIN DASHBOARD ----------------
with tab2:
    st.header("Admin Dashboard")

    try:
        data = requests.get(f"{API_URL}/admin", timeout=10).json()
        
        if not data:
            st.info("No reviews submitted yet.")
        else:
            df = pd.DataFrame(
                data,
                columns=["Rating", "Review", "AI Summary", "Recommended Action"]
            )

            st.dataframe(df, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Reviews", len(df))
            with col2:
                avg_rating = df["Rating"].mean()
                st.metric("Average Rating", f"{avg_rating:.1f}/5")
            
            st.subheader("Rating Distribution")
            rating_counts = df["Rating"].value_counts().sort_index()
            st.bar_chart(rating_counts)
    except requests.exceptions.ConnectionError:
        st.error("Error: Cannot connect to backend API. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        st.error(f"Error loading admin data: {str(e)}")
