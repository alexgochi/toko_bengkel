from applications.lib import PostgresDatabase
from applications.lib.globalFunc import generate_faktur,to_date,update_faktur
import datetime
from flask import request

def getDataOutlet(id=''):
    db = PostgresDatabase()
    param=''
    if id:
        param = f"AND outlet_id = {id}"
    query = f"""
        SELECT 
            outlet_id, 
            outlet_name
        FROM 
            ms_outlet
        WHERE 
            outlet_status = true
        {param};
    """
    return db.execute(query)

def getDataMember():
    db = PostgresDatabase()
    query = """
        SELECT
            member_id,
            member_name,
            member_address,
            member_phone
        FROM 
            ms_member;
    """
    return db.execute(query)

def getPaymentType():
    db = PostgresDatabase()
    query = """
        SELECT 
            type_id, 
            type_name
        FROM 
            ms_payment_type
        WHERE
            type_status = true
    """
    return db.execute(query)

def getRekening(rekening_no=''):
    db = PostgresDatabase()
    param = ''
    if rekening_no:
        param = f"AND rekening_no = {rekening_no}"
    query = f"""
        SELECT 
            rekening_no,
            rekening_name,
            rekening_bank
        FROM 
            ms_rekening
        WHERE 
            rekening_status = true
        {param}
        ORDER BY rekening_bank;
    """
    return db.execute(query)

def getDataMemberById(member_id):
    db = PostgresDatabase()
    query = """
        SELECT
            member_id,
            member_name,
            member_address,
            member_phone
        FROM 
            ms_member
        WHERE member_id = %(member_id)s;
    """
    param = { "member_id" : member_id }
    return db.execute(query, param)

def getDataLovProduct():
    db = PostgresDatabase()
    query = """
        SELECT
            sku,
            product_name,
            merk_name,
            qty
        FROM
            ms_product mp
        INNER JOIN ms_merk mm on mm.merk_id = mp.merk_id
    """
    return db.execute(query)

