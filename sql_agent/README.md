# SQL Agent

This folder contains a LangChain-based SQL agent that interacts with the Chinook SQLite database ([Chinook.db](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/Chinook.db)). The agent uses Google's `gemini-3.5-flash-lite` model to understand user questions in natural language, translate them into SQLite queries, verify them, execute them, and formulate plain-text responses.

## Structure and Files

* **[sql_agent.py](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/sql_agent.py)**: The entrypoint script that initializes the Gemini model, downloads the database (if not already local), instantiates the agent using LangChain's `create_agent`, and runs a sample query.
* **[sql_tools.py](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/sql_tools.py)**: Defines custom LangChain tools for database access and validation.
* **[Chinook.db](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/Chinook.db)**: The SQLite database containing sample data (tracks, playlists, artists, albums, etc.).

## Available Database Tools

The agent has access to a set of custom tools defined in [sql_tools.py](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/sql_tools.py):

1. **[sql_db_list_tables](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/sql_tools.py#L15)**
   * **Description**: Lists all the tables in the database.
   * **Usage**: Used first to find what tables are available.

2. **[sql_db_schema](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/sql_tools.py#L27)**
   * **Description**: Takes a comma-separated list of tables and returns their SQL schema and three sample rows.
   * **Usage**: Used to understand table structures and column names.

3. **[sql_db_query](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/sql_tools.py#L67)**
   * **Description**: Runs a SQL query and returns the results.
   * **Usage**: Used to execute the query after verification.

4. **[sql_db_query_checker](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/sql_tools.py#L83)**
   * **Description**: Uses Gemini to analyze a generated query for common SQL errors (e.g., mismatched types, join columns, nulls) before execution.
   * **Usage**: Crucial checking step before running any queries.

## Getting Started

### Prerequisites

Ensure you have a `.env` file in the project root with your Google API Key:
```env
GOOGLE_API_KEY=your_api_key_here
```

### Usage

Run the SQL Agent script:
```bash
python sql_agent/sql_agent.py
```
This will automatically:
1. Download the [Chinook.db](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/sql_agent/Chinook.db) file if it does not already exist.
2. Query the database to list the available tables.
3. Print the agent's output.
