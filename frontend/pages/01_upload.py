import streamlit as st
from components.api.client import InsightAIClient
from components.utils import local_css
import pandas as pd

api = InsightAIClient()
local_css("frontend/components/assets/style.css")

# Logo
st.markdown('<div class="logo">InsightAI</div>', unsafe_allow_html=True)

st.header("Upload Data")
st.write("Upload your CSV or Excel files for analysis.")
    
uploaded_file = st.file_uploader(
    "Choose a file",
    type=['csv', 'xlsx', 'xls'],
    help="Supported: CSV, Excel files"
)

if uploaded_file:
    # Show file info
    col1, col2, col3 = st.columns(3)
    col1.metric("File", uploaded_file.name)
    col2.metric("Size", f"{uploaded_file.size / 1024:.1f} KB")
    col3.metric("Type", uploaded_file.type.split('/')[-1].upper())
    
    if st.button("Upload", type="primary"):
        with st.spinner("Processing..."):
            success, result = api.upload_file(uploaded_file)
            
            if success:
                st.success("File uploaded successfully!")
                
                # Show results
                profile = result.get('profile', {})
                
                col1, col2 = st.columns(2)
                col1.metric("Rows", profile.get('num_rows', 0))
                col2.metric("Columns", profile.get('num_columns', 0))
                
                # Column info
                if 'columns' in profile:
                    st.subheader("Column Information")
                    df = pd.DataFrame(profile['columns'])
                    st.dataframe(df, use_container_width=True)
            
            else:
                st.error(f"Upload failed: {result.get('error', 'Unknown error')}")
