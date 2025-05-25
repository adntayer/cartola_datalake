import hashlib
import json


def calculate_dict_checksum(data):
    data_str = json.dumps(data, sort_keys=True)

    return hashlib.sha256(data_str.encode("utf-8")).hexdigest()
