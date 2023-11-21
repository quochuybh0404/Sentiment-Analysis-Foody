import sqlite3
import streamlit as st
import toml

conn = sqlite3.connect('foody.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comments TEXT,
        rating INT DEFAULT NULL
    )
''')

def save_to_database(text):
    conn = sqlite3.connect('foody.db')
    cursor = conn.cursor()

    # Thêm đoạn text vào cơ sở dữ liệu
    cursor.execute('INSERT INTO reviews (comments) VALUES (?)', (text,))
    
    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()



