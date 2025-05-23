CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    path VARCHAR(255) UNIQUE,
    color_layout FLOAT[6],
    vgg_features VECTOR(512),
    created_at TIMESTAMP DEFAULT NOW()
);
