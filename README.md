# Scraping Tool API

This project is a FastAPI-based scraping tool that extracts product information from the [Dentalstall Shop](https://dentalstall.com/shop/). The tool scrapes product title, price, and image (downloaded locally) from a specified number of pages. Scraped data is stored concurrently in a JSON file.

The project includes:
- **Storage:** Saving data in a JSON file for simplicity.
- **Authentication:** Secured endpoints with a static Bearer token.
- **Caching & Retry Mechanism:** To avoid redundant updates and to manage transient errors during scraping.
- **Docker Support:** Instructions and configuration to run the application inside a Docker container.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation and Setup](#installation-and-setup)
  - [Without Docker](#without-docker)
  - [With Docker](#with-docker)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Available Endpoints](#available-endpoints)
  - [Scrape Endpoint](#scrape-endpoint)

---

## Features

- **Scraping:** Extracts product details (title, price, image).
- **Storage:** Saves scraped data in a JSON file.
- **Authentication:** All endpoints are protected with a static Bearer Token.
- **Caching & Retry:** Implements an in-memory cache and a retry mechanism for robust scraping.
- **Docker & Local:** Easy deployment either locally or in a Docker container.

---

## Requirements

- **Python 3.9+**
- **Dependencies:** Listed in `requirements.txt`
- **Docker (Optional):** For containerized deployment

---

## Installation and Setup

### Without Docker

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/priyanshugupta169/Atlys-scrapping-tool.git
   cd scraping-tool
   ```

2. **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**
    Create a .env file in the project root with content similar to:
    ```bash
    STATIC_TOKEN=your_static_token_here
    DEFAULT_PAGE_LIMIT=5
    DEFAULT_PROXY=
    RETRY_DELAY=5
    STORAGE_FILE=data/data.json
    IMAGE_DIR=data/images
    ```
5. **Run the Application:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at http://localhost:8000/docs.


### With Docker

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/priyanshugupta169/Atlys-scrapping-tool.git
    cd scraping-tool
    ```

2. **Configure Environment Variables:**

    Create a .env file in the project root as shown above.

3. **Build the Docker Image:**
    ```bash
    docker build -t scraping-tool .
    ```

4. **Run the Docker Container:**
    ```bash
    docker run -d -p 8000:8000 --env-file .env scraping-tool
    ```
    The API will be accessible at http://localhost:8000/docs.

### Configuration
    The application is configured via a .env file and the config.py module. Key configuration values include:

    - STATIC_TOKEN: The API key for authenticating requests.
    - DEFAULT_PAGE_LIMIT: The default number of pages to scrape if not specified in the request.
    - RETRY_DELAY: The delay (in seconds) between retry attempts.
    - STORAGE_FILE: The path to the JSON storage file.
    - IMAGE_DIR: The directory where downloaded images are stored.

### Running the Application
    After installation and configuration, run the application using one of the following methods:

- ## Locally:
    ```bash
    uvicorn main:app --reload
    ```
- ## Docker:
    Ensure the container is running (as shown above).
    
    The API will be available at http://localhost:8000/docs.

### Available Endpoints
**Swagger Documentation**

- ## Scrape Endpoint

    Endpoint: /scrape

    - Method: POST
    - Authentication: Requires the static API key
    - Request Body: JSON (both fields are optional)
        - page_limit (number): Limit the number of pages to scrape.
        - proxy (string): Proxy URL for scraping.


