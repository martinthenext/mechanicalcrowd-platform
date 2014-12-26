import logging
import json

from django.shortcuts import get_object_or_404

from rest_framework import exceptions
from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Hit, Turker, Assignment

from mcrowd.common.exceptions import BadRequest
from mcrowd.task.models import RowDiff

logger = logging.getLogger(__name__)


class QuestionView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_hit(self, hit_id, **kwargs):
        hit = Hit.objects.filter(ident=hit_id, **kwargs)
        if not hit:
            raise exceptions.PermissionDenied(detail="unknown hit_id")
        return hit[0]

    def get_turker(self, worker_id):
        turker, _ = Turker.objects.get_or_create(ident=worker_id)
        return turker

    def get_new_assignment(self, assignment_id, hit, turker):
        allowed, hit = turker.is_allowed_for_hit(hit, assignment_id)
        if not allowed:
            raise exceptions.PermissionDenied(
                detail="this hit is not allowed for turker")
        logger.info("assign hit %s to turker %s", hit.ident,  turker.ident)
        assginment = Assignment.objects.get_or_create(
            ident=assignment_id, hit=hit, turker=turker, done=False,
            approved=None)
        return assignment

    def get_existing_assignment(self, assignment_id, turker, token):
        try:
            assignment = Assignment.objects.get(
                ident=assignment_id, turker=turker,
                token=token, done=False, approved=None)
            return assignment
        except Exception as e:
            logger.exception(e)
            raise exceptions.PermissionDenied(
                detail="uknown assignment %s for turker %s", assignment_id,
                turker.ident)

    def get(self, request):
        hit_id = request.GET.get("hit_id")
        worker_id = request.GET.get("worker_id")
        assignment_id = request.GET.get("assignment_id")
        if not hit_id:
            raise BadRequest(detail="hit_id is required")
        if not worker_id:
            raise BadRequest(detail="worker_id is required")
        if not assignment_id:
            raise BadRequest(detail="assignment_id is requred")
        hit = self.get_hit(hit_id, disabled=False)
        turker = self.get_turker(worker_id)
        assignment = self.get_new_assignment(assignment_id, hit, turker)
        data = {
            "upperTask": hit.upper_task,
            "lowerTask": hit.lower_task,
            "token": assignment.token,
            "table": {
                "headers": hit.task.get_col_names(),
                "rows": hit.get_rows(),
            },
            "functions": hit.get_functions(),
        }
        return Response(data, status=200)

    def post(self, request):
        hit_id = request.DATA.get("mturk", {}).get("hit_id")
        worker_id = request.DATA.get("mturk", {}).get("worker_id")
        assignment_id = request.DATA.get("mturk", {}).get("assignment_id")
        token = request.DATA.get("token")
        rows = request.DATA.get("rows", [])
        if not worker_id:
            raise BadRequest(detail="worker_id is required")
        if not assignment_id:
            raise BadRequest(detail="assignment_id is requred")
        if not token:
            raise BadRequest(detail="token is requred")
        if not rows:
            raise BadRequest(detail="rows is requred")
        turker = self.get_turker(worker_id)
        assignment = self.get_existing_assignment(assignment_id, turker, token)
        hit = assignment.hit

        if hit_id:
            logger.warning(
                "mturk.hit_id = %s is ignored. assignment.hit = %s is used",
                hit_id, assignment.hit.ident)

        if len(hit.get_rows()) != len(rows):
            raise BadRequest(detail="invalid rows count")
        original = hit.get_original_rows()
        diff = []
        for (number, orig), new in zip(original, rows):
            if len(orig) != len(new):
                raise BadRequest(detail="invalid cell count")
            meta = {
                "assignment": assignment.pk,
                "turker": turker.pk,
                "hit": hit.pk
            }
            diff.append(
                RowDiff(task=hit.task, number=number,
                        values=json.dumps(new), meta=json.dumps(meta)))
        RowDiff.objects.bulk_create(diff)
        assignment.done = True
        assignment.approved = True
        assignment.save()
        if hit.enough_assignments():
            hit.disable()
            hit.save()
        return Response(status=200)
