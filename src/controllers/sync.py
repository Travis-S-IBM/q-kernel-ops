"""
#############################################
#
# sync.py
#
# function for sync programs
#
#
#############################################
"""

import os
import shutil
import pandas as pd


def kernel_sync(current_dir: str, local: str, sha_folder: str) -> None:
    """Check and merge telemetry.

    Args:
        current_dir: current dir from cli gen
        local: local resources folder
        sha_folder: sha_folder: shared folder

    Return:
        Nothing
    """
    temp_tele_path = "{}/{}/{}".format(current_dir, local, "telemetry_info.csv")
    local_tele_path = "{}/{}/{}".format(current_dir, local, "shared_telemetry_info.csv")
    sha_tele_path = "{}/{}/{}".format(
        current_dir, sha_folder, "shared_telemetry_info.csv"
    )
    temp_tele = pd.read_feather(temp_tele_path)

    if not os.path.isfile(sha_tele_path) and os.path.isfile(local_tele_path):
        shutil.copyfile(local_tele_path, sha_tele_path)
    elif not os.path.isfile(local_tele_path):
        shutil.copyfile(temp_tele_path, sha_tele_path)
        shutil.copyfile(sha_tele_path, local_tele_path)
    else:
        sha_tele = pd.read_feather(sha_tele_path)
        for index, jobid in enumerate(temp_tele["job_id"].tolist()):
            if jobid in sha_tele["job_id"].tolist():
                temp_tele = temp_tele.drop(labels=index, axis=0)
                temp_tele.reset_index(drop=True, inplace=True)
        if not temp_tele.empty:
            final_tele = pd.concat([temp_tele, sha_tele], ignore_index=True)
            final_tele.reset_index(drop=True, inplace=True)

            final_tele.to_feather(sha_tele_path)
            final_tele.to_feather(local_tele_path)
    os.remove(temp_tele_path)


def telemetry_info_sync(current_dir: str, local: str, sha_folder: str) -> None:
    """Check metadata file function.

    Args:
        current_dir: current dir from cli gen
        local: local resources folder
        sha_folder: sha_folder: shared folder

    Return:
        Nothing
    """
    for folder in os.listdir("{}/{}/".format(current_dir, local)):
        if os.path.isdir("{}/{}/{}".format(current_dir, local, folder)):
            for meta_file in os.listdir("{}/{}/{}".format(current_dir, local, folder)):
                local_file = "{}/{}/{}/{}".format(current_dir, local, folder, meta_file)
                sha_file = "{}/{}/{}/{}".format(
                    current_dir, sha_folder, folder, meta_file
                )
                if os.path.isfile(sha_file):
                    if os.path.getsize(local_file) > os.path.getsize(sha_file):
                        shutil.copyfile(local_file, sha_file)
                    else:
                        shutil.copyfile(sha_file, local_file)
                elif os.path.isdir("{}/{}/{}".format(current_dir, sha_folder, folder)):
                    shutil.copyfile(local_file, sha_file)
                else:
                    os.mkdir("{}/{}/{}".format(current_dir, sha_folder, folder))
                    shutil.copyfile(local_file, sha_file)


def sync_endpoint(
    current_dir: str,
    local: str,
    sha_folder: str,
    kernel_metadata_sync: bool = True,
    telemetry_sync: bool = True,
) -> str:
    """Commands for sync data to shared folder.
    Args:
        current_dir: current dir from cli gen
        local: local resources folder
        sha_folder: shared folder
        kernel_metadata_sync: sync the kernel metadata True / False
        telemetry_sync: sync the telemetry file True / False

    Return:
        Ok or error
    """
    try:
        if kernel_metadata_sync:
            kernel_sync(current_dir, local, sha_folder)
        if telemetry_sync:
            telemetry_info_sync(current_dir, local, sha_folder)
        return "sync data done !"

    except Exception as error_sync:  # pylint: disable=broad-except
        print("Error : ", error_sync)
        return "An error occurred, lockfile unlock."
