# python -m cartola_datalake.mesh.02_landing_to_bronze.clubes
import json
import os

import pandas as pd

from cartola_datalake.mesh.io import write_if_different
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE, FOLDER_LANDING, SEASON_STR

_log = SetupLogger("02_landing_to_bronze.clubes")


def main():
    path_clubes_season = os.path.join(
        os.getcwd(),
        "datalake",
        FOLDER_LANDING,
        f"season-{SEASON_STR}",
        "clubes",
    )
    list_files = os.listdir(path_clubes_season)
    _log.info("Reading 'clubes' folder...")
    df_clubes_all = pd.DataFrame()
    for file in list_files:
        file_path = os.path.join(path_clubes_season, file)
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        df_clubes = pd.DataFrame(data).T.reset_index()
        df_clubes.rename(columns={"index": "clube_id"}, inplace=True)
        df_clubes["file_source"] = os.path.join(
            "datalake",
            FOLDER_LANDING,
            f"season-{SEASON_STR}",
            "clubes",
            file,
        )
        df_clubes_all = pd.concat([df_clubes_all, df_clubes], ignore_index=True)

    _log.info("Saving 'clubes.csv'...")

    # Directory to store the file
    clubes_target_dir = os.path.join(
        os.getcwd(),
        "datalake",
        FOLDER_BRONZE,
        f"season-{SEASON_STR}",
        "clubes",
    )
    os.makedirs(clubes_target_dir, exist_ok=True)

    dict_args_clubes_all = {
        "df": df_clubes_all,
        "filepath": os.path.join(clubes_target_dir, "clubes.csv"),
        "sep": ";",
        "decimal": ".",
        "index": False,
    }

    write_if_different(**dict_args_clubes_all)


if __name__ == "__main__":
    main()
