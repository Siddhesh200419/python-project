-- Create database
CREATE DATABASE IF NOT EXISTS tourism;

-- Use the tourism database
USE tourism;

-- Create table for agents
CREATE TABLE IF NOT EXISTS agents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15),
    address TEXT
);

-- Create table for bookings
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    agent_id INT,
    customer_id INT,
    tour_package_id INT,
    booking_date DATE,
    total_price DECIMAL(10, 2),
    FOREIGN KEY (agent_id) REFERENCES agents(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (tour_package_id) REFERENCES tour_packages(id)
);

-- Create table for customers
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15),
    address TEXT
);

-- Create table for destinations
CREATE TABLE IF NOT EXISTS destinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    country VARCHAR(50),
    city VARCHAR(50)
);

-- Create table for tour packages
CREATE TABLE IF NOT EXISTS tour_packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    destination_id INT,
    price DECIMAL(10, 2),
    duration INT,
    FOREIGN KEY (destination_id) REFERENCES destinations(id)
);

-- Create table for payments
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    payment_date DATE,
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

-- Create table for reviews
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    rating INT,
    comment TEXT,
    review_date DATE,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

-- Create table for transport
CREATE TABLE IF NOT EXISTS transport (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    type VARCHAR(50),
    provider VARCHAR(100),
    departure_time DATETIME,
    arrival_time DATETIME,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

-- Insert sample data into agents
INSERT INTO agents (name, email, phone, address) VALUES
('Agent A', 'agent_a@example.com', '1234567890', '123 Main St, City A'),
('Agent B', 'agent_b@example.com', '0987654321', '456 Secondary St, City B');

-- Insert sample data into customers
INSERT INTO customers (name, email, phone, address) VALUES
('John Doe', 'john.doe@example.com', '1112223333', '789 Oak St, City A'),
('Jane Smith', 'jane.smith@example.com', '4445556666', '101 Pine St, City B');

-- Insert sample data into destinations
INSERT INTO destinations (name, description, country, city) VALUES
('Paris', 'The capital of France, known for its art, fashion, and culture.', 'France', 'Paris'),
('New York', 'Famous for its skyscrapers, Broadway, and cultural landmarks.', 'USA', 'New York');

-- Insert sample data into tour packages
INSERT INTO tour_packages (name, destination_id, price, duration) VALUES
('Paris City Tour', 1, 1500.00, 7),
('New York City Tour', 2, 2000.00, 5);

-- Insert sample data into bookings
INSERT INTO bookings (agent_id, customer_id, tour_package_id, booking_date, total_price) VALUES
(1, 1, 1, '2025-02-10', 1500.00),
(2, 2, 2, '2025-03-15', 2000.00);

-- Insert sample data into payments
INSERT INTO payments (booking_id, payment_date, amount, status) VALUES
(1, '2025-02-12', 1500.00, 'Completed'),
(2, '2025-03-16', 2000.00, 'Pending');

-- Insert sample data into reviews
INSERT INTO reviews (booking_id, rating, comment, review_date) VALUES
(1, 5, 'Amazing experience! Highly recommended.', '2025-02-20'),
(2, 4, 'Great tour, but could improve the accommodations.', '2025-03-18');

-- Insert sample data into transport
INSERT INTO transport (booking_id, type, provider, departure_time, arrival_time) VALUES
(1, 'Flight', 'Airline X', '2025-02-10 09:00:00', '2025-02-10 12:00:00'),
(2, 'Bus', 'Bus Company Y', '2025-03-15 10:00:00', '2025-03-15 16:00:00');
