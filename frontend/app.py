import streamlit as st
from components.utils import local_css
from components.api.client import InsightAIClient

st.set_page_config(
    page_title="InsightAI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
local_css("frontend/components/assets/style.css")

api = InsightAIClient()

# Logo
st.markdown('<div class="logo">InsightAI</div>', unsafe_allow_html=True)

st.header("Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Welcome to InsightAI")
    st.write("""
    Transform your data into actionable insights using AI-powered analysis.
    """)

    if st.button("Start by Uploading Data", type="primary"):
        st.switch_page("pages/01_upload.py")  # or use `st.session_state`

with col2:
    st.subheader("Quick Stats")
    success, datasets = api.list_datasets()
    if success:
        st.metric("Datasets", len(datasets))
        if datasets:
            latest = max(datasets, key=lambda x: x['created_at'])
            st.info(f"Latest: {latest['filename']}")
    else:
        st.warning("Unable to load stats")

# # Advanced visualizations:
# - Plotly interactive charts
# - Data quality scorecards
# - Trend indicators
# - Export functionality