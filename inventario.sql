-- Crear tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    usuario TEXT NOT NULL UNIQUE,
    contrasena TEXT,
    rol TEXT CHECK (rol IN ('admin','publico')) NOT NULL
);

-- Crear tabla computadores
CREATE TABLE IF NOT EXISTS computadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial TEXT NOT NULL,
    marca TEXT,
    modelo TEXT,
    procesador TEXT,
    ram TEXT,
    almacenamiento TEXT
    placa_sena TEXT
);

-- Insertar usuarios base
INSERT INTO usuarios (nombre, usuario, contrasena, rol) VALUES
('Administrador', 'admin', 'admin123', 'admin'),
('Usuario Público', 'publico', NULL, 'publico');

-- Insertar computadores de ejemplo
INSERT INTO computadores (serial, marca, modelo, procesador, ram, almacenamiento) VALUES
('ABC123', 'Dell', 'Optiplex 3050', 'Core i5', '8GB', '256GB SSD'),
('PC987', 'HP', 'Pavilion 15', 'Ryzen 5', '16GB', '512GB SSD');
