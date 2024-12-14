import datetime
from applications.lib import PostgresDatabase

def dt_data_trans(search, member, offset, filter):
    db = PostgresDatabase()
    query = f"""
        SELECT faktur,
            to_char(date_tx, 'dd-mm-yyyy') as date_tx,
            coalesce(member_name,'Bukan Pelanggan') as member_name,
            to_char(total_faktur + other_fee - diskon, 'fm999G999G999G999') as total_faktur,
            coalesce(mpt.type_name,'Bon') as type_name,
            CASE WHEN current_date > due_date::int + date_tx and type_name is null
                THEN 'Overdue ' || current_date - (due_date::int + date_tx) ||' hari'
            ELSE coalesce(payment_info,' ') END as payment_info
        FROM tx_trans tt
        LEFT JOIN ms_payment_type mpt on mpt.type_id = tt.payment_id
        LEFT JOIN ms_member mm on mm.member_id = tt.member_id
        WHERE
            STATUS = true 
            AND (
                faktur ILIKE %(search)s OR
                CAST(date_tx AS TEXT) ILIKE %(search)s OR
                payment_info ILIKE %(search)s OR
                type_name ILIKE %(search)s 
            )
            AND coalesce(member_name,'Bukan Pelanggan') ILIKE %(member)s 
            {filter}
        ORDER BY
            date_tx desc, time_tx desc;
    """
    param = {
        "search": f"%{search}%",
        "member": f"%{member}%",
        "offset": offset
    }

    return db.execute_dt(query, param, limit=25)

def get_data_distinct():
    db = PostgresDatabase()
    data = {}
    query = """
        SELECT *
        FROM (SELECT DISTINCT ON member_name
            FROM ms_member)
        ORDER BY member_name;
    """
    data['member'] = db.execute(query).result

    query = """
        SELECT *
        FROM (SELECT DISTINCT ON outlet_name, outlet_id
            FROM ms_outlet)
        ORDER BY outlet_name;
    """
    data['outlet'] = db.execute(query).result
    return data

def getAllDataTransaksi():
    db = PostgresDatabase()
    query = """
        SELECT faktur,
            to_char(date_tx, 'dd-mm-yyyy') as date_tx,
            coalesce(member_name,'Bukan Pelanggan') as member_name,
            total_faktur + other_fee - diskon as total_faktur,
            coalesce(mpt.type_name,' ') as type_name,
            CASE WHEN current_date > due_date::int + date_tx and type_name is null
                THEN 'Overdue ' || current_date- (due_date::int + date_tx) ||' hari'
            ELSE coalesce(payment_info,' ') END as payment_info
        FROM tx_trans tt
        LEFT JOIN ms_payment_type mpt on mpt.type_id = tt.payment_id
        LEFT JOIN ms_member mm on mm.member_id = tt.member_id
        WHERE status = true
        ORDER BY date_tx desc, time_tx desc;
    """
    return db.execute(query)

def getDataTransByFaktur(faktur):
    outlet = faktur[:2]
    data={}
    db = PostgresDatabase()
    query = """
        SELECT 
            faktur,
            to_char(date_tx, 'dd-mm-yyyy') as date_tx,
            tx_type,
            to_char(date_tx + due_date::int,'dd-mm-yyyy') as due_date,
            member_name,
            address,
            phone,
            other_fee,
            other_note,
            to_char(update_date, 'dd-mm-yyyy') as update_date,
            total_faktur,
            diskon,
            coalesce(mpt.type_name,' ') as type_name,
            CASE WHEN current_date > due_date::int + date_tx and type_name is null
                THEN 'Overdue ' || current_date- (due_date::int + date_tx) ||' hari'
            ELSE coalesce(payment_info,' ') END as payment_info,
            time_tx::varchar
        FROM tx_trans tt
            LEFT JOIN ms_payment_type mpt on mpt.type_id = tt.payment_id
            LEFT JOIN ms_member mm on mm.member_id = tt.member_id
        WHERE status = true
        AND faktur = %(faktur)s
        ORDER BY date_tx desc, time_tx desc;
    """
    param = {
        "faktur" : faktur
    }
    data = db.execute(query, param).result[0]
    
    if not data:
        return {'status': False, 'message': 'Data Tidak ditemukan', 'data': {}}
    
    query = """
        SELECT tt.sku,
            mp.part_number,
            tt.product_name,
            mc.category_name  merk_name,
            coalesce(mp.satuan,'') satuan,
            tt.qty,
            price,
            tt.qty * price as subtotal
        FROM tx_trans_detail tt
            INNER JOIN ms_product mp on tt.sku = mp.sku
            INNER JOIN ms_category mc on mc.category_id = mp.category_id
        WHERE faktur = %(faktur)s
        ORDER BY faktur;
    """
    param = {
        "faktur" : faktur
    }
    data['product'] = db.execute(query, param).result

    query = """
        SELECT 
            outlet_id, outlet_name, address, phone
        FROM ms_outlet
        WHERE outlet_id = %(outlet)s;
    """
    param = {
        "outlet" : outlet
    }
    data['outlet'] = db.execute(query, param).result[0]
    return {'status': True, 'message': 'Berhasil get data', 'data': data}


def update_payment_trans(param):
    db = PostgresDatabase()
    query = """
        UPDATE
            tx_trans
        SET tx_type = 2,
            payment_id = %(payment_id)s,
            payment_info= %(payment_info)s,
            update_date= current_date
        WHERE
            faktur = %(faktur)s;
        """
    return db.execute(query, param)