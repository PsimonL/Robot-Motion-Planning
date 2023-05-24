DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE  IF NOT EXISTS  customers(
  customer_id int GENERATED ALWAYS AS IDENTITY,
  name char (20) NOT NULL,
  location char (25) NOT NULL,
  type int NOT NULL,

  PRIMARY KEY (customer_id)
);
ALTER TABLE customers ADD CONSTRAINT type_check CHECK (type IN ('A', 'B', 'C', 'D'));
-- POPULATE CUSTOMERS


DROP TABLE IF EXISTS food CASCADE;
CREATE TABLE  IF NOT EXISTS  food(
  food_id int GENERATED ALWAYS AS IDENTITY,
  description char (20) NOT NULL,
  price float NOT NULL,

  PRIMARY KEY (food_id)
);
-- POPULATE FOOD

DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE  IF NOT EXISTS  orders(
  order_id int GENERATED ALWAYS AS IDENTITY,
  price float NOT NULL,
  date date NOT NULL,

  PRIMARY KEY (order_id)
);



