-- depends: 0003_link_analysis_to_city

CREATE TABLE "user"
(
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(64)  NOT NULL,
    name            VARCHAR(128) NOT NULL,
    hashed_password VARCHAR(128) NOT NULL,
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    is_superuser    BOOLEAN      NOT NULL DEFAULT false,
    is_verified     BOOLEAN      NOT NULL DEFAULT true
);
