CREATE DATABASE IF NOT EXISTS image_classification
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE image_classification;

CREATE TABLE IF NOT EXISTS image_uploads (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    category VARCHAR(10) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT UNSIGNED NOT NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_category (category),
    INDEX idx_uploaded_at (uploaded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
