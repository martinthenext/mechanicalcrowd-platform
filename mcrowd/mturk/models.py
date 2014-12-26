import json
import logging

from django.db import models
from django.db.models.signals import post_save, pre_save

from .managers import HitManager
from .hooks import create_token, finish_assignment, check_constraint

from mcrowd.task.models import Task

logger = logging.getLogger(__name__)


class Hit(models.Model):
    task = models.ForeignKey(Task, null=False, related_name="hits")
    ident = models.CharField(
        max_length=40, null=False, blank=False, db_index=True, unique=True)
    group = models.CharField(
        max_length=40, null=False, blank=False, db_index=True)
    values = models.TextField(blank=False, null=False)
    upper_task = models.TextField(blank=True, null=False, default="")
    lower_task = models.TextField(blank=True, null=False, default="")
    functions = models.TextField(blank=False, null=False)
    url = models.URLField(blank=False, null=False)
    reward = models.DecimalField(
        blank=False, null=False, max_digits=3, decimal_places=2)  # max 9.99$
    max_assignments = models.IntegerField(blank=False, null=False)
    disabled = models.BooleanField(blank=False, null=False, default=False)

    def get_rows(self):
        values = json.loads(self.values)
        return list(map(lambda x: x[1], values))

    def get_original_rows(self):
        return json.loads(self.values)

    def get_functions(self):
        return json.loads(self.functions)

    def enough_assignments(self):
        if len(self.assignments.filter(done=True)) >= self.max_assignments:
            return True
        return False

    def disable(self):
        connection = Hit.objects.get_connection()
        connection.disable_hit(self.ident)
        self.disabled = True

    objects = HitManager()


class Turker(models.Model):
    ident = models.CharField(
        max_length=40, null=False, blank=False, db_index=True, unique=True)

    def is_allowed_for_hit(self, hit, assignment_id):
        same = self.assignments.filter(
            ident=assignment_id, hit=hit, done=False, approved=None)
        if same:
            logger.info("seems turker %s reload page with hit %s",
                        self.ident, hit.ident)
            return (True, hit)
        task = hit.task
        done = task.hits.assignments.filter(turker=self, done=True).all()
        if len(done) >= task.hits_per_user:  # too many hits
            logger.info("turker %s done all available hits in task %s",
                        self.ident, task.id)
            return (False, _)
        if bool(list(filter(lambda x: x.hit == hit, done))):
            # this hit already done
            logger.info("turker %s already done hit %s", self.ident, hit.ident)
            return (False, _)
        unfinished = task.hits.assignments.filter(
            turker=self, done=False, approved=None).all()
        if len(unfinished) == 0:  # no unfinished
            logger.info("turker %s has no unfinished assignments", self.ident)
            return (True, hit)
        else:
            in_unfinished = False
            # new assignment but unfinished hits
            for assignment in unfinished:
                if assignment.hit == hit:
                    in_unfinished = True
                assignment.approved = False
                assignment.save()
            if in_unfinished:
                logger.info("turker %s wants new assginment to hit %s",
                            self.ident, hit.ident)
                # new assignment for same hit
                return (True, hit)
            else:
                logger.info("turker %s wants new hit %s but has unfinished",
                            self.ident, hit.ident)
                logger.info("he should finish it: %s", unfinished[0].hit)
                # new assignment for new hit but unfinished
                return (True, unfinished[0].hit)


class Assignment(models.Model):
    ident = models.CharField(
        max_length=40, null=False, blank=False, unique=True, db_index=True)
    hit = models.ForeignKey(Hit, related_name="assignments", null=False)
    turker = models.ForeignKey(Turker, related_name="assignments", null=False)
    token = models.TextField(blank=False, null=False)
    done = models.BooleanField(blank=False, null=False, default=False)
    approved = models.NullBooleanField(blank=False, null=True, default=None)

    def reject(self):
        Hit.objects.reject(self.ident)

    def approve(self):
        Hit.objects.approve(self.ident)

    class Meta:
        unique_together = (("ident", "turker", "token"),)


pre_save.connect(create_token, Assignment)
pre_save.connect(finish_assignment, Assignment)
pre_save.connect(check_constraint, Assignment)
