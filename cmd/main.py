from gevent import monkey
from gevent import pywsgi

monkey.patch_all()  # 打上猴子补丁

from internal.server.main import app
from internal.utils.log import LOGGER
from internal.utils.config_to_redis import init_all_config_to_redis
from internal.job.self_corn.selfCorn import init_scheduler


def start_server():
    init_all_config_to_redis()
    init_scheduler()
    app.debug = True
    server = pywsgi.WSGIServer(('127.0.0.1', 10009), app)
    server.serve_forever()
