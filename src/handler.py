import functools

import psycopg2
from flask import Flask, request
from flask_cors import CORS
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor

from utils import CustomEncoder

DB_HOST = "autogestion-dev.c66d2rypdwyt.us-east-2.rds.amazonaws.com"
DB_NAME = "postgres"
DB_PORT = 5432

conn = None
cursor = None
app = Flask(__name__)
CORS(app)
app.json_encoder = CustomEncoder
app.debug = True

@app.errorhandler(Exception)
def handle_any_error(ex):
    """Función catch-all para manejar errores

    Args:
        ex ([type]): [description]

    Returns:
        [type]: [description]
    """
    # event_id = capture_exception(ex)
    event_id = None

    response = dict(
        event_id=event_id,
        status_code=500,
        message="Ocurrió un error interno.")
    try:
        type_ = type(ex)
        module = type_.__module__
        qualname = type_.__qualname__
    except:
        pass
    else:
        response.update(dict(
            error_class="class:{}.{}".format(module, qualname)))

    return response, 500


def dbconn(func):
    @functools.wraps(func)
    def db_wrapper():
        global conn, cursor
        user = request.get_json().get("user")
        password = request.get_json().get("password")
        conn = psycopg2.connect(
            database=DB_NAME,
            user=user,
            password=password,
            host=DB_HOST,
            port=DB_PORT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        return func()
    return db_wrapper


@app.route("/login", methods=['POST'])
@dbconn
def login():
    user = request.get_json().get('user')
    cursor.execute("""
        SELECT table_name, string_agg( privilege_type, ',')
        FROM information_schema.role_table_grants
        where table_schema = 'autogestion'
        and grantee = %s
        group by table_name ;
    """, (user,))
    conn.commit()
    privileges = cursor.fetchall()
    conn.close()

    response = {
        "role": user,
        "resources": {
            resource: perms.split(",") for resource, perms in
            [tuple(privilege.values()) for privilege in privileges]
        }
    }

    return response, 200


@app.route("/query", methods=['POST'])
@dbconn
def query():
    data = request.get_json()
    resource = f"""autogestion."{data.get('resource')}" """
    action = data.get("action")
    data = data.get("data")

    if action == "SELECT":
        cursor.execute("""
            SELECT * FROM %s
        """, (AsIs(resource), ))
        conn.commit()
        results = cursor.fetchall()
        conn.close()
        return dict(results=[dict(row) for row in results]), 200

    elif action == "INSERT":
        columns = ", ".join([
            f"\"{key}\"" for key in data.keys()])
        cursor.execute("""
            INSERT INTO %s (%s) values %s
            RETURNING *
        """, (
            AsIs(resource),
            AsIs(columns),
            tuple(data.values())
        ))
        conn.commit()
        created = cursor.fetchall()[0]
        conn.close()
        return dict(results=dict(created)), 200

    return dict(), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0')
