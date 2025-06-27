# InsightAI: AI-Powered Business Intelligence Analyst

**InsightAI** is an AI-powered business analyst that enables users to explore datasets, uncover insights, and generate forecasts and reports by asking questions in natural language. Designed for business users, it leverages powerful GenAI and Data Science tooling under the hood.

---

## Features

- Upload and process structured business data (CSV, XLSX)
- Ask questions like:
    - "What are the key drivers of sales decline in Q2?"
    - "What’s the customer churn forecast for next month?"
- LLM-assisted exploratory data analysis (EDA)
- Time series forecasting (Prophet/ARIMA)
- Statistical analysis and ML modeling
- Insight report generation via GPT-4o or Claude 3.5
- Semantic search over past reports using Pinecone/Azure AI Search

---

## Tech Stack

| Layer | Tools |
| --- | --- |
| Frontend | Streamlit or Chainlit |
| Backend | FastAPI, LangChain, LangServe |
| AI/ML | GPT-4o, Claude 3.5, Scikit-learn, Prophet |
| Vector DB | Pinecone, Azure AI Search |
| RDBMS | Amazon RDS, Aurora with pgvector |
| Deployment | Docker, AWS/Azure |
