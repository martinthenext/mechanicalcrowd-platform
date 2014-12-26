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

    def reject_assignment(self, *args, **kwargs):
        logger.debug("fake reject_assignment: %s %s", args, kwargs)

    def approve_assignment(self, *args, **kwargs):
        logger.debug("fake approve_assignment: %s, %s", args, kwargs)


class HitManager(models.Manager):
    def get_connection(self):
        if DRY_RUN:
            return DryConnection()
        connection = MTurkConnection(
            aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,
            host=HOST)
        logger.info("connection to host %s is established", HOST)
        return connection

    def create_hit(self, task, *rows, reward=None, max_assignments=None):
        logger.info("creating hit for task %s", task.id)
        reward = reward or DEFAULT_REWORD
        logger.info(".. reward: %s", reward)
        max_assignments = max_assignments or DEFAULT_MAX_ASSIGNMENTS
        logger.info(".. max_assignments: %s", max_assignments)

        upper_task = task.wrong_rows_definition
        logger.info(".. upper_task: %s", upper_task)
        lower_task = task.task_definition
        logger.info(".. lower_task: %s", lower_task)
        functions = json.dumps(task.get_functions())
        logger.info(".. functions: %s", functions)
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
        logger.info(".. url: %s", url)

        loggger.info(".. done: %s - %s", hit.HITId, hit.HITTypeId)

        return self.model(
            ident=hit.HITId, task=task, group=hit.HITTypeId,
            reward=reward, max_assignments=max_assignments,
            upper_task=upper_task, lower_task=lower_task,
            functions=functions, url=url, values=values)

    def reject(self, assignment_id):
        logger.info("rejecting assignment: %s", assignment_id)
        connection = self.get_connection()
        connection.reject_assignment(assignment_id)

    def approve(self, assignment_id):
        logger.info("approving assignment: %s", assignment_id)
        connection = self.get_connection()
        connection.approve_assignment(assignment_id)
