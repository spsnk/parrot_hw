from flask.json import JSONEncoder
import decimal


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)


def convert_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return obj
