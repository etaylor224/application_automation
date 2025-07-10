import asyncpg
import asyncio


_pg_url = "postgresql://postgres@localhost/test"
#TODO Fix url
#TODO add error handling for all pgsql funcs


def check_tables(conn, table):
    query = f"""SELECT EXISTS ( 
    SELECT 1 
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name = '{table}'
"""
    search = conn.fetch(query)
    if search == False:
        return False
    else:
        return True

async def create_tables(conn):

    table_and_query = {
    "searchquery_table" : """
        CREATE TABLE searchquery(
            id interger PRIMARY KEY,
            query character varying(50),
            location character varying(6),
        )
    """,
    "low_result_table" : """
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
    "high_result_table" : """
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
    "applied_table" : """
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

    for entry in table_and_query:
        check = check_tables(conn, entry)
        if not check:
            query = f"""CREATE TABLE {entry}(
                    {table_and_query[entry]})"""
            await conn.execute(query)


async def insert_into_search(conn, position, location):

    query = f"""
    INSERT INTO searchquery_table(query,location) 
    VALUES($1, $2)
    """, position, location
    await conn.execute(query)

async def insert_into_low(conn, data: list):
    #9 columns for each table

    query = """
    INSERT INTO low_result_table(job_title,
    employer_name,
    employer_web,
    employment_type,
    publisher,
    apply_link,
    job_description,
    remote,
    score) 
    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)
    """, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]

    await conn.execute(query)


async def insert_into_high(conn, data: list):
    query = """INSERT INTO high_result_table(job_title,
    employer_name,
    employer_web,
    employment_type,
    publisher,
    apply_link,
    job_description,
    remote,
    score) 
    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) 
    """, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]

    await conn.execute(query)

async def insert_into_applied(conn, data: list):
    query = """INSERT INTO applied_table(job_title,
    employer_name,
    employer_web,
    employment_type,
    publisher,
    apply_link,
    job_description,
    remote,
    score) 
    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) 
    """, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]

    await conn.execute(query)

def remove_row():
    #TODO this will be a call to remove a tow
    pass

async def populate_table_call(table):
    #TODO query table data to populate web page, any table
    query = f"""
    SELECT * FROM {table}
    """

async def check_for_duplicate():
    pass


async def create_pg_conn():
    """Opens connection to posgresql database and returns connection"""
    return await asyncpg.connect(_pg_url)

