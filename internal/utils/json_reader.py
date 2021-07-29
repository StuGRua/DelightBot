import json
from internal.utils.log import LOGGER


def json_reader(filename: str):
    with open(filename,"r") as fi:
        dict_data = json.load(fi)
    return dict_data


def json_writer(filename: str, _data):
    try:
        with open(filename, "w") as fi:
            json.dump(_data, fi, indent=4)
        return filename
    except Exception as e:
        LOGGER.error("Error in writing json")
        LOGGER.error(str(e))
    finally:
        pass
