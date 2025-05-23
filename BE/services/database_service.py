import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from flask import current_app
from typing import List, Tuple, Any


def get_db_connection() -> psycopg2.extensions.connection:
    """
    Create and return a new PostgreSQL database connection with pgvector registered.
    """
    config = current_app.config
    conn = psycopg2.connect(
        host=config['DB_HOST'],
        database=config['DB_NAME'],
        user=config['DB_USER'],
        password=config['DB_PASSWORD']
    )
    register_vector(conn)  # Register pgvector extension on this connection
    return conn


def insert_image(path: str, color_layout: Tuple[float, ...], vgg_features: List[float]) -> None:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Convert color_layout to a Python list if it's a NumPy array
                color_layout_list = color_layout.tolist() if isinstance(color_layout, np.ndarray) else list(color_layout)
                
                # Print lengths for debugging
                print("************************")
                print(f"Length of color_layout: {len(color_layout_list)}")
                print(f"Length of vgg_features: {len(vgg_features)}")

                cur.execute(
                    "INSERT INTO images (path, color_layout, vgg_features) VALUES (%s, %s, %s)",
                    (path, color_layout_list, vgg_features)  # Pass the converted list
                )
                conn.commit()
    except Exception as e:
        print("***************** Error *************************")
        print(e)
        raise RuntimeError(f"Error inserting image: {e}") from e


def get_all_features() -> List[Tuple[int, Tuple[float, ...], Any]]:
    """
    Retrieve all image features from the database.

    Returns:
        List of tuples: Each tuple contains (id, color_layout, vgg_features).
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, color_layout, vgg_features FROM images")
                records = cur.fetchall()
        return records
    except Exception as e:
        # You may want to log this error in real applications
        raise RuntimeError(f"Error fetching features: {e}") from e
