import hashlib
import json


def calculate_dict_checksum(data):
    data_str = json.dumps(data, sort_keys=True)

    checksum = hashlib.sha256(data_str.encode("utf-8")).hexdigest()

    return checksum
