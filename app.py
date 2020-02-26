from flask import Flask, Request
import redis
import os

app = Flask(__name__)
REDIS_URL = "redis://localhost:6379"

redis_host = os.getenv("REDIS_MASTER_SERVICE_HOST")
redis_port = os.getenv("REDIS_MASTER_SERVICE_PORT")

redis_user = "user"
redis_password = "CfHsTLIuQ6"


@app.route('/')
def main():
    REDIS_VALUES = f"REDIS HOST --> {redis_host}\nREDIS PORT --> {redis_port}"
    ENV_LIST = ""
    for key in os.environ:
        ENV_LIST = ENV_LIST + f"{key} : {os.environ.get(key)}\n"
    return f"{REDIS_VALUES}\n\n{ENV_LIST}"


@app.route('/<parameter>')
def hello_world(parameter=None):
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port)
        r.set("REDIS_MESSAGE", f"REDIS SAYS {parameter}")
        x = r.get("REDIS_MESSAGE")

        if x is not None:
            r.delete("REDIS_MESSAGE")
            r.close()
            return x
        else:
            r.close()
            return 'No message returned'

    except Exception as e:
        return f"Possibly no Redis connection \nException : {e}"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
