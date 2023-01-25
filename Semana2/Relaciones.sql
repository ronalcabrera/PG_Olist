use dbolist;
-- PRIMARY KEYS

ALTER TABLE products ADD PRIMARY KEY (id_product);
ALTER TABLE customers ADD PRIMARY KEY (id_customer);
ALTER TABLE sellers ADD PRIMARY KEY (id_seller);
ALTER TABLE orders ADD PRIMARY KEY (id_order);
ALTER TABLE marketing_qualified_leads ADD PRIMARY KEY (mql_id);
ALTER TABLE geolocation ADD PRIMARY KEY (id_state);
ALTER TABLE zip_code_prefix ADD PRIMARY KEY (id_code_prefix);

-- --------------------------------------------------------------------------------------------------------------------
ALTER TABLE customers MODIFY id_code_prefix VARCHAR(50);

-- FOREIGN KEYS

SET FOREIGN_KEY_CHECKS=0;

ALTER TABLE orders ADD CONSTRAINT fk_customer_id FOREIGN KEY (id_customer) REFERENCES customers(id_customer);

ALTER TABLE order_items ADD CONSTRAINT fk_order_items FOREIGN KEY (id_order) REFERENCES orders(id_order);
ALTER TABLE order_items ADD CONSTRAINT fk_products FOREIGN KEY (id_product) REFERENCES products(id_product);

ALTER TABLE order_payments ADD CONSTRAINT fk_order_payments FOREIGN KEY (id_order) REFERENCES orders(id_order);

ALTER TABLE order_reviews ADD CONSTRAINT fk_order_reviews FOREIGN KEY (id_order) REFERENCES orders(id_order);

ALTER TABLE zip_code_prefix ADD CONSTRAINT fk_zip_code FOREIGN KEY (id_state) REFERENCES geolocation(id_state);

ALTER TABLE sellers ADD CONSTRAINT fk_seller_zip FOREIGN KEY (id_code_prefix) REFERENCES zip_code_prefix(id_code_prefix);
ALTER TABLE customers ADD CONSTRAINT fk_customer_zip FOREIGN KEY (id_code_prefix) REFERENCES zip_code_prefix(id_code_prefix);
