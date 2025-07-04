import streamlit as st
from components.api.client import InsightAIClient
from components.utils import local_css
import pandas as pd
import plotly.express as px

api = InsightAIClient()
local_css("frontend/components/assets/style.css")

# Logo
st.markdown('<div class="logo">InsightAI</div>', unsafe_allow_html=True)

st.header("Analysis")
success, datasets = api.list_datasets()

if not success or not datasets:
    st.warning("No datasets available. Upload a dataset first.")
else:
    # Dataset selection
    dataset_names = [f"{d['filename']} (ID: {d['id']})" for d in datasets]
    selected = st.selectbox("Select dataset:", dataset_names)

    if selected:
        dataset_id = int(selected.split("ID: ")[1].split(")")[0])
        
        success, detail = api.get_dataset(dataset_id)
        if not success:
            st.error("Unable to load dataset")
        else:
            profile = detail.get('profile', {})
            
            # Overview metrics
            st.subheader("Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", profile.get('num_rows', 0))
            col2.metric("Columns", profile.get('num_columns', 0))
            
            total_missing = sum(col.get('missing', 0) for col in profile.get('columns', []))
            col3.metric("Missing Values", total_missing)
            
            # Column analysis
            if 'columns' in profile and profile['columns']:
                st.subheader("Column Analysis")
                
                df_cols = pd.DataFrame(profile['columns'])
                
                # Simple charts
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'dtype' in df_cols.columns:
                        st.write("**Data Types**")
                        dtype_counts = df_cols['dtype'].value_counts()
                        fig = px.pie(
                            values=dtype_counts.values,
                            names=dtype_counts.index,
                            color_discrete_sequence=['#4e45d6', '#6563dc', '#7c81e2', '#939fe9']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    if 'missing' in df_cols.columns:
                        missing_data = df_cols[df_cols['missing'] > 0]
                        if not missing_data.empty:
                            st.write("**Missing Values**")
                            fig = px.bar(
                                missing_data,
                                x='name',
                                y='missing',
                                color_discrete_sequence=['#4e45d6']
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.success("No missing values!")
                
                # Column details table
                st.subheader("Column Details")
                st.dataframe(df_cols, use_container_width=True)
                
                # Simple insights
                st.subheader("Insights")
                total_cells = profile.get('num_rows', 0) * profile.get('num_columns', 0)
                missing_pct = (total_missing / total_cells * 100) if total_cells > 0 else 0
                
                if missing_pct < 5:
                    st.success("Excellent data quality - very few missing values")
                elif missing_pct < 15:
                    st.warning("Good data quality - some missing values")
                else:
                    st.error("Data quality concerns - many missing values")

# # Add these components:
# - Interactive correlation heatmaps
# - Outlier visualization
# - Distribution plots
# - Time series analysis
# - Statistical summary cards

# # Auto-chart recommendations:
# - Smart chart type selection
# - Brand-colored visualizations
# - Export to PNG/PDF
# - Interactive filtering