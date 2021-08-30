class RawMessage(object):
    time: int
    self_id: int
    post_type: str
    message_type: str
    sub_type: str
    message_id: int
    group_id: int
    user_id: int
    anonymous: object
    message: object
    raw_message: str


class TextMessage(object):
    at_id: int
    sender_id: int
    text_content: str


class Router(object):
    # bot的qq号码
    manager_id: int

    def __init__(self):
        pass
