from typing import Optional
import psycopg2
from ktdparser.config import settings


def create_tables(connection: psycopg2.extensions.connection) -> None:
    """Create if not exists all KTD tables

    Args:
        connection: The connection object.

    Raises:
        psycopg2.OperationalError: If an error occurs during table creation.
    """
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS ktd (
                       id              VARCHAR(50) PRIMARY KEY,
                       name            TEXT NOT NULL,
                       page_count      INT NOT NULL
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS main_task (
                       ktd_id          VARCHAR(50) NOT NULL,
                       id              SERIAL PRIMARY KEY,
                       name            TEXT NOT NULL,
                       page            INT NOT NULL,
                       FOREIGN KEY (ktd_id) REFERENCES ktd(id) ON DELETE CASCADE
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS summary_task (
                       main_task_id    INT NOT NULL,
                       id              INT NOT NULL,
                       code            VARCHAR(50) NOT NULL,
                       object          VARCHAR(50),
                       name            TEXT NOT NULL,
                       docs            TEXT,
                       profession      TEXT,
                       category        INT,
                       quantity        INT,
                       page            INT NOT NULL,
                       FOREIGN KEY (main_task_id) REFERENCES main_task(id) ON DELETE CASCADE
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS subtask (
                       ktd_id          VARCHAR(50) NOT NULL,
                       main_task_id    INT NOT NULL,
                       summary_task_id INT NOT NULL,
                       id              SERIAL PRIMARY KEY,
                       name            TEXT NOT NULL,
                       page            INT NOT NULL,
                       FOREIGN KEY (ktd_id) REFERENCES ktd(id) ON DELETE CASCADE,
                       FOREIGN KEY (main_task_id) REFERENCES main_task(id) ON DELETE CASCADE
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS material (
                       ktd_id          VARCHAR(50) NOT NULL,
                       main_task_id    INT NOT NULL,
                       summary_task_id INT NOT NULL,
                       subtask_id      INT,
                       id              SERIAL PRIMARY KEY,
                       name            TEXT NOT NULL,
                       measurement     VARCHAR(50),
                       quantity        REAL,
                       page            INT NOT NULL,
                       FOREIGN KEY (ktd_id) REFERENCES ktd(id) ON DELETE CASCADE,
                       FOREIGN KEY (main_task_id) REFERENCES main_task(id) ON DELETE CASCADE
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS instrument (
                       ktd_id          VARCHAR(50) NOT NULL,
                       main_task_id    INT NOT NULL,
                       summary_task_id INT NOT NULL,
                       subtask_id      INT,
                       id              SERIAL PRIMARY KEY,
                       name            TEXT NOT NULL,
                       measurement     VARCHAR(50),
                       quantity        INT,
                       page            INT NOT NULL,
                       FOREIGN KEY (ktd_id) REFERENCES ktd(id) ON DELETE CASCADE,
                       FOREIGN KEY (main_task_id) REFERENCES main_task(id) ON DELETE CASCADE,
                       FOREIGN KEY (subtask_id) REFERENCES subtask(id) ON DELETE CASCADE
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS object (
                       ktd_id          VARCHAR(50) NOT NULL,
                       main_task_id    INT NOT NULL,
                       code            VARCHAR(50),
                       name            TEXT NOT NULL,
                       page            INT NOT NULL,
                       FOREIGN KEY (ktd_id) REFERENCES ktd(id) ON DELETE CASCADE,
                       FOREIGN KEY (main_task_id) REFERENCES main_task(id) ON DELETE CASCADE
                   )""")
    connection.commit()


def get_db(password: str, user: Optional[str] = None, host: Optional[str] = None, port: Optional[int] = None,
           database: Optional[str] = None) -> psycopg2.extensions.connection:
    """Establish a connection to a PostgreSQL database and create tables if not exist.

    Args:
        password: The password for the database user.
        user: The username for the database.
        host: The host address of the database.
        port: The port number of the database.
        database: The name of the database.

    Returns:
        psycopg2.extensions.connection: The connection object.

    Raises:
        psycopg2.OperationalError: If an error occurs during the connection or table creation.
    """
    connection = psycopg2.connect(
        password=password,
        user=user or settings.DB_USER,
        host=host or settings.DB_HOST,
        port=port or settings.DB_PORT,
        database=database or settings.DB_NAME
    )
    create_tables(connection)
    return connection
