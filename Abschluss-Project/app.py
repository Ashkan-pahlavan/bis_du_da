import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

df_path = f"Attendance/Attendance_{date}.csv"
if os.path.isfile(df_path):
    df = pd.read_csv(df_path)
    st.dataframe(df.style.highlight_max(axis=0))
else:
    st.write("No attendance data available for today.")
