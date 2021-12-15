import decimal


def convert_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return obj
