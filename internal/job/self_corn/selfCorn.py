from apscheduler.schedulers.background import BackgroundScheduler

from internal.job.chaos import chaos_func
from internal.job.check_player_online import check_all_players
from internal.job.get_bili_pics import update_cos_pics_to_redis
from internal.service.cos.random_cos import random_cos_to_wx_with_retry


def init_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(func=chaos_func, id='apscheduler_chaos', trigger='interval', minutes=30,
                      replace_existing=True)
    scheduler.add_job(func=random_cos_to_wx_with_retry, id='apscheduler_wx_cos', trigger='interval', minutes=30,
                      replace_existing=True)
    scheduler.add_job(func=check_all_players, id='apscheduler_check_all_players', trigger='interval', minutes=0.5,
                      replace_existing=True)
    scheduler.add_job(func=update_cos_pics_to_redis, id='apscheduler_update_cos_pics_to_redis', trigger='interval',
                      minutes=60 * 12,
                      replace_existing=True)
    scheduler.start()
