import sqlite3

default_admins = [
    (1, '5712572640', 1),
    (2, '1549748318', 1)
    (3, '1662672529', 1)
]
token = '7594521276:AAEyNanseIFUpZZvjl3qttq9JPJmMeaieR4'
bot_name = '@DDOSHUMEIN_BOT'
bot_username = '@@DDOSHUMEIN_BOT'
owner_username = '@@DDOSHUMEIN_BOT'
channel_username = '@@DDOSHUMEIN_BOT'

def initialize_db():
    conn = sqlite3.connect('bot_data.db')
    conn.execute('PRAGMA journal_mode=WAL;')
    cursor = conn.cursor()
    cursor.execute("BEGIN IMMEDIATE")
    # Create table for bot configurations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_configs (
            id INTEGER PRIMARY KEY,
            token TEXT NOT NULL,
            bot_name TEXT NOT NULL,
            bot_username TEXT NOT NULL,
            owner_username TEXT NOT NULL,
            channel_username TEXT
        )
    ''')
    
    # Insert default bot config if not exists
    cursor.execute('''
        INSERT OR IGNORE INTO bot_configs (id,token,bot_name,bot_username,owner_username,channel_username)
        VALUES (?,?,?,?,?,?)
    ''', ('1',token,bot_name,bot_username,owner_username,channel_username,))
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            expiration_date DATETIME,
            bot_id INTEGER,
            FOREIGN KEY (bot_id) REFERENCES bot_configs(id)
        )
    ''')

    # Create admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY,
            admin_id TEXT,
            bot_id INTEGER,
            FOREIGN KEY (bot_id) REFERENCES bot_configs(id)
        )
    ''')
    
    # Insert default admin if not exists
    for id,admin_id, bot_id in default_admins:
        cursor.execute('''
            INSERT OR IGNORE INTO admins (id, admin_id, bot_id)
            VALUES (?, ?, ?)
        ''', (id, admin_id, bot_id))

    # Create logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            target TEXT,
            port INTEGER,
            time INTEGER,
            command TEXT,
            timestamp TEXT
        )
    ''')

    conn.commit()
    conn.close()
