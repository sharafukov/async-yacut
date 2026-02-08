import random
from yacut.constants import ALLOWED_CHARS, SHORT_ID_LENGTH
from yacut.models import URLMap


def get_unique_short_id():
    while True:
        short_id = ''.join(
            random.choice(ALLOWED_CHARS) for _ in range(SHORT_ID_LENGTH)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
