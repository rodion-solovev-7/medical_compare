-- depends: 0000_analysis

CREATE EXTENSION pg_trgm;
CREATE INDEX ix_analysis_name_tsv ON analysis USING gin (name gin_trgm_ops);
