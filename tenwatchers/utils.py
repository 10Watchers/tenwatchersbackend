from flask import current_app
from functools import wraps
import json


class ModelJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)


def json_response(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        result = fn(*args, **kwargs)
        if isinstance(result, current_app.response_class):
            return result
        if isinstance(result, (list, tuple)):
            result = {'items': result}
        data = json.dumps(result, cls=ModelJSONEncoder)
        return current_app.response_class(data, mimetype='application/json')
    return wrapped
