import uvicorn as uvicorn

from internal.server.main import app
from internal.job.chaos import scheduler


def start_server():
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="0.0.0.0", port=10009, debug=True)


if __name__ == "__main__":
    start_server()
