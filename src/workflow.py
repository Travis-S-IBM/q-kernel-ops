"""Workflow class for controlling all CLI functions."""

import os
import sys
import shutil
import subprocess
from typing import List

import pandas as pd
from qiskit_ibm_runtime import QiskitRuntimeService

from src.controllers import kernel_endpoint


class Workflow:
    """Worflow class.
    Entrypoint for all CLI commands.

    Each public method of this class is CLI command
    and arguments for method are options/flags for this command.

    Ex: `python workflow.py kernel_flow --circuit_tpl_id=[2,5]`
    """

    def __init__(self):
        pass

    @staticmethod
    def authentication(
        channel: str, token: str, instance="ibm-q/open/main", overwrite=False
    ) -> None:
        """Commands for authentication.

        Args:
            channel:
                if you have a Cloud account : "ibm_cloud",
                if you have an Quantum account "ibm_quantum"
            token: your IBM Cloud/Quantum token
            instance: group path for computer access
            overwrite: set True if you want to overwrite your actual token

        Return:
            Register the session in disk space
        """
        QiskitRuntimeService.save_account(
            channel=channel, token=token, instance=instance, overwrite=overwrite
        )

    @staticmethod
    def kernel_flow(
        circuit_tpl_id: [int],
        width: int = 4,
        layer: int = 1,
        seed1: int = 42,
        seed2: int = 4242,
        matrix_size: List[int] = None,
        backend: str = "ibmq_qasm_simulator",
        shots: int = 1024,
        verbose: bool = False,
    ) -> [str]:
        """Command for kernel matrix generation.

        Args:
            circuit_tpl_id: list of circuit id to run as template
            width: number of qubits
            layer: number of reps for the tpl
            seed1: seed for x axes
            seed2: seed for y axes
            matrix_size: matrix size for seed coordinate [x, y]
            backend: backend for running circuit
            shots: number of shots for the circuit
            verbose: print all kind of information

        Returns:
            Array of data files name
        """
        seed_x = []
        seed_y = []

        if matrix_size is not None:
            if matrix_size[0] != matrix_size[1]:
                print(
                    """
                The coordinate have to be square.
                Ex. [2,2] or [5,5]
                """
                )
                sys.exit(1)
            for x_axe in range(matrix_size[0] + 1):
                for y_axe in range(x_axe + 1):
                    seed_x.append(x_axe)
                    seed_y.append(y_axe)
        else:
            seed_x.append(seed1)
            seed_y.append(seed2)

        return kernel_endpoint(
            circuit_tpl_id=circuit_tpl_id,
            width=width,
            layer=layer,
            seed_x=seed_x,
            seed_y=seed_y,
            backend=backend,
            shots=shots,
            verbose=verbose,
        )

    @staticmethod
    def view_kernel(
        file_name: str, backend: str = "ibmq_qasm_simulator"
    ) -> pd.DataFrame:
        """Commands for decode kernel files.

        Args:
            file_name: name of the file to decode in resources/kernel_metadata
            backend: backend of the experiment of the resource file

        Return:
            Return file_name decode as pandas.Dataframe
        """
        local = "../resources/kernel_metadata/" + backend
        current_dir = os.path.dirname(os.path.abspath(__file__))

        data_fea = pd.read_feather("{}/{}/".format(current_dir, local) + file_name)

        print(
            "::set-output name={name}::{value}".format(
                name=file_name, value="\n" + str(data_fea)
            )
        )

        return data_fea

    @staticmethod
    def view_telemetry(file_name: str = "telemetry_info.csv") -> pd.DataFrame:
        """Commands for decode telemetry files.

        Args:
            file_name: name of the file to decode in resources/kernel_metadata

        Return:
            Return file_name decode as pandas.Dataframe
        """
        local = "../resources/kernel_metadata/"
        current_dir = os.path.dirname(os.path.abspath(__file__))

        data_fea = pd.read_feather("{}/{}/".format(current_dir, local) + file_name)

        print(
            "::set-output name={name}::{value}".format(
                name=file_name, value="\n" + str(data_fea)
            )
        )

        return data_fea

    @staticmethod
    def sync_data(sha_folder: str = "../resources/shared_folder/") -> str:
        """Commands for sync data to shared folder.

        Args:
            sha_folder: shared folder

        Return:
            Ok or error
        """
        local = "../resources/kernel_metadata/"
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Check metadata file
        for folder in os.listdir("{}/{}/".format(current_dir, local)):
            if os.path.isdir("{}/{}/{}".format(current_dir, local, folder)):
                for meta_file in os.listdir(
                    "{}/{}/{}".format(current_dir, local, folder)
                ):
                    local_file = "{}/{}/{}/{}".format(
                        current_dir, local, folder, meta_file
                    )
                    sha_file = "{}/{}/{}/{}".format(
                        current_dir, sha_folder, folder, meta_file
                    )
                    if os.path.isfile(sha_file):
                        if os.path.getsize(local_file) > sys.getsizeof(sha_file):
                            shutil.copyfile(local_file, sha_file)
                        else:
                            shutil.copyfile(sha_file, local_file)
                    elif os.path.isdir(sha_folder):
                        shutil.copyfile(local_file, sha_file)
                    else:
                        os.mkdir(sha_folder)
                        shutil.copyfile(local_file, sha_file)

        # Check & merge telemetry
        temp_tele_path = current_dir + local + "telemetry_info.csv"
        local_tele_path = current_dir + local + "shared_telemetry_info.csv"
        sha_tele_path = current_dir + sha_folder + "shared_telemetry_info.csv"
        temp_tele = pd.read_feather(temp_tele_path)
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

        # Try to Git commit / push
        try:
            subprocess.check_call("git add resources/", shell=True)
            subprocess.check_call('git commit -m "sync resources"', shell=True)
            subprocess.check_call("git push origin master", shell=True)
        except Exception as _:  # pylint: disable=broad-except
            return "Don't forget to update the resources file in GitHub"

        return "sync data done & pushed to GitHub !"
