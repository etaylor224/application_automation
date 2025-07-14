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
                    if already_exists == False:
                        print("not in db")
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
                    else:
                        print("Entry exists")
            except Exception as e:
                print("Error")
                print(e)

def insert_into_applied(data: list):
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            try:
                for entry in data:
                    already_exists = check_for_duplicates(cur, "applied", entry)
                    if already_exists == False:
                        print("not in db")
                        execute_batch(cur,
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


def remove_row():
    #TODO this will be a call to remove a tow
    pass


def populate_table_call(table):
    """Retrieves data from SQL DB and returns a dict for front end parsing"""
    with psy.connect(_pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM public.{table}")
            data = cur.fetchall()
            return data


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
