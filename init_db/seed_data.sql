-- Limpar dados existentes (caso precise reexecutar)
DELETE FROM reservation_reservation;
DELETE FROM reservation_vehicle;
DELETE FROM reservation_location;
DELETE FROM customer_customer WHERE id > 1; -- Preserva o superusuário, se existir

-- Inserir localidades (reservation_location)
INSERT INTO reservation_location (reference_point, city, state) VALUES
('Aeroporto Internacional', 'São Paulo', 'SP'),
('Shopping Center Norte', 'São Paulo', 'SP'),
('Centro', 'Rio de Janeiro', 'RJ'),
('Aeroporto Santos Dumont', 'Rio de Janeiro', 'RJ'),
('Aeroporto Confins', 'Belo Horizonte', 'MG'),
('Rodoviária', 'Belo Horizonte', 'MG');

-- Inserir veículos (reservation_vehicle)
INSERT INTO reservation_vehicle (model, license_plate, year, status) VALUES
('Honda Civic', 'ABC-1234', 2022, 'available'),
('Toyota Corolla', 'DEF-5678', 2021, 'available'),
('Volkswagen Gol', 'GHI-9012', 2020, 'available'),
('Fiat Argo', 'JKL-3456', 2022, 'available'),
('Jeep Renegade', 'MNO-7890', 2021, 'available'),
('Chevrolet Onix', 'PQR-1234', 2023, 'available'),
('Hyundai HB20', 'STU-5678', 2022, 'available'),
('Nissan Kicks', 'VWX-9012', 2021, 'available'),
('Ford Ka', 'YZA-3456', 2020, 'available'),
('Renault Kwid', 'BCD-7890', 2022, 'available');
