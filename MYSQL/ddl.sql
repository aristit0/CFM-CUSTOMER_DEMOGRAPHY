CREATE DATABASE customer DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

use customer;

CREATE TABLE customer_info (
  cif BIGINT PRIMARY KEY,
  name VARCHAR(100),
  birth_date DATE,
  gender ENUM('M', 'F'),
  address VARCHAR(255),
  city VARCHAR(100)
);

CREATE TABLE bank_product (
  product_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  cif BIGINT,
  product_type ENUM('SAVINGS', 'CREDIT_CARD', 'LOAN', 'DEPOSIT'),
  open_date DATE,
  status ENUM('ACTIVE', 'CLOSED'),
  FOREIGN KEY (cif) REFERENCES customer_info(cif)
);

CREATE TABLE customer_asset (
  asset_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  cif BIGINT,
  asset_type ENUM('PROPERTY', 'CAR', 'STOCKS', 'BONDS'),
  asset_value DECIMAL(15,2),
  valuation_date DATE,
  FOREIGN KEY (cif) REFERENCES customer_info(cif)
);