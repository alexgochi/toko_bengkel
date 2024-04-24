from applications.lib import PostgresDatabase

def get_data_merk():
    db = PostgresDatabase()
    query = """
        SELECT
            merk_id,
            merk_name
        FROM
            ms_merk
    """
    return db.execute(query)

def dt_data_category(search, offset, orderBy):
    db = PostgresDatabase()
    query = f"""
        SELECT
            mc.category_id,
            mc.category_name,
            count(*) +
                max(case when mm.category_id is null then -1 else 0 end)
            as jumlah_merk
        FROM ms_category mc
        LEFT JOIN ms_merk mm on mc.category_id = mm.category_id
        WHERE
            category_name ILIKE %(search)s
        GROUP BY
            mc.category_id,
            mc.category_name
        ORDER BY
            {orderBy};
    """
    param = {
        "search": f"%{search}%",
        "offset": offset,
    }

    return db.execute_dt(query, param)


def update_data_category(data):
    db = PostgresDatabase()
    query = """
        UPDATE 
            ms_category
        SET
            category_name = %(category_name)s
        WHERE
            category_id = %(category_id)s
    """
    param = data

    return db.execute(query, param)

def delete_data_category(id):
    db = PostgresDatabase()
    query = """
        DELETE
        FROM 
            ms_category
        WHERE
            category_id = %(id)s
    """
    param = {
        "id" : id
    }

    return db.execute(query, param)

def add_data_category(data):
    db = PostgresDatabase()
    print(data)
    query = """
        INSERT INTO 
            ms_category 
                (category_name) 
        VALUES 
                (%(category_name)s);
    """
    param = data

    return db.execute(query, param)
