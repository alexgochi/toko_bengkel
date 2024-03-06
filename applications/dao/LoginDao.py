from func import select_req
from applications.lib import PostgresDatabase

def dt_data_user(search, offset):
    db = PostgresDatabase()
    query = """
        SELECT
            user_id,
            name
        FROM
            ms_user
        WHERE
            user_id ILIKE %(search)s OR
            name ILIKE %(search)s
        ORDER BY
            name;
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }

    return db.execute_dt(query, param)

def findUser():
    data = select_req("select user_id,name,level from ms_user")
    return data


def getLogin(id, pin):
    data = select_req(
        f"select * from ms_user where user_id= %(user_id)s and pin=%(pin)s", {'user_id': id, 'pin': pin})
    return data

def get_user_by_id(user_id):
    db = PostgresDatabase()
    query = """
        SELECT
            *
        FROM
            ms_user
        WHERE
            user_id = %(user_id)s;
    """
    param = {
        "user_id": user_id
    }
    return db.execute(query, param)