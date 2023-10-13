import mouse
from time import time, sleep


events = []
mouse.hook(events.append)
mouse._listener.queue.join()


def init():
    result = False
    for event in events:
        if isinstance(event, mouse._mouse_event.ButtonEvent):
            if event.button == 'left':
                if event.event_type == 'up':
                    result = False
                else:
                    result = True
    return result


while True:
    pressed = init()
    if pressed:
        singlepress = True
        stime = time()
        while pressed:
            for event in events:
                if isinstance(event, mouse._mouse_event.ButtonEvent):
                    pressed = False if (event.event_type == 'up') else True
                if (time() - stime) < 1:
                    if singlepress:
                        print('tiklama')
                        singlepress = False
                else:
                    print('basili\ntutma')
    events.clear()
    sleep(0.01)
