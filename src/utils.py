# from flask import json
import json
from decimal import Decimal
from datetime import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, datetime):
            return str(o).split(".")[0]
        return super(DecimalEncoder, self).default(o)
