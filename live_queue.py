
live_queue = []


def get_queue():
    return live_queue


def add_to_queue(live_channel):
    live_queue.append(live_channel)


def remove_from_queue(channel):
    if channel in live_queue:
        live_queue.remove(channel)


def is_in_queue(channel):
    return channel in live_queue
