# DataFlow AI Common Errors and Troubleshooting

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
