# Project Title
Food Order Management System

## Description
The Food Order Management System is a Python application that integrates with Dialogflow to manage food orders. It provides a basic order management system, allowing users to add, remove, and track orders.

## Features
* Real-time communication with Dialogflow
* Order management: add, remove, and track orders
* Database interaction to store and retrieve order status

## File Descriptions

### main.py
`main.py` is a FastAPI application that implements a webhook for Dialogflow, enabling real-time communication between Dialogflow and external services. The application manages food orders, allowing users to add, remove, and track orders.

### tests/test_main.py
*No summary provided. However, this file likely contains unit tests for the `main.py` application, ensuring its core logic and functionality are properly tested.*

## Getting Started

### Prerequisites
* Python 3.12
* FastAPI
* Dialogflow
* Database (e.g., SQLite, PostgreSQL)

### Installation
To set up the project, follow these steps:

1. Create a new virtual environment: `python -m venv food-order-env`
2. Activate the virtual environment: `source food-order-env/bin/activate` (on Linux/Mac) or `food-order-env\Scripts\activate` (on Windows)
3. Install required packages: `pip install fastapi uvicorn`
4. Clone this repository: `git clone https://github.com/your-username/food-order-management-system.git`
5. Navigate to the project directory: `cd food-order-management-system`
6. Run the application: `uvicorn main:app --host 0.0.0.0 --port 8000`

### Example Usage
To test the application, you can use a tool like `curl` to send HTTP requests to the webhook endpoint. For example:
```bash
curl -X POST \
  http://localhost:8000/webhook \
  -H 'Content-Type: application/json' \
  -d '{"queryResult": {"intent": {"displayName": "Add to Order"}, "parameters": {"foodItem": "pizza"}}}' 
```
Replace the `foodItem` parameter with your desired food item.

## Usage
The application uses the following endpoints:

* `/webhook`: receives requests from Dialogflow and responds accordingly

Note: This is a basic example, and you should consider implementing proper error handling, security measures, and logging in a production environment.
