import json
import random

from internal.utils.json_reader import json_reader

zjw_audios = json_reader("static/audio_zjw.json")


def random_audio_zjw():
    rd = random.randint(0, len(zjw_audios) - 1)
    url = zjw_audios[rd]
    return json.dumps({"reply": "[CQ:record,file={},url={}]".format(url, url)})
