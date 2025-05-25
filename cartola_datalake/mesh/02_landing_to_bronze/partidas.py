# python -m cartola_datalake.mesh.02_landing_to_bronze.partidas
import json
import os

import pandas as pd

from cartola_datalake.mesh.io import write_if_different
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE, FOLDER_LANDING, SEASON_STR

_log = SetupLogger("02_landing_to_bronze.partidas")


def main():
    path_partidas_season = os.path.join(
        os.getcwd(),
        "datalake",
        FOLDER_LANDING,
        f"season-{SEASON_STR}",
        "partidas",
    )
    _log.info("Reading 'partidas' folder...")
    df_all = pd.DataFrame()
    for root, dirs, files in os.walk(path_partidas_season):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
            for dict_partida in data["partidas"]:
                df_loop = pd.json_normalize(dict_partida)
                df_loop["rodada"] = file.replace("partidas_rodada_", "").replace(
                    ".json",
                    "",
                )
                df_loop["file_source"] = os.path.join(
                    "datalake",
                    FOLDER_LANDING,
                    f"season-{SEASON_STR}",
                    "partidas",
                    file,
                )
                df_all = pd.concat([df_all, df_loop], ignore_index=True)

    _log.info("All partidas got")

    _log.info("Reading 'clubes'...")
    df_clubes = pd.DataFrame(data["clubes"]).T.reset_index()
    df_clubes.rename(columns={"index": "clube_id"}, inplace=True)
    df_clubes["file_source"] = os.path.join(
        "datalake",
        FOLDER_LANDING,
        f"season-{SEASON_STR}",
        "partidas",
        file,
    )

    _log.info("Saving 'partidas.csv' and 'clubes.csv'...")

    # Directory to store the files
    partidas_target_dir = os.path.join(
        os.getcwd(),
        "datalake",
        FOLDER_BRONZE,
        f"season-{SEASON_STR}",
        "partidas",
    )
    os.makedirs(partidas_target_dir, exist_ok=True)

    dict_args_partidas = {
        "df": df_all,
        "filepath": os.path.join(partidas_target_dir, "partidas.csv"),
        "sep": ";",
        "decimal": ".",
        "index": False,
    }

    dict_args_clubes_partidas = {
        "df": df_clubes,
        "filepath": os.path.join(partidas_target_dir, "clubes.csv"),
        "sep": ";",
        "decimal": ".",
        "index": False,
    }

    write_if_different(**dict_args_partidas)
    write_if_different(**dict_args_clubes_partidas)


if __name__ == "__main__":
    main()
