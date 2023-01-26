-- depends: 0005_custom_analysis

CREATE TABLE linkfollowinghistory
(
    id         UUID PRIMARY KEY NOT NULL,
    user_id    INT              NOT NULL REFERENCES "user" (id),
    link       VARCHAR(128)     NOT NULL,
    created_at TIMESTAMP        NOT NULL DEFAULT now()
);
