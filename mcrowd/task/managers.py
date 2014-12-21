from django.db import models


class RowDiffManager(models.Manager):
    def get_last(self, task):
        query = """
        select
            last(id) as id,
            last(values) as values,
            last(meta) as meta,
            last(task_id) as task_id,
            number
        from task_rowdiff
        where task_id = %s
        group by number;
        """
        return self.model.objects.raw(query, [task.id])
