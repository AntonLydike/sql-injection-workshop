import sqlite3
from secrets import token_urlsafe

from fastapi import FastAPI, Security, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN


app = FastAPI(title="SQL Injection Showcase")


def run_statement(sql_statement: str):
    """
    Super smart sql statement execution function that can execute many many sql scripts and
    return results, so it's even better than the connection.executescript, which doesn't return
    any result whatsoever! sqlite should hire me instead to write their functions! this is so smart!

    :param sql_statement: The sql statement(s) to execute
    :return: The last statements result
    """
    conn = sqlite3.connect("data.sqlite")
    cur = conn.cursor()
    try:
        for statement in sql_statement.split(';'):
            if not statement.strip():
                continue
            print(">>> " + statement)
            cur.execute(statement)
        return cur.fetchall()
    finally:
        conn.commit()
        conn.close()


async def authenticate(
        token: str = Security(APIKeyHeader(name="authorization", scheme_name="Bearer", auto_error=True))
):
    res = run_statement("SELECT * FROM sessions WHERE token = '{}'".format(token))
    if not res:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    return token


@app.get('/books/{id}')
def book_by_id(id: str, auth: str = Depends(authenticate)):
    res = run_statement("SELECT * FROM books WHERE id = '{}'".format(id))
    return dict(zip(('id', 'name', 'written', 'authors', 'description'), res[0]))


@app.get('/books/')
def all_books(author: str = None, name: str = None, written: str = None, auth: str = Depends(authenticate)):
    query = 'SELECT * FROM books'
    where = []
    if author is not None:
        where.append("authors LIKE '%{}%'".format(author))
    if name is not None:
        where.append("name LIKE '%{}%'".format(name))
    if written is not None:
        where.append("written = '%{}%'".format(written))
    if where:
        query += " WHERE " + " AND ".join(where)

    res = run_statement(query)

    return [
        dict(zip(('id', 'name', 'written', 'authors', 'description'), row)) for row in res
    ]


@app.post('/login')
def login(username: str, password: str):
    res = run_statement("SELECT * FROM users WHERE username = '{}' and password = '{}'".format(username, password))
    if res:
        session_token = token_urlsafe(32)
        run_statement("INSERT INTO sessions (token) VALUES ('{}')".format(session_token))
        return {"success": True, "token": session_token}
    else:
        return {"success": False, "token": None}
