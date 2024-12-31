from applications.lib import PostgresDatabase
import random
from flask import jsonify

def get_data_merk(category_id):
    db = PostgresDatabase()
    query = """
        SELECT
            merk_id,
            merk_name
        FROM
            ms_merk
        WHERE
            category_id = %(category_id)s
    """
    param = {
        "category_id" : category_id
    }
    return db.execute(query, param)

def get_data_distinct():
    db = PostgresDatabase()
    data = {}
    query = """
        SELECT *
        FROM (SELECT DISTINCT category_name FROM ms_category) AS category_name
        ORDER BY category_name;
    """
    data['category'] = db.execute(query).result

    query = """
        SELECT *
        FROM (SELECT DISTINCT merk_name FROM ms_merk) AS merk_name
        ORDER BY merk_name;
    """
    data['merk'] = db.execute(query).result

    query = """
        SELECT *
        FROM (SELECT DISTINCT outlet_name FROM ms_outlet) AS outlet_name
        ORDER BY outlet_name;
    """
    data['outlet'] = db.execute(query).result

    query = """
        SELECT *
        FROM (SELECT DISTINCT vehicle FROM ms_product WHERE vehicle is not null AND vehicle <> '-') AS vehicle
        ORDER BY vehicle;
    """
    data['vehicle'] = db.execute(query).result
    return data

def get_data_category():
    db = PostgresDatabase()
    query = """
        SELECT
            category_id,
            category_name
        FROM
            ms_category
    """
    return db.execute(query)

def get_data_outlet():
    db = PostgresDatabase()
    query = """
        SELECT
            outlet_id,
            outlet_name
        FROM
            ms_outlet
    """
    return db.execute(query)

def dt_data_product(search, category, merk, vehicle, offset, filter):
    db = PostgresDatabase()
    query = f"""
        SELECT
            sku,
            part_number,
            alternative_part_number,
            descriptions_product,
            product_name,
            barcode,
            vehicle,
            f_print_vehicle,
            merk_name,
            category_name,
            outlet_name,
            qty,
            satuan,
            harga_beli,
            harga_jual,
            case when f_stock_opname is true Then 'Valid'
            when f_stock_opname is false THEN 'Invalid' 
            END f_stock_opname,
            mp.category_id,
            mp.merk_id,
            mp.outlet_id
        FROM
            ms_product mp
            INNER JOIN ms_merk mm on mm.merk_id = mp.merk_id
            INNER JOIN ms_category mc on mc.category_id = mp.category_id
            INNER JOIN ms_outlet mo on mo.outlet_id = mp.outlet_id
        WHERE
            sku is not null AND (
            CAST (sku AS TEXT) ILIKE %(search)s OR
            part_number ILIKE %(search)s OR										
            product_name ILIKE %(search)s OR
            descriptions_product ILIKE %(search)s OR
            alternative_part_number ILIKE %(search)s OR
            case when f_stock_opname is true Then 'Valid'
            when f_stock_opname is false THEN 'Invalid' 
            END ILIKE %(stock_opname)s OR
            CAST(barcode AS TEXT) ILIKE %(search)s)
            AND merk_name ILIKE %(category)s
            AND category_name ILIKE %(merk)s
            AND vehicle ILIKE %(vehicle)s
            {filter}
    """
    param = {
        "search": f"%{search}%",
        "stock_opname": f"{search}%",
        "category": f"{category}%",
        "merk": f"%{merk}%",
        "vehicle": f"%{vehicle}%",
        "offset": offset
    }
    return db.execute_dt(query, param, limit=25)

def get_data_product_filter(search, category, merk, vehicle, filter):
    db = PostgresDatabase()
    query = f"""
        SELECT
            sku "SKU",
            part_number as "Part Number",
            alternative_part_number as "Alternatif Part Number",
            descriptions_product as "Deskripsi Produk",
            product_name as "Nama Produk",
            barcode as "Barcode",
            vehicle as "Kendaraan",
            merk_name  as "Nama Kategori",
            category_name as "Nama Merk",
            outlet_name as "Nama Outlet",
            qty as "Qty",
            satuan as "Satuan",
            harga_beli as "Harga Beli",
            harga_jual as "Harga Jual",
            case when f_stock_opname is true Then 'Valid'
            when f_stock_opname is false THEN 'Invalid' 
            END as "Stock Opname"
        FROM
            ms_product mp
            INNER JOIN ms_merk mm on mm.merk_id = mp.merk_id
            INNER JOIN ms_category mc on mc.category_id = mp.category_id
            INNER JOIN ms_outlet mo on mo.outlet_id = mp.outlet_id
        WHERE
            sku is not null AND (
            CAST (sku AS TEXT) ILIKE %(search)s OR
            part_number ILIKE %(search)s OR
            alternative_part_number ILIKE %(search)s OR
            descriptions_product ILIKE %(search)s OR
            case when f_stock_opname is true Then 'Valid'
            when f_stock_opname is false THEN 'Invalid' 
            END ILIKE (stock_opname)s% OR
            product_name ILIKE %(search)s OR
            CAST(barcode AS TEXT) ILIKE %(search)s)
            AND merk_name ILIKE %(category)s
            AND category_name ILIKE %(merk)s
            AND vehicle ILIKE %(vehicle)s
            {filter}
    """
    param = {
        "search": f"%{search}%",
        "stock_opname": f"{search}%",
        "category": f"{category}%",
        "merk": f"%{merk}%",
        "vehicle": f"%{vehicle}%"
    }
    return db.execute(query, param)

