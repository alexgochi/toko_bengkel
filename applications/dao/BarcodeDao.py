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
            vehicle,
            category_name,
            part_number
        FROM ms_product mp
            INNER JOIN ms_merk mm on mm.merk_id = mp.merk_id
            INNER JOIN ms_category mc on mc.category_id = mp.category_id
        WHERE
            UPPER(sku) = %(search)s OR
            CAST(barcode AS TEXT) =  %(search)s
    """
    param = {
        'search' : search
    }
    return db.execute(query, param)