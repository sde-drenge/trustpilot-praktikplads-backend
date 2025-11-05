class Roles:
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"
    WORKER = "worker"
    GUEST = "guest"

    choices = (
        (ADMIN, "admin"),
        (STUDENT, "student"),
        (TEACHER, "teacher"),
        (WORKER, "worker"),
        (GUEST, "guest"),
    )

    accessToRemoveReviews = [ADMIN]
    accessToCreateReviews = [STUDENT]
    accessToCreateSchools = [ADMIN]