def checkProductdbExist(data):
    db = PostgresDatabase()
    print(data)
    query = """
        SELECT product_name
        FROM ms_product
        WHERE product_name = %(product_name)s
        AND merk_id = %(merk_id)s
        AND category_id = %(category_id)s
        AND part_number = %(part_number)s
        AND vehicle = %(vehicle)s
        AND sku != %(sku)s
        AND outlet_id = %(outlet_id)s
    """
    param = data
    res = db.execute(query, param)
    if res.is_error:
        return {"status": False, "message": res.pgerror}
    if res.result:
        return {"status": False, "message": "Error, Ket : Nama Produk Bentrok / Duplikat"}
    return {"status": True, "message": ""}

def update_data_product(data):
    db = PostgresDatabase()
    query = """
        UPDATE 
            ms_product
        SET
            part_number = %(part_number)s,
            alternative_part_number = %(alternative_part_number)s,
            product_name = %(product_name)s,
            descriptions_product = %(descriptions_product)s,
            vehicle = %(vehicle)s,
            merk_id = %(merk_id)s,
            category_id = %(category_id)s,
            outlet_id = %(outlet_id)s,
            qty = %(qty)s,
            satuan = %(satuan)s,
            harga_beli = %(harga_beli)s,
            harga_jual = %(harga_jual)s,
            barcode = %(barcode)s,
            f_print_vehicle = %(f_print_vehicle)s,
            f_stock_opname = %(f_stock_opname)s
        WHERE
            sku = %(sku)s
    """
    param = data

    return db.execute(query, param)

def delete_data_product(id):
    db = PostgresDatabase()
    query = """
        DELETE
        FROM 
            ms_product
        WHERE
            sku = %(sku)s
    """
    param = {
        "sku" : id
    }

    return db.execute(query, param)

def add_data_product(data):
    try:
        db = PostgresDatabase()
        query = """
            INSERT INTO 
                ms_product 
                    (sku, part_number, alternative_part_number, descriptions_product, product_name, vehicle, merk_id, category_id, outlet_id, qty, satuan, harga_beli, harga_jual, barcode, f_print_vehicle, f_stock_opname) 
            VALUES 
                    (%(sku)s, %(part_number)s, %(alternative_part_number)s, %(descriptions_product)s, %(product_name)s, %(vehicle)s, %(merk_id)s, %(category_id)s, %(outlet_id)s, %(qty)s, %(satuan)s, %(harga_beli)s, %(harga_jual)s, %(barcode)s, %(f_print_vehicle)s, %(f_stock_opname)s);
        """
        param = data

        hasil = db.execute_preserve(query,param)
        if hasil.is_error:
            return hasil
        
        hasil = update_sku(db, data['sku'])
        if hasil.is_error:
            return hasil

        return db.commit()
    finally:
        db.release_connection()

def generate_barcode():
    temp = random.randint(10000000,99999999)
    db = PostgresDatabase()
    query = """
        SELECT
            sku
        FROM
            ms_product
        WHERE
            barcode = %(temp)s
    """
    param = {'temp': temp }
    res = db.execute(query, param)
    if res.result:
        generate_barcode()
    else:   
        return temp

def check_id_product(sku):
    db = PostgresDatabase()
    query = """
        SELECT
            sku
        FROM
            ms_product
        WHERE
            sku = %(sku)s
    """
    param = {'sku': sku }
    return db.execute(query, param)

def generate_sku():
    db = PostgresDatabase()
    ordinal_num = 10000000
    query = """
        SELECT * 
        FROM 
            tx_ofaktur
        WHERE 
            head_fak = 'SKU'
    """
    res = db.execute(query).result
    if res:
        ordinal_num = int(res[0]['ordinal_number']) + 1
    return ordinal_num

def update_sku(conn,num):
    query = """
            INSERT INTO
                tx_ofaktur (head_fak, ordinal_number)
            VALUES
                ('SKU', '1')
            ON CONFLICT
                (head_fak)
            DO UPDATE
            SET
                ordinal_number = %(ordinal_number)s;
            """
    param = {'ordinal_number': str(num)}
    return conn.execute_preserve(query, param)

def get_all_product():
    db = PostgresDatabase()
    query = f"""
        SELECT
            sku as SKU,
            part_number as Part_Number,
            alternative_part_number as Alternative_Part_Number,
            descriptions_product as Descriptions_Product,
            product_name as Nama_Produk,
            barcode as Barcode,
            vehicle as Kendaraan,
            merk_name as Kategori,
            category_name as Merk,
            outlet_name as Nama_Outlet,
            qty as Qty,
            satuan as Satuan,
            harga_beli as Beli,
            harga_jual as Jual
        FROM
            ms_product mp
            INNER JOIN ms_merk mm on mm.merk_id = mp.merk_id
            INNER JOIN ms_category mc on mc.category_id = mp.category_id
            INNER JOIN ms_outlet mo on mo.outlet_id = mp.outlet_id
        ORDER BY 
            sku desc;
        """
    return db.execute(query)