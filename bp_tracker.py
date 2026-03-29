import streamlit as st
import pandas as pd
import datetime
import os

DATA_FILE = "bp_log_twice_daily.csv"

# Initialize CSV with a 'Session' column
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Session", "Systolic", "Diastolic", "Pulse", "Notes"])
    df.to_csv(DATA_FILE, index=False)

st.title("15-Day BP Tracker (AM/PM)")

# Sidebar for Data Entry
st.sidebar.header("Log Reading")
date = st.sidebar.date_input("Date", datetime.date.today())

# Selection for Morning or Evening
session = st.sidebar.selectbox("Session", ["Morning (AM)", "Evening (PM)"])

systolic = st.sidebar.number_input("Systolic (Top)", 50, 250, 120)
diastolic = st.sidebar.number_input("Diastolic (Bottom)", 30, 150, 80)
pulse = st.sidebar.number_input("Pulse (BPM)", 30, 200, 72)
notes = st.sidebar.text_input("Notes (e.g., after meds)")

if st.sidebar.button("Save Entry"):
    new_data = pd.DataFrame([[date, session, systolic, diastolic, pulse, notes]], 
                            columns=["Date", "Session", "Systolic", "Diastolic", "Pulse", "Notes"])
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.sidebar.success(f"{session} reading saved!")
    st.rerun()

# Load Data
df = pd.read_csv(DATA_FILE)

if not df.empty:
    # Display the table formatted for 15 days (30 entries total)
    st.subheader("Last 15 Days of Records")
    st.dataframe(df.tail(30), use_container_width=True)

    # Visualization: Comparing AM vs PM
    st.subheader("AM vs PM Trends")
    
    # Pivot data for a better chart view
    chart_df = df.tail(30).copy()
    chart_df['Label'] = chart_df['Date'].astype(str) + " (" + chart_df['Session'] + ")"
    
    st.line_chart(chart_df.set_index('Label')[['Systolic', 'Diastolic']])

    # Delete Options
    st.sidebar.markdown("---")
    if st.sidebar.button("Delete Last Entry"):
        df[:-1].to_csv(DATA_FILE, index=False)
        st.rerun()
        
    if st.sidebar.button("Clear All Logs"):
        pd.DataFrame(columns=df.columns).to_csv(DATA_FILE, index=False)
        st.rerun()
else:
    st.info("Start by logging your Morning or Evening reading in the sidebar.")