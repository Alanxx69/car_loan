CREATE TABLE vehicle (
    id SERIAL PRIMARY KEY,
    model VARCHAR(100) NOT NULL,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    year INT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('available', 'loaned', 'maintenance')) DEFAULT 'available'
);

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


