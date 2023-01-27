-- depends: 0008_analysis_add_organisation

ALTER TABLE analysis
    ADD COLUMN url VARCHAR(128) NOT NULL DEFAULT '';
ALTER TABLE analysis
    ALTER COLUMN url DROP DEFAULT;
