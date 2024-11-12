from pygame import USEREVENT
from pygame.event import Event

NAVIGATION_EVENT = USEREVENT + 1

# BRUH
def NavigationEvent(to: str, **kwargs):
    return Event(NAVIGATION_EVENT, to=to, **kwargs)