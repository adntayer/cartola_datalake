import gzip
import json

from cartola_datalake.mesh.logger import SetupLogger

_log = SetupLogger('io')


def save_dict_to_file(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        _log.debug(f'save_dict_to_file | data successfully saved to {file_path}')
    except Exception as e:
        _log.error(f'save_dict_to_file | an error occurred while saving the file: {e}')
        raise e


def save_dict_to_file_compress(file_path, data):
    try:
        assert file_path.endswith('json.gz')
        with gzip.open(file_path, 'wt', encoding='utf-8') as f:
            json.dump(data, f)
        _log.debug(f'save_dict_to_file_compress | data successfully saved to {file_path}')
    except Exception as e:
        _log.error(f'save_dict_to_file_compress | an error occurred while saving the file: {e}')
        raise e


def load_dict_from_file(file_path):
    try:
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        _log.debug(f'load_dict_from_file | data successfully loaded to {file_path}')
        return data
    except Exception as e:
        _log.error(f'load_dict_from_file | an error occurred while loading the file: {e}')
        raise e


def load_dict_from_file_compress(file_path):
    try:
        assert file_path.endswith('json.gz')
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            data = json.load(f)
        _log.debug(f'load_dict_from_file_compress | data successfully loaded to {file_path}')
        return data
    except Exception as e:
        _log.error(f'load_dict_from_file_compress | an error occurred while loading the file: {e}')
        raise e
