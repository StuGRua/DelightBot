from flask_apscheduler import APScheduler
from internal.job.chaos import chaos_func
from internal.job.crawler_xiachufang import get_foods_job
from internal.server.main import app
import atexit
import fcntl
from internal.utils.log import LOGGER


def start_server():
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
        scheduler.add_job(func=chaos_func, id='apscheduler_chaos', args=None, trigger='interval', minutes=30,
                          replace_existing=True)
        scheduler.add_job(func=get_foods_job, id='apscheduler_xcf', args=None, trigger='interval', minutes=120,
                          replace_existing=True)
    except Exception as e:
        LOGGER.warning("Locked on scheduler.lock")

    app.run(host="0.0.0.0", port=10009, debug=True)
