-- depends: 0001_analysis_name_fulltext_search

CREATE TABLE city (
    id UUID PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
    name VARCHAR(64) NOT NULL,
    url VARCHAR(128) NOT NULL,
    code VARCHAR(32) NULL
);
