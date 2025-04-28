# python -m cartola_datalake.mesh.landing_to_bronze.clubes
import json
import os

import pandas as pd

from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE
from cartola_datalake.mesh.settings import FOLDER_LANDING
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger('landing_to_bronze.clubes')


def main():
    PATH_CLUBES_SEASON = os.path.join(os.getcwd(), 'datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'clubes')
    list_files = os.listdir(PATH_CLUBES_SEASON)
    _log.info("Reading 'clubes' folder...")
    df_clubes_all = pd.DataFrame()
    for file in list_files:
        file_path = os.path.join(PATH_CLUBES_SEASON, file)
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        df_clubes = pd.DataFrame(data).T.reset_index()
        df_clubes.rename(columns={'index': 'clube_id'}, inplace=True)
        df_clubes['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'clubes', file)
        df_clubes_all = pd.concat([df_clubes_all, df_clubes], ignore_index=True)

    _log.info("Saving 'clubes.csv'...")
    os.makedirs(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'clubes'), exist_ok=True)
    df_clubes_all.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'clubes', 'clubes.csv'), sep=';', decimal='.', index=False)
    _log.info('Saved')


if __name__ == '__main__':
    main()
