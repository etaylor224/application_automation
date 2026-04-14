import yaml
import psycopg2 as psy
from psycopg2.extras import execute_batch

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

_pg_url = config['database_url_test']


#TODO Fix url
#TODO add error handling for all pgsql funcs

def insert_into_search(position, location):
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO searchquery(query,location) 
    VALUES(%s, %s) RETURNING id""", (position, location))
            return cur.fetchone()[0]


def insert_data(table: str, data: list):
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            try:
                for entry in data:
                    already_exists = check_for_duplicates(cur, table, entry)
                    if not already_exists:
                        execute_batch(cur,
                                      f"""
                            INSERT INTO {table}(
                            job_title,
                            employer_name,
                            employer_web,
                            employment_type,
                            publisher,
                            apply_link,
                            job_description,
                            remote,
                            score)          

                            VALUES( 
                            %(job_title)s,
                            %(employer_name)s, 
                            %(employer_web)s,
                            %(employment_type)s,
                            %(publisher)s,
                            %(apply_link)s,
                            %(job_description)s,
                            %(remote)s,
                            %(score)s
                            )
                            """,
                                      data)
                        conn.commit()
            except Exception as e:
                print("Error")
                print(e)


def insert_into_applied(data: list):
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            try:
                drop_old_id = data[0][1:]
                cur.execute(
                              """
                    INSERT INTO applied(
                    job_title,
                    employer_name,
                    employer_web,
                    employment_type,
                    publisher,
                    apply_link,
                    job_description,
                    remote,
                    score)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, drop_old_id)
                conn.commit()
                return True
            except Exception as e:
                print("Error")
                print(e)


def remove_row(table: str, row_id: int):
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
            DELETE FROM {table} WHERE id = %s
            """, (row_id,))
        conn.commit()


def populate_table_call(table):
    """Retrieves data from SQL DB and returns a dict for front end parsing"""
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM public.{table}")
            data = cur.fetchall()
            return data


def get_row_by_id(table: str, row_id: int):
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM public.{table} WHERE id = %s", (row_id,))
            return cur.fetchall()


def check_for_duplicates(conn, table: str, data: dict):
    conn.execute(f"""
        SELECT EXISTS(SELECT 1 FROM {table} WHERE
        job_title = %s AND
        employer_name = %s AND
        employer_web = %s AND
        employment_type = %s AND
        publisher = %s AND
        apply_link = %s AND
        job_description = %s)    
        """, (
        data['job_title'], data['employer_name'], data['employer_web'], data["employment_type"], data["publisher"],
        data["apply_link"], data["job_description"]))
    check = conn.fetchone()

    if check[0]:
        return True
    else:
        return False


def job_data_helper(data):
    column_names = [
        "id",
        "job_title",
        "employer_name",
        "employer_web",
        "employment_type",
        "publisher",
        "apply_link",
        "job_description",
        "remote",
        "score",
    ]

    cleaned = list()
    for entry in data:
        rows = entry
        data_dict = dict()
        for i in range(len(column_names)):
            data_dict[column_names[i]] = rows[i]
        cleaned.append(data_dict)
    return cleaned


def positions_data_helper(data):
    column_names = [
        "id",
        "query",
        "location",
    ]

    cleaned = list()
    for entry in data:
        rows = entry
        data_dict = dict()
        for i in range(len(column_names)):
            data_dict[column_names[i]] = rows[i]
        cleaned.append(data_dict)
    return cleaned


#TODO Remove possible unused funcs

def insert_into_low(data: list):
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            try:
                for entry in data:
                    already_exists = check_for_duplicates(cur, "low_results", entry)
                    if already_exists == False:
                        print("not in db")
                        execute_batch(cur,
                                      """
                            INSERT INTO low_results(
                            job_title,
                            employer_name,
                            employer_web,
                            employment_type,
                            publisher,
                            apply_link,
                            job_description,
                            remote,
                            score)          

                            VALUES( 
                            %(job_title)s,
                            %(employer_name)s, 
                            %(employer_web)s,
                            %(employment_type)s,
                            %(publisher)s,
                            %(apply_link)s,
                            %(job_description)s,
                            %(remote)s,
                            %(score)s
                            )
                            """,
                                      data)
                        conn.commit()
                    else:
                        print("Entry exists")
            except Exception as e:
                print("Error")
                print(e)


def insert_into_high(data: list):
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            try:
                for entry in data:
                    already_exists = check_for_duplicates(cur, "high_results", entry)
                    if already_exists == False:
                        print("not in db")
                        execute_batch(cur,
                                      """
                            INSERT INTO high_results(
                            job_title,
                            employer_name,
                            employer_web,
                            employment_type,
                            publisher,
                            apply_link,
                            job_description,
                            remote,
                            score)          

                            VALUES( 
                            %(job_title)s,
                            %(employer_name)s, 
                            %(employer_web)s,
                            %(employment_type)s,
                            %(publisher)s,
                            %(apply_link)s,
                            %(job_description)s,
                            %(remote)s,
                            %(score)s
                            )
                            """,
                                      data)
                        conn.commit()
                    else:
                        print("Entry exists")
            except Exception as e:
                print("Error")
                print(e)


async def check_tables(conn, table):
    query = f"""SELECT EXISTS ( 
    SELECT 1 
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name = '{table}')
"""
    search = await conn.fetch(query)
    if search == False:
        print(f"Creating table {table}")
        return False

    else:
        print(f"Table {table} exists")
        return True


async def create_tables():
    table_and_query = {
        "searchquery_table": """
        CREATE TABLE searchquery(
            id integer PRIMARY KEY,
            query character varying(50),
            location character varying(50)
        )
    """,
        "low_result_table": """
    CREATE TABLE low_results(
    id integer PRIMARY KEY, 
    job_title character varying(100),
    employer_name character varying (512),
    employer_web character varying (512),
    employment_type character varying (100),
    publisher character varying (150),
    apply_link character varying(1024),
    job_description text,
    remote boolean,
    score real)
    """,
        "high_result_table": """
    CREATE TABLE high_results(
    id integer PRIMARY KEY, 
    job_title character varying(100),
    employer_name character varying (512),
    employer_web character varying (512),
    employment_type character varying (100),
    publisher character varying (150),
    apply_link character varying(1024),
    job_description text,
    remote boolean,
    score real)
    """,
        "applied_table": """
    CREATE TABLE applied(
    id integer PRIMARY KEY, 
    job_title character varying(100),
    employer_name character varying (512),
    employer_web character varying (512),
    employment_type character varying (100),
    publisher character varying (150),
    apply_link character varying(1024),
    job_description text,
    remote boolean,
    score real)
    """
    }
