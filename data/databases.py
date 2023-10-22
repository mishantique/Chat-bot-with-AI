import sqlite3
import binascii
import os
import hashlib
from PIL import Image

import base64

if not os.path.exists('data'):
    os.makedirs('data')

conn = sqlite3.connect('data/database', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int, name: str, user_surname: str, mail: str, password: str):
    cursor.execute('INSERT INTO users (name, user_surname, mail, password) VALUES (?, ?, ?, ?)',
                   (name, user_surname, mail, password))
    conn.commit()

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def insert_blob(photo):
    try:
        conn = sqlite3.connect('data/database', check_same_thread=False)
        cursor = conn.cursor()
        print("Подключен к SQLite")

        sqlite_insert_blob_query = """INSERT INTO orders
                                  (photo) VALUES (?)"""

        emp_photo = convert_to_binary_data(photo)

        # Преобразование данных в формат кортежа
        data_tuple = emp_photo
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        conn.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблиу")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            print("Соединение с SQLite закрыто")


def clean_filename(filename):
    return ''.join(c if c.isalnum() or c in {'-', '_', ' '} else '_' for c in filename).rstrip('_')


def write_to_file(data, filename):
    # Запись строковых данных в файл в бинарном режиме
    with open(filename, 'wb') as file:
        file.write(base64.b64decode(data))

    print(f"Данные из blob сохранены в: {filename}\n")


def read_blob_data(time):
    try:
        print("Подключен к SQLite")

        # Получаем id из таблицы orders по времени
        cursor.execute('SELECT id FROM orders WHERE time = ?', (time,))
        result = cursor.fetchone()

        if result:
            order_id = result[0]
            print(f"ID заказа для времени {time}: {order_id}")

            # Создаем папку 'data' (если её еще нет)
            data_folder = 'data'
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            # Создаем папку 'id' для данного заказа
            order_folder = os.path.join(data_folder, str(order_id))
            if not os.path.exists(order_folder):
                os.makedirs(order_folder)

            sql_fetch_blob_query = """SELECT photo1, photo2, photo3, photo4, photo5, photo6, photo7, photo8, photo9, photo10, photo11, photo12, photo13, photo14,photo15 FROM orders WHERE time = ?"""
            cursor.execute(sql_fetch_blob_query, (time,))
            record = cursor.fetchall()

            for i, row in enumerate(record):
                print(f"Сохранение изображения {i + 1} на диске \n")
                for j, photo_data in enumerate(row):
                    if photo_data:
                        # Заменяем двоеточие во времени на подчеркивание
                        formatted_time = time.replace(':', '_')
                        filename = os.path.join(order_folder, f"{formatted_time}_photo{j + 1}.jpg")
                        write_to_file(photo_data, filename)

            print(f'order_folder: {order_folder}')
            return order_folder
        else:
            print(f"Не удалось найти заказ для времени {time}")
            return None
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        return None
    finally:
        print("Соединение с SQLite закрыто")



def read_doc_data(time):
    try:
        print("Подключен к SQLite")

        # Получаем order_id из таблицы orders
        cursor.execute('SELECT id FROM orders WHERE time = ?', (time,))
        order_id_result = cursor.fetchone()
        if not order_id_result:
            print("Не удалось получить order_id для времени", time)
            return

        order_id = order_id_result[0]

        sql_fetch_blob_query = """SELECT doc FROM orders WHERE time = ?"""
        cursor.execute(sql_fetch_blob_query, (time,))
        record = cursor.fetchall()
        for i, row in enumerate(record):
            print(f"Сохранение документа {i + 1} на диске \n")
            # Создаем папку для каждого заказа
            folder_name = f"data/акт_{order_id}"
            os.makedirs(folder_name, exist_ok=True)

            for j, doc_data in enumerate(row):
                if doc_data:
                    # Заменяем двоеточие во времени на подчеркивание
                    formatted_time = time.replace(':', '_')
                    filename = f"{folder_name}\\Заявка от {formatted_time}_document{j + 1}.pdf"
                    write_to_file(doc_data, filename)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        print("Соединение с SQLite закрыто")

import os

