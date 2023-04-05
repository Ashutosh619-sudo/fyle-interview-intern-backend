from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment


from .schema import AssignmentSchema, AssignmentGradeSchema


teacher_assignment_resources = Blueprint("teacher_assignment_resources",__name__)

@teacher_assignment_resources.route("/assignments",methods=['GET'],strict_slashes=False)
@decorators.auth_principal
def list_all_submitted_assignments(p):
    assignments = Assignment.get_assignments_submitted_to_teacher(p.teacher_id)
    assignments_dump = AssignmentSchema().dump(assignments,many=True)
    return APIResponse.respond(data=assignments_dump)

@teacher_assignment_resources.route("/assignments/grade", methods=["POST"], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):

    assignment_grade = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.grade_assignment(
        _id=assignment_grade.id,
        grade = assignment_grade.grade,
        principal=p
    )

    db.session.commit()
    assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=assignment_dump)

