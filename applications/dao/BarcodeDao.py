from applications.lib import PostgresDatabase

def getDataBySkuBarcode(search):
    db = PostgresDatabase()
    query = """
        SELECT 
            sku,
            product_name,
            merk_name,
            barcode,
            harga_jual,
            CASE WHEN f_print_vehicle is true
                THEN COALESCE(vehicle,'')
                ELSE ' '
            END vehicle,
            category_name,
            part_number,
            mp.outlet_id as outlet_name
        FROM ms_product mp
            INNER JOIN ms_merk mm on mm.merk_id = mp.merk_id
            INNER JOIN ms_category mc on mc.category_id = mp.category_id
            INNER JOIN ms_outlet mo on mp.outlet_id = mo.outlet_id
        WHERE
            UPPER(sku) = %(search)s OR
            CAST(barcode AS TEXT) =  %(search)s
    """
    param = {
        'search' : search
    }
    return db.execute(query, param)