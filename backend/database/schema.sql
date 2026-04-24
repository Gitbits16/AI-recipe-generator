-- ═══════════════════════════════════════════════════════════════════════
-- FlavorForge Database Schema
-- ═══════════════════════════════════════════════════════════════════════
-- Note: Tables are automatically created by backend/db.py
-- This file is for reference or manual creation if needed
-- ═══════════════════════════════════════════════════════════════════════

-- Create database (run this first)
CREATE DATABASE IF NOT EXISTS recipe_ai;
USE recipe_ai;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL COMMENT 'bcrypt hashed password',
    allergy TEXT COMMENT 'comma-separated allergies',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Favorites table
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    recipe TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE,
    INDEX idx_email_date (email, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- History table
CREATE TABLE IF NOT EXISTS history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    ingredients TEXT NOT NULL,
    generated_recipe TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE,
    INDEX idx_email_date (email, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═══════════════════════════════════════════════════════════════════════
-- Verify tables were created
-- ═══════════════════════════════════════════════════════════════════════
SHOW TABLES;
DESCRIBE users;
DESCRIBE favorites;
DESCRIBE history;