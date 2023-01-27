-- depends: 0006_link_following_history

TRUNCATE linkfollowinghistory;
ALTER TABLE linkfollowinghistory
    ADD COLUMN analysis_id UUID NOT NULL REFERENCES analysis (id),
    DROP COLUMN link;
