CREATE TABLE Users (
    email varchar NOT NULL,
    name varchar NOT NULL,
    CONSTRAINT pk_Users PRIMARY KEY (email)
);
CREATE TABLE Orders (
    id varchar NOT NULL,
    user_email varchar NOT NULL,
    total money NOT NULL,
    timestamp timestamp NOT NULL,
    CONSTRAINT pk_Orders PRIMARY KEY (id)
);
CREATE TABLE Products (
    id varchar NOT NULL,
    name varchar NOT NULL,
    CONSTRAINT pk_Products PRIMARY KEY (id),
    CONSTRAINT uc_Products_name UNIQUE (name)
);
CREATE TABLE OrderContents (
    order_id varchar NOT NULL,
    product_id varchar NOT NULL,
    quantity int NOT NULL,
    unitary_price money NOT NULL
);
ALTER TABLE Orders
ADD CONSTRAINT fk_Orders_user_email FOREIGN KEY(user_email) REFERENCES Users (email);
ALTER TABLE OrderContents
ADD CONSTRAINT fk_OrderContents_order_id FOREIGN KEY(order_id) REFERENCES Orders (id);
ALTER TABLE OrderContents
ADD CONSTRAINT fk_OrderContents_product_id FOREIGN KEY(product_id) REFERENCES Products (id);
CREATE INDEX idx_Orders_timestamp ON Orders (timestamp);
CREATE INDEX idx_OrderContents_unitary_price ON OrderContents (unitary_price);
