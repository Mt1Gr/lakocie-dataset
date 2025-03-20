# LaKocie Dataset
A specialized web scraping and data processing tool for collecting, structuring, and analyzing wet cat food product information from Polish pet stores.

## Project Overview
LaKocie Dataset is an automated data collection system that:

- Scrapes detailed product information from pet store websites
- Stores structured data in SQLite database
- Processes and extracts analytical composition data using AI/ML
- Maintains historical price tracking
- Ensures data validity and consistency

## Key Features
- **Automated Web Scraping**
    - HTML content collection with rate limiting and robots.txt compliance
    - Multi-store support architecture (currently supporting Kocie Figle)
    - Historical data preservation

- **Robust Data Processing**
    - SQLModel-based database schema
    - Product information extraction and normalization
    - Price history tracking
    - Analytical composition parsing

- **AI-Powered Data Extraction**
    - OpenAI GPT integration for complex text analysis
    - Structured output generation for analytical components
    - Automated dietary supplement classification

## Technology Stack
- Python 3.13
- SQLModel/SQLAlchemy (Database ORM)
- BeautifulSoup4 (Web Scraping)
- OpenAI API (GPT-4 Integration)
- pytest (Testing Framework)

## Project Structure
```
lakocie-dataset/
├── src/
│   └── lakocie_dataset/
│       ├── database/     # Database models and operations
│       ├── scrap/        # Web scraping infrastructure
│       └── openai_api/   # AI integration components
├── test/                 # Comprehensive test suite
└── config.yaml           # Configuration management
```

## Setup and Installation
Project is


1. Clone the repository:
```bash
git clone https://github.com/yourusername/lakocie-dataset.git
cd lakocie-dataset
```

2. Create and fill `.env` fill with OpenAI API key:

```bash
echo "OPENAI_API_KEY=<you key>" > .env
```

1. Install dependencies

```bash
uv sync
```
uv is an extremely fast Python package and project manager, installation guide can be found in here: <https://docs.astral.sh/uv/>



## Running the Tool

Control flow of tool can be controlled via `config.yaml` file.

For example, with this configuration:

```yaml
modes:
  latest_info:
    switch: True
    save_to_db: True
  gpt_extract_data:
    switch: True
```

The tool will:

Download the latest product data
Save it to the database
Process the text data using GPT to extract structured information
All downloaded files will be stored in data/htmls and processed data in database.db.

### Configuration Structure:
```yaml
paths:
  htmls_dir: data/htmls     # Directory for storing HTML files
  database: data/database.db # SQLite database location

downloading:
  sleep_time: 3             # Delay between requests (in seconds)

modes:                      # Operation modes switches
  latest_info:
    switch: False           # Enable/disable downloading latest data
    save_to_db: False       # Enable/disable saving to database

  save_history_info_to_db:
    switch: False
    date_choice: "2025-03-12" # Date for historical data processing

  cohere_database:
    switch: False           # Enable/disable database coherence check

  gpt_extract_data:
    switch: False           # Enable/disable GPT data extraction
```

### Development mode
```yaml
dev:
  debug: True  # Enable debug logging
```
Set debug: False in production to reduce log output.

These configurations control the tool's behavior as implemented in `config.py`.

### Testing

```bash
uv run pytest
```

## Design Highlights
- **Modular Architecture**: Clean separation of concerns between scraping, data storage, and AI processing
- **Type Safety**: Extensive use of Python type hints and Pydantic models
- **Test Coverage**: Comprehensive test suite for core functionality
- **Configurability:** YAML-based configuration for easy deployment adjustments
- **Error Handling**: Robust error handling and logging throughout the system
