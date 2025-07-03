import streamlit as st
from components.api.client import InsightAIClient
from components.utils import local_css
import pandas as pd

api = InsightAIClient()
local_css("frontend/components/assets/style.css")

# Logo
st.markdown('<div class="logo">InsightAI</div>', unsafe_allow_html=True)

st.header("My Datasets")
success, datasets = api.list_datasets()

if not success:
    st.error("Unable to load datasets")
    st.stop()

if not datasets:
    st.info("No datasets yet. Upload your first dataset!")
    st.stop()

# Simple search
search = st.text_input("Search datasets", placeholder="Search by filename...")

# Filter and display
filtered = [d for d in datasets if search.lower() in d['filename'].lower()] if search else datasets

for dataset in filtered:
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        
        col1.write(f"**{dataset['filename']}**")
        col2.write(dataset['created_at'])
        
        if col3.button("View", key=f"view_{dataset['id']}"):
            with st.expander(f"Details: {dataset['filename']}", expanded=True):
                success, detail = api.get_dataset(dataset['id'])
                if success:
                    profile = detail.get('profile', {})
                    
                    col_a, col_b = st.columns(2)
                    col_a.metric("Rows", profile.get('num_rows', 0))
                    col_b.metric("Columns", profile.get('num_columns', 0))
                    
                    if 'columns' in profile:
                        st.write("**Column Details:**")
                        df = pd.DataFrame(profile['columns'])
                        st.dataframe(df, use_container_width=True)
        
        if col4.button("Delete", key=f"del_{dataset['id']}"):
            success, result = api.delete_dataset(dataset['id'])
            if success:
                st.success("Deleted!")
                st.rerun()
            else:
                st.error("Delete failed")
        
        st.divider()