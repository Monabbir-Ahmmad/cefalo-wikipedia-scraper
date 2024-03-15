# Cefalo web scraper

This is the Python Developer Assignment assigned by Cefalo

## Requirements

Make sure you have the following installed:

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Monabbir-Ahmmad/cefalo-wikipedia-scraper.git
```

2. Navigate to the project directory:

```bash
cd cefalo-wikipedia-scraper
```

3. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
```

4. Activate your virtual environment:

```bash
venv\Scripts\activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment variables example

```bash
MONGO_URI = 'Your MongoDB Atlas connection string'
```

## Running the Application

1. To run the web scraper execute the following command (Run in python virtual environment if exists):

```bash
python scraper_main.py
```

3. To run the REST API, execute the following command (Run in python virtual environment if exists):

```bash
uvicorn server:app --reload
```

This command starts the server locally and enables auto-reloading whenever changes are made to the code.

Once the server is running, you can access the API documentation by visiting http://127.0.0.1:8000/docs in your web browser.
