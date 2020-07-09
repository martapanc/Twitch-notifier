from datetime import datetime, timedelta

notification_queue = []


def get_queue():
    return notification_queue


def add_to_queue(notification_info):
    notification_queue.append(notification_info)


def clear_older_queue():
    one_hour_ago = datetime.utcnow() - timedelta(minutes=60)
    for notif in notification_queue:
        if notif[1] < one_hour_ago:
            notification_queue.pop(notif)


def is_already_in_queue(channel):
    for notif in notification_queue:
        if notif[0] == channel:
            return True
    return False
