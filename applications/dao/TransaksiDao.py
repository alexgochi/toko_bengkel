from applications.lib import PostgresDatabase

def getAllDataTransaksi():
    db = PostgresDatabase()
    query = """
        SELECT faktur,
            to_char(date_tx, 'dd-mm-yyyy') as date_tx,
            member_name,
            total_faktur,
            mpt.type_name,
            coalesce(payment_info,' ') as payment_info
        FROM tx_trans tt
        INNER JOIN ms_payment_type mpt on mpt.type_id = tt.payment_id
        LEFT JOIN ms_member mm on mm.member_id = tt.member_id
        WHERE status = true
        ORDER BY faktur;
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
            other_fee,
            other_note,
            to_char(update_date, 'dd-mm-yyyy') as update_date,
            total_faktur,
            mpt.type_name,
            coalesce(payment_info,''),
            time_tx::varchar
        FROM tx_trans tt
            INNER JOIN ms_payment_type mpt on mpt.type_id = tt.payment_id
            LEFT JOIN ms_member mm on mm.member_id = tt.member_id
        WHERE status = true
        AND faktur = %(faktur)s
        ORDER BY faktur;
    """
    param = {
        "faktur" : faktur
    }
    data = db.execute(query, param).result[0]
    
    if not data:
        return {'status': False, 'message': 'Data Tidak ditemukan', 'data': {}}
    
    query = """
        SELECT 
            sku, part_number, product_name, merk_name, qty, price, qty*price as subtotal
        FROM tx_trans_detail
        WHERE faktur = %(faktur)s
        ORDER BY faktur;
    """
    param = {
        "faktur" : faktur
    }
    data['product'] = db.execute(query, param).result

    query = """
        SELECT 
            *
        FROM ms_outlet
        WHERE outlet_id = %(outlet)s;
    """
    param = {
        "outlet" : outlet
    }
    data['outlet'] = db.execute(query, param).result[0]
    return {'status': True, 'message': 'Berhasil get data', 'data': data}