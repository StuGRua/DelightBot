import uvicorn as uvicorn

from internal.server.main import app


def start_server():
    app.run(host="0.0.0.0", port=10009, debug=True)


if __name__ == "__main__":
    start_server()
