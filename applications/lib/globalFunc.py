from applications.lib import PostgresDatabase
from datetime import datetime

def generate_faktur(head):
    db = PostgresDatabase()
    ordinal_num = 0
    query = """
        SELECT * 
        FROM 
            tx_ofaktur
        WHERE 
            head_fak = %(head_fak)s
    """
    param = {'head_fak': head}

    res = db.execute(query, param).result
    if res:
        ordinal_num = int(res[0]['ordinal_number']) + 1
    else : 
        query = """
            INSERT INTO 
                tx_ofaktur (head_fak, ordinal_number) 
            VALUES 
                (%(head_fak)s, '1');
            """
        param = {'head_fak': head}
        db.execute(query, param)
        ordinal_num = 1
    faktur = f"{head}{format(ordinal_num,'03')}"
    return faktur

def update_faktur(faktur,conn):
    head = faktur[:-3]
    ordinal = int(faktur[-3:])

    query = """
            INSERT INTO
                tx_ofaktur (head_fak, ordinal_number)
            VALUES
                (%(head_fak)s, '1')
            ON CONFLICT
                (head_fak)
            DO UPDATE
            SET
                ordinal_number = %(ordinal_number)s;
            """
    param = {'head_fak': head,'ordinal_number': str(ordinal)}
    return conn.execute_preserve(query, param)


def to_date(string):
    date = datetime.strptime(string,'%Y-%m-%d')
    return date