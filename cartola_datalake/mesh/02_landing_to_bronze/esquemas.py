# python -m cartola_datalake.mesh.02_landing_to_bronze.esquemas
import json
import os

import pandas as pd

from cartola_datalake.mesh.io import write_if_different
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE, FOLDER_LANDING, SEASON_STR

_log = SetupLogger("02_landing_to_bronze.esquemas")


def main():
    path_esquemas_season = os.path.join(
        os.getcwd(),
        "datalake",
        FOLDER_LANDING,
        f"season-{SEASON_STR}",
        "esquemas",
    )
    list_files = os.listdir(path_esquemas_season)
    _log.info("Reading 'esquemas' folder...")
    df_esquemas = pd.DataFrame()
    for file in list_files:
        file_path = os.path.join(path_esquemas_season, file)
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        df_loop = pd.DataFrame(data)
        df_posicoes = pd.json_normalize(df_loop["posicoes"])
        df_loop = pd.concat([df_loop.drop(columns=["posicoes"]), df_posicoes], axis=1)
        df_loop["file_source"] = os.path.join(
            "datalake",
            FOLDER_LANDING,
            f"season-{SEASON_STR}",
            "esquemas",
            file,
        )
        df_esquemas = pd.concat([df_esquemas, df_loop], ignore_index=True)

    _log.info("Saving 'esquemas.csv'...")

    # Directory to store the file
    esquemas_target_dir = os.path.join(
        os.getcwd(),
        "datalake",
        FOLDER_BRONZE,
        f"season-{SEASON_STR}",
        "esquemas",
    )
    os.makedirs(esquemas_target_dir, exist_ok=True)

    dict_args_esquemas = {
        "df": df_esquemas,
        "filepath": os.path.join(esquemas_target_dir, "esquemas.csv"),
        "sep": ";",
        "decimal": ".",
        "index": False,
    }

    write_if_different(**dict_args_esquemas)


if __name__ == "__main__":
    main()
