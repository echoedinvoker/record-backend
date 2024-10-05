-- Create the precepts table
CREATE TABLE IF NOT EXISTS precepts (
    id INTEGER NOT NULL,
    start_end_times VARCHAR,
    base_multiplier FLOAT NOT NULL,
    thresholds VARCHAR,
    hope_key VARCHAR NOT NULL,
    PRIMARY KEY (id)
);

-- Create an index on the id column of the precepts table
CREATE INDEX IF NOT EXISTS ix_precepts_id ON precepts (id);
