import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

# CURSOR.commit()

class Dog:

    all = []

    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        # self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """
        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE dogs.name == ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        CONN.commit()

        if row:
            return Dog(row[1], row[2], row[0])
        else:
            return None
        
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE dogs.id = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        CONN.commit()

        if row:
            return Dog(row[1], row[2], row[0])
        else:
            return None
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT *
            FROM dogs
            WHERE dogs.name = ?
            AND dogs.breed = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name, breed)).fetchone()
        CONN.commit()

        if row:
            return Dog(row[1], row[2], row[0])
        else:
            return cls.create(name, breed)
        
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))