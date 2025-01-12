import re

from rest_framework.serializers import ValidationError


class YoutubeValidator:
    """Валидатор для проверки, что ссылка принадлежит YouTube."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r"https?://(www\.)?youtube\.com/.*")
        tmp_val = value.get(self.field)
        if not reg.match(tmp_val):
            raise ValidationError("Ссылка должна указывать только на YouTube.")


def youtube_url_validator(value):
    """
    Валидатор для проверки, что ссылка принадлежит YouTube.
    """
    if not re.match(r"https?://(www\.)?youtube\.com/.*", value):
        raise ValidationError("Ссылка должна указывать только на YouTube.")
