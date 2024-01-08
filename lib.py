import sqlite3
import datetime
import pickle

ENCODINGS = ("Unicode", "ASCII", "CP037", "CP850", "CP1140", "CP1252",
             "Latin1", "ISO8859_15", "Mac_Roman", "UTF-8",
             "UTF-8-sig", "UTF-16", "UTF-32", "KOI8-R")


def get_hex_table(filename: str) -> list[list[str, str, ...], ...]:
    """filename: filename to open\n
    return two-dim list like: list[[str, str, str], [str, str, str]]"""
    with open(filename, 'rb') as f:
        b = f.read()

    data = [str(hex(i)[2::]).upper() for i in b]

    if not len(data) % 16:
        data = [data[i:i + 16] for i in range(0, len(data) - 1, 16)]
    else:
        for _ in range((len(data) // 16 + 1) * 16 - len(data)):
            data.append('0')
        data = [data[i:i + 16] for i in range(0, len(data) - 1, 16)]

    return data


def add_to_db(name: str, value: bytes):
    db = sqlite3.connect('dbs/database.db')
    curs = db.cursor()
    curs.execute(f"INSERT INTO main VALUES (?, ?, ?)", (name, str(datetime.datetime.today()), value))
    db.commit()
    db.close()