def dt_lovProduct(search, offset):
    db = PostgresDatabase()
    query = """
        SELECT
            sku,
            CASE WHEN f_print_vehicle is true
                THEN product_name || ' ' || COALESCE(vehicle,'')
                ELSE product_name
            END product_name,
            merk_name,
            category_name,
            part_number,
            qty
        FROM
            ms_product mp
        INNER JOIN 
                ms_merk mm on mm.merk_id = mp.merk_id
        INNER JOIN 
                ms_category mc on mm.category_id = mc.category_id
        WHERE
            CAST(sku AS TEXT) ILIKE %(search)s OR
            product_name ILIKE %(search)s OR
            merk_name ILIKE %(search)s OR
            part_number ILIKE %(search)s 
        ORDER BY 
            CASE WHEN sku < 'A'
                THEN lpad(sku, 255, '0')
            ELSE sku
                END;;
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }
    
    return db.execute_dt(query, param, limit=25)

def getDataBySkuBarcode(search):
    db = PostgresDatabase()
    query = """
        SELECT
            sku,
            part_number,
            CASE WHEN f_print_vehicle is true
                THEN product_name || ' ' || COALESCE(vehicle,'')
                ELSE product_name
            END product_name,
            mp.merk_id,
            category_name,
            merk_name,
            harga_jual,
            harga_beli,
            qty
        FROM
            ms_product mp
        INNER JOIN ms_merk mm on mm.merk_id = mp.merk_id
        INNER JOIN ms_category mc on mm.category_id = mc.category_id
        WHERE
            sku = %(search)s OR
            CAST(barcode AS TEXT) =  %(search)s
    """
    param = {
        'search' : search
    }
    return db.execute(query, param)

def dt_data_dashboard(search, offset, orderBy):
    db = PostgresDatabase()
    query = f"""
        SELECT
            faktur,
            to_char(date_tx, 'dd-mm-yyyy') as date_tx,
            COALESCE(mm.member_name,'Bukan Pelanggan') as member_name,
            total_faktur + other_fee as total_faktur,
            CASE
                WHEN status = false THEN 'Draft'
                ELSE 'Done'
            END as status
        FROM tx_trans
        LEFT JOIN ms_member mm
            ON tx_trans.member_id = mm.member_id
        WHERE (member_name ILIKE %(search)s OR
              faktur ILIKE %(search)s OR
              to_char(date_tx, 'dd-mm-yyyy') ILIKE %(search)s)
              AND status = false
        ORDER BY
            {orderBy}
    """
    param = {
        "search": f"%{search}%",
        "offset": offset,
    }

    return db.execute_dt(query, param, limit=25)


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

def delete_data_dashboard(faktur):
    try:
        db = PostgresDatabase()
        # Delete tx_trans
        query = """
            DELETE
            FROM 
                tx_trans
            WHERE
                faktur = %(faktur)s
        """
        param = {
            "faktur" : faktur
        }

        hasil = db.execute_preserve(query,param)
        if hasil.is_error:
            return hasil
        
        # Delete tx_trans_detail
        query = """
            DELETE
            FROM 
                tx_trans_detail
            WHERE
                faktur = %(faktur)s
        """
        param = {
            "faktur" : faktur
        }

        hasil = db.execute_preserve(query,param)
        if hasil.is_error:
            return hasil
        
        return db.commit()
    finally:
        db.release_connection()

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

def save_order(data,type = 'draft'):
    db = PostgresDatabase()
    now = datetime.datetime.now()
    
    faktur = ''
    if "faktur" not in data:
        date = to_date(data['tanggal'])
        head = f"{data['outletId']}{date.strftime('%m%y')}"
        faktur = generate_faktur(head)
        data['faktur'] = faktur
    else:
        faktur = data['faktur']

    try:
        query = """
            INSERT INTO
                tx_trans (faktur, date_tx, tx_type, due_date, member_id,
                        status, other_fee, other_note, update_date, diskon,
                        total_faktur, payment_id, payment_info, time_tx)
            VALUES
                (%(faktur)s, %(date_tx)s, %(tx_type)s, %(due_date)s, %(member_id)s,
                    %(status)s, %(other_fee)s, %(other_note)s, %(update_date)s, %(diskon)s,
                    %(total_faktur)s, %(payment_id)s, %(payment_info)s, %(time_tx)s)
            ON CONFLICT (faktur)
            DO UPDATE
            SET faktur = excluded.faktur, date_tx = excluded.date_tx, tx_type = excluded.tx_type,
                due_date = excluded.due_date, member_id = excluded.member_id, status = excluded.status,
                other_fee = excluded.other_fee, other_note = excluded.other_note, update_date = excluded.update_date,
                diskon = excluded.diskon, total_faktur = excluded.total_faktur, payment_id = excluded.payment_id,
                payment_info = excluded.payment_info, time_tx = excluded.time_tx;
        """
        param = {
                "faktur": data['faktur'], "date_tx":  data['tanggal'], "tx_type":  data['jenisFaktur'],
                "due_date":  data['jatuhTempo'], "member_id":  data['memberId'], "status":  data['status'],
                "other_fee":  data['ongkir'], "other_note":  data['keterangan'], "update_date":  now.strftime('%Y-%m-%d'),
                "total_faktur":  data['subtotal'], "payment_id":  data['payment_id'], "payment_info":  data['payment_info'],
                "time_tx":  now.strftime('%H:%M:%S'), "diskon": data['diskon']
            }
        hasil = db.execute_preserve(query,param)
        if hasil.is_error:
            return hasil

        # Delete 
        query = """
            DELETE 
            FROM 
                tx_trans_detail 
            WHERE 
                faktur = %(faktur)s
        """
        param = { "faktur": data['faktur']}
        hasil = db.execute_preserve(query,param)
        if hasil.is_error:
            return hasil

        # insert detail
        trans_detail = data['trans_detail']
        for i in trans_detail:
            query = """
                INSERT INTO
                    tx_trans_detail (faktur, sku, part_number, product_name, merk_name, qty, price)
                VALUES
                    (%(faktur)s, %(sku)s, %(part_number)s, %(product_name)s, %(merk_name)s, %(qty)s, %(price)s)
            """
            param = {
                    "faktur": data['faktur'], "sku":  i['sku'], "part_number":  i['part_number'],
                    "product_name":  i['product_name'], "merk_name":  i['merk_name'], "qty":  i['qty'],
                    "price":  i['price']
                }
            hasil = db.execute_preserve(query,param)
            if hasil.is_error:
                return hasil
            
            # Kalau fix dia ngurangin qty nya
            if type == 'invoice':
                hasil = update_qty_product(i['sku'], float(i['qty']), db)
                if hasil.is_error:
                    return hasil
                
        hasil = update_faktur(data['faktur'], db)
        if hasil.is_error:
            return hasil
        
        return db.commit(),faktur
    finally:
        db.release_connection()

def update_qty_product(sku, qty ,conn):
    query = """
        UPDATE ms_product mp
        SET qty = x.qty
        FROM 
            (SELECT qty-%(qty)s qty, sku,outlet_id from ms_product where sku = %(sku)s) x
        WHERE mp.sku = x.sku;
    """
    param = {
            "sku":  sku, 
            "qty":  qty
        }
    hasil = conn.execute_preserve(query,param)
    if hasil.is_error:
        return hasil    
    return hasil

def getTransDraftData(faktur):
    db = PostgresDatabase()
    dataFaktur={}
    query = """
        SELECT
            faktur,
            date_tx,
            tx_type,
            due_date,
            member_id,
            status,
            other_fee,
            other_note,
            update_date,
            total_faktur,
            payment_id,
            payment_info,
            diskon
        FROM
            tx_trans
        WHERE   
            faktur = %(faktur)s;
    """
    param = {
        "faktur": faktur,
    }
    dataFaktur = db.execute(query, param).result[0]

    query = """
        SELECT
            faktur, sku, part_number, product_name, merk_name, qty, price as harga_jual
        FROM
            tx_trans_detail
        WHERE   
            faktur = %(faktur)s;
    """
    param = {
        "faktur": faktur,
    }
    dataFaktur['product'] = db.execute(query, param).result

    return dataFaktur
