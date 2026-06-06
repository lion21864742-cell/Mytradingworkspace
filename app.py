import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_autorefresh import st_autorefresh

from modules.database import *
from modules.quotes import *
from modules.portfolio import *

st.set_page_config(
    page_title="Portfolio Manager Pro",
    layout="wide"
)

init_db()

st_autorefresh(
    interval=60000,
    key="refresh"
)

st.title("📈 Portfolio Manager Pro")
