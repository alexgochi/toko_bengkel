from applications.lib import PostgresDatabase
from datetime import datetime

def generate_faktur(head):
    db = PostgresDatabase()
    ordinal = 0

    query = """
        SELECT 
            head_fak,
            ordinal_number
        FROM 
            tx_ofaktur 
        WHERE 
            head_fak = %(head_fak)s
    """
    param = {'head_fak': head}

    res = db.execute(query, param).result
    if res:
        ordinal = res[0]['ordinal_number'] + 1
    else : 
        query = """
            INSERT INTO 
                tx_ofaktur (head_fak, ordinal_number) 
            VALUES 
                (%(head_fak)s, 1)
        """
        param = {'head_fak': head}

        db.execute(query, param)
        ordinal = 1

    faktur = f"{head}{format(ordinal,'03')}"

    return faktur

def update_faktur(faktur, conn):
    db = PostgresDatabase()
    head = faktur[:-3]
    ordinal = int(faktur[-3:])

    query = """
        SELECT 
            head_fak,
            ordinal_number
        FROM 
            tx_ofaktur 
        WHERE 
            head_fak = %(head_fak)s
    """
    param = {'head_fak': head}

    res = db.execute(query, param).result
    print("update_faktur: res ", res)

    if res[0]['ordinal_number'] >= ordinal:
        pass
    else:
        query = """
            INSERT INTO
                tx_ofaktur (head_fak, ordinal_number)
            VALUES
                (%(head_fak)s, 1)
            ON CONFLICT
                (head_fak)
            DO UPDATE
            SET
                ordinal_number = %(ordinal_number)s;
        """
        param = {'head_fak': head, 'ordinal_number': ordinal}

    return conn.execute_preserve(query, param)
    
def to_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d')