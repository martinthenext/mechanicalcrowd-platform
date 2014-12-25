import json
import logging
import random

from django.db import models

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price

from .settings import DEFAULT_REWORD, DEFAULT_MAX_ASSIGNMENTS
from .settings import HOST, ACCESS_KEY, SECRET_KEY, URLHOST
from .settings import QUESTION_KEYWORDS, QUESTION_LIFETIME
from .settings import QUESTION_TITLE, QUESTION_DESC, QUESTION_ANNOTATION
from .settings import QUESTION_URL, QUESTION_HEIGHT
from .settings import DRY_RUN

logger = logging.getLogger(__name__)


class DryConnection:
    class Hit:
        def __init__(self):
            self.HITId = str(random.randint(0, 1000000))
            self.HITTypeId = str(random.randint(0, 1000000))

    def create_hit(self, **kwargs):
        logger.debug("fake create_hit: %s", kwargs)
        return [DryConnection.Hit()]

    def disable_hit(self, *args, **kwargs):
        logger.debug("fake disable_hit: %s %s", args, kwargs)


class HitManager(models.Manager):
    def get_connection(self):
        if DRY_RUN:
            return DryConnection()
        connection = MTurkConnection(
            aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,
            host=HOST)
        return connection

    def create_hit(self, task, *rows, reward=None, max_assignments=None):
        reward = reward or DEFAULT_REWORD
        max_assignments = max_assignments or DEFAULT_MAX_ASSIGNMENTS

        upper_task = task.wrong_rows_definition
        lower_task = task.task_definition
        functions = json.dumps(task.get_functions())
        values = []
        for row in rows:
            values.append([row.number, row.get_values()])
        values = json.dumps(values)

        connection = self.get_connection()
        question = ExternalQuestion(QUESTION_URL, QUESTION_HEIGHT)
        result = connection.create_hit(
            question=question,
            title=QUESTION_TITLE,
            description=QUESTION_DESC,
            reward=Price(reward),
            keywords=QUESTION_KEYWORDS,
            max_assignments=max_assignments,
            lifetime=QUESTION_LIFETIME,
            annotation=QUESTION_ANNOTATION)
        hit = result[0]

        url = "https://{}/mturk/preview?groupId={}".format(
            URLHOST, hit.HITTypeId)

        return self.model(
            ident=hit.HITId, task=task,
            reward=reward, max_assignments=max_assignments,
            upper_task=upper_task, lower_task=lower_task,
            functions=functions, url=url, values=values)
