from django.db import models


class StatusChoices(models.IntegerChoices):
    SENT = 1, "sent"
    ACCEPTED = 2, "accepted"
    REJECTED = 3, "rejected"
