import psycopg2

def get_db_connection():

    conn = psycopg2.connect(
        database="loop-test",
        user='postgres',
        password='admin', 
        host='localhost',
        port='5432'
    )
    return conn

def insert_store_status():
    conn = get_db_connection()
    cursor = conn.cursor()

    path = r"C:\\Users\\lenovo\\Downloads\\Test\\store_status.csv"

    sql = f'''COPY store_status(store_id,status,timestamp_utc)
    # FROM '{path}'
    # DELIMITER ','
    # CSV HEADER;'''
    cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()

    return True

def insert_s_results():
    conn = get_db_connection()
    cursor = conn.cursor()

    path = r"C:\\Users\\lenovo\\Downloads\\Test\\s_results.csv"

    sql = f'''COPY bq_results(store_id,timezone_str)
    FROM '{path}'
    CSV HEADER;'''
    cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()

    return True

def insert_menu_hours():
    conn = get_db_connection()
    cursor = conn.cursor()

    path = r"C:\\Users\\lenovo\\Downloads\\Test\\Menu_hours.csv"

    sql = f'''COPY menu_hours(store_id,day,start_time_local,end_time_local)
    FROM '{path}'
    CSV HEADER;'''
    cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()

    return True

def get_report_id():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    WITH TABLEE AS (
    SELECT store_status.store_id FROM store_status
    UNION
    SELECT menu_hours.store_id FROM menu_hours
    UNION
    SELECT bq_results.store_id FROM bq_results
    ) select * from TABLEE order by random() limit 1;
    """

    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    return result

def get_csv(store_id):
    sql = f"SELECT store_id, up_time_last_hour, up_time_last_day, up_time_last_week, down_time_last_hour, down_time_last_day, down_time_last_week FROM result WHERE (store_id = {store_id}) AND (flag = 'new')"
    conn = get_db_connection()
    cursor = conn.cursor()
    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(sql)

    with open('result_file.csv', 'w') as f:
        cursor.copy_expert(outputquery, f)

    conn.close
    return True

def update_flag(store_id):
    sql = f"""
    UPDATE result SET flag = 'fetched' WHERE store_id = {store_id}
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()

    return True
