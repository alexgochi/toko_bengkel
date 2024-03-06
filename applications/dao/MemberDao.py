from applications.lib import PostgresDatabase

def dt_data_member(search, offset):
    db = PostgresDatabase()
    query = """
        SELECT
            member_id,
            member_name,
            phone,
            email,
            address
        FROM
            ms_member
        WHERE
            member_id ILIKE %(search)s OR
            member_name ILIKE %(search)s OR
            phone ILIKE %(search)s OR
            email ILIKE %(search)s 
        ORDER BY
            member_name;
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }

    return db.execute_dt(query, param)