import sqlite3

def setup_db():
    """Set up an in-memory SQLite database with magical candy shops and ingredients."""
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()

    # Candy Shops Table
    cur.execute('''
        CREATE TABLE candy_shops (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            rating INTEGER
        )
    ''')
    candy_shops_data = [
        (1, 'Sweet Haven', 'Candyland', 5),
        (2, 'Lollipop Palace', 'Sugar Hills', 4),
        (3, 'Chocolate Kingdom', 'Cocoa Valley', 5),
        (4, 'Gummy Wonderland', 'Jelly Isles', 3)
    ]
    cur.executemany("INSERT INTO candy_shops VALUES (?, ?, ?, ?)", candy_shops_data)

    # Ingredients Table
    cur.execute('''
        CREATE TABLE candy_ingredients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            rarity TEXT,
            shop_id INTEGER,
            FOREIGN KEY (shop_id) REFERENCES candy_shops(id)
        )
    ''')
    candy_ingredients_data = [
        (1, 'Rainbow Sugar', 'Rare', 1),
        (2, 'Golden Caramel', 'Epic', 2),
        (3, 'Mystic Cocoa', 'Legendary', 3),
        (4, 'Glowing Gummy Gel', 'Rare', 4)
    ]
    cur.executemany("INSERT INTO candy_ingredients VALUES (?, ?, ?, ?)", candy_ingredients_data)

    # Commit changes
    conn.commit()
    return conn
