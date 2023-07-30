import sqlite3


def create_table():

    """This function creates a table called tenants in the database tenant_info.db to
    store tenant information in the form of columns and rows"""
    conn = sqlite3.connect('tenant_info.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tenants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    apt_num INTEGER UNIQUE,
                    name TEXT,
                    rent TEXT,
                    ph_num TEXT
                )''')
    conn.commit()
    conn.close()


def work_table():
    """This function creates a table called workorders in the database tenant_info.db to
        store work order information in the form of columns and rows"""
    conn = sqlite3.connect('tenant_info.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS workorders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    apt_num INTEGER,
                    issue TEXT,
                    status TEXT
                )''')
    conn.commit()
    conn.close()
