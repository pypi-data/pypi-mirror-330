import json
from ciocore import conductor_submit
from . import ConductorPayload


def submit_payload(payload: ConductorPayload):
    data = payload.as_dict()
    submission = conductor_submit.Submit(data)
    response, response_code = submission.main()
    print(response_code)
    print(json.dumps(response))
