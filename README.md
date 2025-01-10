# Tourism API

This is a simple **Tourism API** built using Python with the `http.server` module to handle HTTP requests (GET, POST, PUT, DELETE) and MySQL for data storage. The API allows you to manage entities like **agents**, **bookings**, **customers**, **destinations**, **tour packages**, and more.

## Features

- **GET**: Retrieve data for agents, bookings, customers, destinations, and tour packages.
- **POST**: Create new records for agents, bookings, and other entities.
- **PUT**: Update existing records.
- **DELETE**: Remove records.

## Technologies

- **Python**: For building the server and handling HTTP requests.
- **MySQL**: For storing data related to the tourism system.
- **JSON**: For data exchange in API responses and requests.

## Requirements

- Python 3.x
- MySQL Database
- Postman (for testing the API)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/tourism-api.git
cd tourism-api
```

### 2. Install dependencies

If you're using any specific dependencies, you can include them in a `requirements.txt` file. If not, the project only uses the built-in `http.server` and `mysql-connector-python`.

Install `mysql-connector-python`:

```bash
pip install mysql-connector-python
```

### 3. Set up MySQL database

Ensure you have a MySQL database set up with the following configuration:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "tourism"  # Make sure the database exists in MySQL
}
```

You can create the necessary tables (`agents`, `bookings`, `customers`, `destinations`, etc.) in MySQL.

### 4. Run the server

Run the Python script to start the server:

```bash
python server.py
```

This will start the server on `http://localhost:8080`.

## API Endpoints

### Agents

- **GET** `/agents/` - Retrieve all agents.
- **GET** `/agents/{id}` - Retrieve a specific agent by ID.
- **POST** `/agents/` - Create a new agent.
- **PUT** `/agents/{id}` - Update an existing agent by ID.
- **DELETE** `/agents/{id}` - Delete an agent by ID.

### Bookings

- **GET** `/bookings/` - Retrieve all bookings.
- **GET** `/bookings/{id}` - Retrieve a specific booking by ID.
- **POST** `/bookings/` - Create a new booking.
- **PUT** `/bookings/{id}` - Update an existing booking by ID.
- **DELETE** `/bookings/{id}` - Delete a booking by ID.

### Customers

- **GET** `/customers/` - Retrieve all customers.
- **GET** `/customers/{id}` - Retrieve a specific customer by ID.
- **POST** `/customers/` - Create a new customer.
- **PUT** `/customers/{id}` - Update an existing customer by ID.
- **DELETE** `/customers/{id}` - Delete a customer by ID.

### Destinations

- **GET** `/destinations/` - Retrieve all destinations.
- **GET** `/destinations/{id}` - Retrieve a specific destination by ID.
- **POST** `/destinations/` - Create a new destination.
- **PUT** `/destinations/{id}` - Update an existing destination by ID.
- **DELETE** `/destinations/{id}` - Delete a destination by ID.

### Tour Packages

- **GET** `/tourpackages/` - Retrieve all tour packages.
- **GET** `/tourpackages/{id}` - Retrieve a specific tour package by ID.
- **POST** `/tourpackages/` - Create a new tour package.
- **PUT** `/tourpackages/{id}` - Update an existing tour package by ID.
- **DELETE** `/tourpackages/{id}` - Delete a tour package by ID.

### Payments

- **GET** `/payments/` - Retrieve all payments.
- **GET** `/payments/{id}` - Retrieve a specific payment by ID.
- **POST** `/payments/` - Create a new payment.
- **PUT** `/payments/{id}` - Update an existing payment by ID.
- **DELETE** `/payments/{id}` - Delete a payment by ID.

### Reviews

- **GET** `/reviews/` - Retrieve all reviews.
- **GET** `/reviews/{id}` - Retrieve a specific review by ID.
- **POST** `/reviews/` - Create a new review.
- **PUT** `/reviews/{id}` - Update an existing review by ID.
- **DELETE** `/reviews/{id}` - Delete a review by ID.

### Transport

- **GET** `/transport/` - Retrieve all transport details.
- **GET** `/transport/{id}` - Retrieve specific transport details by ID.
- **POST** `/transport/` - Add new transport.
- **PUT** `/transport/{id}` - Update an existing transport entry by ID.
- **DELETE** `/transport/{id}` - Delete a transport entry by ID.

## Testing with Postman

Once the server is running, you can test the API using Postman.

1. **GET Request**:
   - URL: `http://localhost:8080/{endpoint}` (Replace `{endpoint}` with the actual API endpoint you want to test, such as `/agents/` or `/bookings/{id}`).

2. **POST Request**:
   - URL: `http://localhost:8080/{endpoint}`
   - Body: In JSON format, include the necessary fields based on the entity you're adding (e.g., name, email for agents).

3. **PUT Request**:
   - URL: `http://localhost:8080/{endpoint}/{id}`
   - Body: In JSON format, include the updated fields for the record.

4. **DELETE Request**:
   - URL: `http://localhost:8080/{endpoint}/{id}`

