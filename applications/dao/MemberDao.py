from applications.lib import PostgresDatabase

def dt_data_member(search, offset):
    db = PostgresDatabase()
    query = """
        SELECT
            member_id,
            member_name,
            member_phone,
            member_address,
            member_notes,
            member_alternative,
            member_contact_person
        FROM
            ms_member
        WHERE
            CAST(member_id AS TEXT) ILIKE %(search)s OR
            member_name ILIKE %(search)s OR
            member_phone ILIKE %(search)s OR
            member_notes ILIKE %(search)s OR
            member_alternative ILIKE %(search)s OR
            member_contact_person ILIKE %(search)s
        ORDER BY
            member_id desc;
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }

    return db.execute_dt(query, param, limit=50)

def get_data_member_filter(search):
    db = PostgresDatabase()
    query = """
        SELECT
            member_id as "ID Pelanggan",
            member_name as "Nama Pelanggan",
            member_phone as "Telepon Pelanggan",
            member_address as "Alamat",
            member_notes as "Catatan Pelanggan",
            member_alternative as "Alternatif Pelanggan",
            member_contact_person as "Pelanggan Kontak Person"
        FROM
            ms_member
        WHERE
            CAST(member_id AS TEXT) ILIKE %(search)s OR
            member_name ILIKE %(search)s OR
            member_phone ILIKE %(search)s OR
            member_notes ILIKE %(search)s OR
            member_alternative ILIKE %(search)s OR
            member_contact_person ILIKE %(search)s
        ORDER BY
            member_id;
    """
    param = {
        "search": f"%{search}%"
    }

    return db.execute(query, param)

def update_data_member(data):
    db = PostgresDatabase()
    query = """
        UPDATE 
            ms_member
        SET
            member_name = %(member_name)s,
            member_phone = %(member_phone)s,
            member_address = %(member_address)s,
            member_notes = %(member_notes)s,
            member_alternative = %(member_alternative)s,
            member_contact_person = %(member_contact_person)s
        WHERE
            member_id = %(member_id)s
    """
    param = {
        "member_name" : data['member_name'],
        "member_phone" : data['member_phone'],
        "member_address" : data['member_address'],
        "member_notes" : data['member_notes'],
        "member_alternative" : data['member_alternative'],
        "member_contact_person" : data['member_contact_person'],
        "member_id" : data['member_id']
    }

    return db.execute(query, param)

def delete_data_member(member_id):
    db = PostgresDatabase()
    query = """
        DELETE
        FROM 
            ms_member
        WHERE
            member_id = %(member_id)s
    """
    param = {
        "member_id" : member_id
    }

    return db.execute(query, param)

def add_data_member(data):
    db = PostgresDatabase()
    query = """
        INSERT INTO 
            ms_member 
                (member_name, member_phone, member_address, member_note, member_alternative, member_contact_person) 
        VALUES 
                (%(member_name)s, %(member_phone)s, %(member_address)s, %(member_notes)s, %(member_alternative)s, %(member_contact_person)s);
    """
    param = data

    return db.execute(query, param)

def check_id_member(member_id):
    db = PostgresDatabase()
    query = """
        SELECT
            member_id
        FROM
            ms_member
        WHERE
            member_id = %(member_id)s
    """
    param = {
        'member_id': member_id 
    }
    return db.execute(query, param)

def get_all_member():
    db = PostgresDatabase()
    query = """
        SELECT
            member_name Member_Name,
            member_phone Member_Phone,
            member_address Member_Address,
            member_notes Member_Notes
            member_alternative Member_Alternative
            member_contact_person Member_Contact_Person
        FROM
            ms_member
        ORDER BY
            member_id desc;
    """
    return db.execute(query)