from flask import Flask, request
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = "autogestion-dev.c66d2rypdwyt.us-east-2.rds.amazonaws.com"
DB_NAME = "postgres"
DB_PORT = 5432

conn = None
cursor = None
app = Flask(__name__)


@app.errorhandler(Exception)
@cross_origin()
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


def db(func):
    def db_wrapper():
        user = request.get_json().get("user")
        password = request.get_json().get("password")
        conn = psycopg2.connect(
            database=DB_NAME,
            user=user,
            password=password,
            host=DB_HOST,
            port=DB_ṔORT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        func()
    return db_wrapper


@app.route("/login", methods=['POST'])
@db
def hello():
    return dict(), 200


@app.route("/query", methods=['POST'])
    data = request.get_json()
    resource = data.get("resource")
    action = data.get("action")

    if action == "SELECT":
        cursor.execute("""
            SELECT * FROM %s
        """, (resource, ))
        conn.commit()
        results = cursor.fetchall()
        conn.close()
        return dict(results), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
