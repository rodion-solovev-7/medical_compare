CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE analysis (
    id UUID PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
    name VARCHAR(256) NOT NULL,
    description TEXT NULL,
    preparation TEXT NULL,
    purpose TEXT NULL,
    interpretation TEXT NULL,
    article_number VARCHAR(64) NULL,
    total_price DECIMAL(8,2) NULL,
    add_data JSONB NOT NULL
);
