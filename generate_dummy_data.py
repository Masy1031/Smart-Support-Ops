import os

def create_dummy_docs():
    source_docs_dir = "data/source_docs"
    os.makedirs(source_docs_dir, exist_ok=True)

    # Dummy Specification Document
    with open(os.path.join(source_docs_dir, "dataflow_ai_spec.md"), "w", encoding="utf-8") as f:
        f.write("""# DataFlow AI Product Specification

## 1. Overview
DataFlow AI is an intelligent data integration and analytics platform designed to streamline data pipelines and provide actionable insights.

## 2. Key Features
- **Automated Data Ingestion:** Connects to various data sources (databases, cloud storage, APIs).
- **ETL Capabilities:** Data transformation, cleaning, and enrichment.
- **AI-Powered Analytics:** Machine learning models for predictive analytics and anomaly detection.
- **Interactive Dashboards:** Customizable dashboards for data visualization.

## 3. System Architecture
- Microservices-based architecture.
- Utilizes Kubernetes for container orchestration.
- PostgreSQL for metadata storage.
- Apache Kafka for real-time data streaming.

## 4. API Endpoints
- `/api/v1/data/ingest`: For ingesting new data.
- `/api/v1/analytics/predict`: For running AI predictions.
- `/api/v1/dashboards`: For managing user dashboards.

## 5. Known Limitations
- Large file uploads (>1GB) may experience performance degradation during peak hours.
- Real-time dashboard updates might have a latency of up to 5 seconds.
""")

    # Dummy Error Log Document
    with open(os.path.join(source_docs_dir, "dataflow_ai_errors.md"), "w", encoding="utf-8") as f:
        f.write("""# DataFlow AI Common Errors and Troubleshooting

## 1. Error Code: `DF-5001 - Database Connection Failed`
- **Description:** The application failed to establish a connection with the PostgreSQL database.
- **Possible Causes:**
    - Incorrect database credentials in configuration.
    - Database server is down or unreachable.
    - Firewall blocking database port.
- **Solution:**
    1. Verify `DATABASE_URL` in `.env` file.
    2. Check database server status.
    3. Ensure necessary ports (e.g., 5432) are open.

## 2. Error Code: `DF-4003 - Invalid API Key`
- **Description:** The API request was made with an invalid or expired API key.
- **Possible Causes:**
    - `OPENAI_API_KEY` in `.env` is incorrect or missing.
    - API key has expired.
- **Solution:**
    1. Confirm `OPENAI_API_KEY` in `.env` is correct.
    2. Regenerate API key from OpenAI dashboard if expired.

## 3. Error Code: `DF-6002 - Data Transformation Failure`
- **Description:** An error occurred during data transformation in the ETL pipeline.
- **Possible Causes:**
    - Input data schema mismatch.
    - Custom transformation script error.
- **Solution:**
    1. Review input data format.
    2. Debug custom transformation logic.
""")

    # Dummy FAQ Document
    with open(os.path.join(source_docs_dir, "dataflow_ai_faq.md"), "w", encoding="utf-8") as f:
        f.write("""# DataFlow AI Frequently Asked Questions

## Q1: How do I connect a new data source?
- **Answer:** Navigate to 'Settings > Data Sources' and click 'Add New Source'. Follow the prompts to configure your connection.

## Q2: Can I integrate DataFlow AI with my existing BI tools?
- **Answer:** Yes, DataFlow AI provides standard API endpoints and direct database access for integration with popular BI tools like Tableau, Power BI, and Looker. Refer to our integration guide for more details.

## Q3: What kind of machine learning models are supported?
- **Answer:** We support a variety of supervised and unsupervised learning models, including regression, classification, clustering, and time-series forecasting. Users can also bring their own custom models.

## Q4: How often is my data updated?
- **Answer:** Data update frequency is configurable per data source. Options range from real-time streaming to daily or weekly batch processing.
""")

    print(f"Created dummy documents in {source_docs_dir}")

if __name__ == "__main__":
    create_dummy_docs()

