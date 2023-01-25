-- depends: 0002_city

ALTER TABLE analysis
    ADD COLUMN city_id UUID NOT NULL,
    ADD CONSTRAINT city_id_fkey FOREIGN KEY (city_id)
    REFERENCES city (id);

