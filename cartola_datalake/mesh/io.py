import gzip
import hashlib
import json
import os
from io import BytesIO

from cartola_datalake.mesh.logger import SetupLogger

_log = SetupLogger("io")


def save_dict_to_file(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        _log.debug(f"save_dict_to_file | data successfully saved to {file_path}")
    except Exception as e:
        _log.error(f"save_dict_to_file | an error occurred while saving the file: {e}")
        raise e


def save_dict_to_file_compress(file_path, data):
    try:
        assert file_path.endswith("json.gz")
        with gzip.open(file_path, "wt", encoding="utf-8") as f:
            json.dump(data, f)
        _log.debug(
            f"save_dict_to_file_compress | data successfully saved to {file_path}",
        )
    except Exception as e:
        _log.error(
            f"save_dict_to_file_compress | an error occurred while saving the file: {e}",
        )
        raise e


def load_dict_from_file(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        _log.debug(f"load_dict_from_file | data successfully loaded to {file_path}")
        return data
    except Exception as e:
        _log.error(
            f"load_dict_from_file | an error occurred while loading the file: {e}",
        )
        raise e


def load_dict_from_file_compress(file_path):
    try:
        assert file_path.endswith("json.gz")
        with gzip.open(file_path, "rt", encoding="utf-8") as f:
            data = json.load(f)
        _log.debug(
            f"load_dict_from_file_compress | data successfully loaded to {file_path}",
        )
        return data
    except Exception as e:
        _log.error(
            f"load_dict_from_file_compress | an error occurred while loading the file: {e}",
        )
        raise e


def hash_file_bytes(file_bytes):
    return hashlib.md5(file_bytes).hexdigest()


def hash_existing_file(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def write_if_different(df, filepath, **to_csv_kwargs):
    buffer = BytesIO()
    df.to_csv(buffer, **to_csv_kwargs)
    new_bytes = buffer.getvalue()
    new_hash = hash_file_bytes(new_bytes)
    old_hash = hash_existing_file(filepath)

    _log.info(
        f"write_if_different | {os.path.basename(filepath)} | New hash: {new_hash}",
    )
    if old_hash:
        _log.info(
            f"write_if_different | {os.path.basename(filepath)} | Old hash: {old_hash}",
        )
    else:
        _log.info(
            f"write_if_different | {os.path.basename(filepath)} | Old file doesn't exist, so no previous hash to compare.",
        )

    if new_hash != old_hash or not old_hash:
        if os.path.exists(filepath):
            os.remove(filepath)
            _log.info(
                f"write_if_different | {os.path.basename(filepath)} | Deleted old file: {filepath}",
            )

        df.to_csv(filepath, **to_csv_kwargs)
        _log.info(
            f"write_if_different | {os.path.basename(filepath)} | Created updated file: {filepath}",
        )
    else:
        _log.info(
            f"write_if_different | {os.path.basename(filepath)} | No changes in file: {filepath}",
        )
