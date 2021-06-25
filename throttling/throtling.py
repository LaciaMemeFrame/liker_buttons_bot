from time import time
from collections import defaultdict
from typing import Union

USERS = defaultdict(list)
MESSAGES = 1
SECONDS = 1


async def isFlood(callback: int) -> Union[bool, None]:
    USERS[callback.from_user.id].append(time())
    if len(list(filter(lambda x: time() - int(x) < SECONDS, USERS[callback.from_user.id]))) > MESSAGES:
        return False