import os

from django.conf import settings as S


if hasattr(S, "MTURK"):
    MTURK = S.MTURK
else:
    MTURK = {}

HOST = MTURK.get("HOST", "workersandbox.mturk.com")

ACCESS_KEY = MTURK.get("ACCESS_KEY")
SECRET_KEY = MTURK.get("SECRET_KEY")

if not (ACCESS_KEY and SECRET_KEY):
    raise Exception("MTURK.ACCESS_KEY and MTURK.SECRET_KEY are required")

DEFAULT_REWORD = MTURK.get("DEFAULT_REWORD", 0.30)  # $
DEFAULT_MAX_ASSIGNMENTS = MTURK.get("DEFAULT_MAX_ASSIGNMENTS", 3)

QUESTION_URL = MTURK.get("QUESTION_URL", "https://platform.comnsense.io/mturk")
QUESTION_HEIGHT = MTURK.get("QUESTION_HEIGHT", 500)
QUESTION_TITLE = MTURK.get("QUESTION_TITLE", "Table review")
QUESTION_DESC = MTURK.get("QUESTION_DESC",
                          "Answer about correctness of table values")
QUESTION_KEYWORDS = MTURK.get("QUESTION_KEYWORDS",
                              "table, English, search")
QUESTION_LIFETIME = MTURK.get("QUESTION_LIFETIME", 3 * 24 * 60 * 60)
QUESTION_ANNOTATION = MTURK.get("QUESTION_ANNOTATION", "Table review")

# do all but connect to mturk
DRY_RUN = MTURK.get("DRY_RUN", False)
