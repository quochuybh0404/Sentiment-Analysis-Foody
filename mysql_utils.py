# import toml
import mysql.connector


def connect_to_mysql():

    [connections.mysql]
    host = 'localhost'
    username = 'root'
    password = ''
    database = 'Foody'

    conn = mysql.connector.connect(
        
        host=st.secrets[connections.mysql][host],
        user=st.secrets[connections.mysql][username],
        password=st.secrets[connections.mysql][password],
        database=st.secrets[connections.mysql][database]
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