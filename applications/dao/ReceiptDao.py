from applications.lib import PostgresDatabase
from applications.lib.globalFunc import generate_faktur,to_date,update_faktur
import datetime

def dt_data_receipt(search, storeBuy, offset, filter):
    db = PostgresDatabase()
    query = f"""
        SELECT faktur,
            to_char(date_tx, 'dd-mm-yyyy') as date_tx,
            store_buy,
            to_char(total_faktur + other_fee - discount, 'fm999G999G999G999') as total_faktur
        FROM tx_receipt
        WHERE  
            faktur is not null AND
            (CAST(date_tx AS TEXT) ILIKE %(search)s OR
            store_buy ILIKE %(search)s OR
            faktur ILIKE %(search)s)
            AND store_buy ILIKE %(storeBuy)s
            {filter}
        ORDER BY
            faktur;
    """
    param = {
        "search": f"%{search}%",
        "storeBuy": f"%{storeBuy}%",
        "offset": offset
    }

    return db.execute_dt(query, param, limit=25)

def get_data_distinct():
    db = PostgresDatabase()
    data = {}
    query = """
        SELECT *
        FROM (SELECT DISTINCT ON (upper(store_buy)) store_buy
            FROM tx_receipt)
        WHERE
            store_buy is not null 
            AND store_buy <>''
        ORDER BY store_buy;
    """
    data['store_buy'] = db.execute(query).result
    return data

def getAllDataReceipt():
    db = PostgresDatabase()
    query = """
        SELECT faktur,
            to_char(date_tx, 'dd-mm-yyyy') as date_tx,
            store_buy,
            total_faktur + other_fee - discount as total_faktur
        FROM tx_receipt
        ORDER BY faktur;
    """
    return db.execute(query)

def save_receipt(data):
    db = PostgresDatabase()
    now = datetime.datetime.now()
    
    faktur = ''
    if "faktur" not in data:
        date = to_date(data['tanggal'])
        head = f"P-{data['outletId']}-{date.strftime('%d%m%y')}"
        faktur = generate_faktur(head)
        data['faktur'] = faktur

    print(data)
    try:
        query = """
            INSERT INTO tx_receipt 
                (faktur, date_tx, store_buy, total_faktur, 
                discount, other_fee, other_note, update_date)
            VALUES  
                (%(faktur)s,%(date_tx)s,%(store_buy)s,%(total_faktur)s,
                %(discount)s,%(other_fee)s,%(other_note)s,%(update_date)s);   
        """
        param = {
                "faktur": data['faktur'], "date_tx":  data['tanggal'], "store_buy": data['store_buy'],
                "other_fee":  data['other_fee'], "other_note":  data['other_note'], 
                "update_date":  now.strftime('%Y-%m-%d'), "total_faktur":  data['subtotal'],
                "discount": data['discount']
            }
        hasil = db.execute_preserve(query,param)
        if hasil.is_error:
            return hasil

        # insert detail
        receipt_detail = data['receipt_detail']
        for i in receipt_detail:
            query = """
                INSERT INTO
                    tx_receipt_detail (faktur, sku, part_number, product_name, merk_name, qty, price)
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
            
            query = """
                UPDATE ms_product mp
                SET qty = x.qty,
                    harga_jual = %(hjual)s
                FROM 
                    (SELECT qty+%(qty)s qty, sku,outlet_id from ms_product where sku = %(sku)s) x
                WHERE mp.sku = x.sku;
            """
            param = {
                    "sku":  i['sku'], 
                    "qty":  i['qty'],
                    "hjual": i['hjual']
                }
            hasil = db.execute_preserve(query,param)
            if hasil.is_error:
                return hasil    
        
        if data['update_price']:
            for i in data['update_price']:
                query = """
                    UPDATE ms_product
                    SET harga_beli = %(hbeli)s
                    WHERE sku = %(sku)s;
                    """
                param = {
                        "hbeli": i['hbeli'], "sku":  i['sku']
                    }
                hasil = db.execute_preserve(query,param)
                if hasil.is_error:
                    return hasil
                
        hasil = update_faktur(data['faktur'], db)
        if hasil.is_error:
            return hasil
        
        return db.commit()
    finally:
        db.release_connection()

def getDataRecByFaktur(faktur):
    data={}
    db = PostgresDatabase()
    query = """
        SELECT faktur,
            TO_CHAR(date_tx, 'dd-mm-yyyy') AS date_tx,
            store_buy,
            total_faktur,
            discount,
            other_fee,
            other_note,
            update_date
        FROM tx_receipt
        WHERE faktur = %(faktur)s;
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
        FROM tx_receipt_detail
        WHERE faktur = %(faktur)s
        ORDER BY 
            CASE WHEN sku < 'A'
                THEN lpad(sku, 255, '0')
            ELSE sku
                END;
    """
    param = {
        "faktur" : faktur
    }
    data['product'] = db.execute(query, param).result
    return {'status': True, 'message': 'Berhasil get data', 'data': data}