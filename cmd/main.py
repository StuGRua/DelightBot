import uvicorn as uvicorn

from internal.server.main import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10009, debug=True)