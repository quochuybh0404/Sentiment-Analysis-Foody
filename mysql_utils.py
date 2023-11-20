import toml
import mysql.connector


def load_db_config():
    with open('secrets.toml', 'r') as file:
        config = toml.load(file)
    return config.get('database', {})

def connect_to_mysql():
    db_config = load_db_config()
    host = db_config.get('host', 'localhost')
    username = db_config.get('username', 'root')
    password = db_config.get('password', '')
    database = db_config.get('database_name', 'Foody')

    conn = mysql.connector.connect(
        
        host=host,
        user=username,
        password=password,
        database=database
    )
    return conn

def save_comment_to_db(comment):
    conn = connect_to_mysql()
    insert_query = "INSERT INTO reviews (comments) VALUES (%s)"
    data_to_insert = (comment,)
    cursor = conn.cursor()
    cursor.execute(insert_query, data_to_insert)
    conn.commit()
    conn.close()

conn = connect_to_mysql()
create_table_query = '''
    CREATE TABLE IF NOT EXISTS reviews (
        id INT AUTO_INCREMENT PRIMARY KEY,
        comments TEXT,
        ratings INT DEFAULT NULL
    )
'''
cursor = conn.cursor()
cursor.execute(create_table_query)
conn.commit()
conn.close()