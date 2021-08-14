from flask_apscheduler import APScheduler
from internal.job.chaos import chaos_func
from internal.job.crawler_xiachufang import get_foods_job
from internal.server.main import app
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import fcntl
from internal.utils.log import LOGGER


def start_server():
    f = open("scheduler.lock", "wb")

    try:

        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler = BackgroundScheduler()

        scheduler.add_job(func=chaos_func, id='apscheduler_chaos', trigger='interval', minutes=45,
                          replace_existing=True)
        # scheduler.add_job(func=get_foods_job, id='apscheduler_xcf', trigger='interval', minutes=0.1,
        #                   replace_existing=True)
        scheduler.start()
    except Exception as e:
        LOGGER.warning("Locked on scheduler.lock")
    app.run(host="0.0.0.0", port=10009, debug=True)

