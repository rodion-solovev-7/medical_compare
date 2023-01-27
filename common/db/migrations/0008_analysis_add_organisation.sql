-- depends: 0007_refactor_link_following_history

ALTER TABLE city
    ADD COLUMN organisation VARCHAR(32) NOT NULL DEFAULT 'unknown';
ALTER TABLE analysis
    ADD COLUMN organisation VARCHAR(32) NOT NULL DEFAULT 'unknown';
