-- depends: 0004_user

CREATE TABLE customanalysis
(
    id         UUID PRIMARY KEY NOT NULL,
    user_id    INT              NOT NULL REFERENCES "user" (id),
    name       VARCHAR(96)      NOT NULL,
    unit       VARCHAR(16)      NOT NULL,
    value      FLOAT            NOT NULL,
    created_at TIMESTAMP        NOT NULL DEFAULT now()
);
