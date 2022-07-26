"""Workflow class for controlling all CLI functions."""

import os
import sys
import time
import subprocess
from typing import List
from cvxopt import matrix
from numpy import save, load

import pandas as pd
from qiskit_ibm_runtime import QiskitRuntimeService

from src.controllers import sync_endpoint
from src.controllers import Completion, Kernel
from src.data import completion_telemetry


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
        width: int = 3,
        layer: int = 1,
        seed1: int = 42,
        seed2: int = 4242,
        matrix_size: List[int] = None,
        backend: str = "ibmq_qasm_simulator",
        shots: int = 1024,
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

        kernel_circuits = Kernel(
            circuit_tpl_id=circuit_tpl_id,
            width=width,
            layer=layer,
            seed_x=seed_x,
            seed_y=seed_y,
            backend=backend,
            shots=shots,
        )

        # Gen template circuit
        kernel_circuits.gen_circuits_tpl()
        # Gen kernel circuits
        kernel_circuits.gen_kernel_circuits()
        # Exec circuits
        return_str = kernel_circuits.exec_circuits()

        return return_str

    @staticmethod
    def completion_flow(
        file_name: str,
        backend: str = "ibmq_qasm_simulator",
        nb_qubits: int = None,
        size_matrix: int = None,
    ) -> [str]:
        """Command for matrix completion.

        Args:
            file_name: name of the kernel to make to completion
            backend: name of the backend
            nb_qubits: number of qubits into the kernel (Optional)
            size_matrix: size [x, y] of the matrix (Optional)

        Return:
            File generate
        """

        res_folder = "../resources/kernel_metadata/" + backend + "/"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        matrix_res = pd.read_feather(
            "{}/{}/".format(current_dir, res_folder) + file_name
        )

        # Size of the matrix check
        if size_matrix is None:
            size_matrix = max(matrix_res["seed_x"].tolist())
        matrix_size = sum(1 + i for i in range(0, size_matrix))
        matrix_data = matrix_res.head(matrix_size)

        # Number of qubits check

        # Init completion object
        matrix_cmpl = Completion(
            matrix_data=matrix_data, size_matrix=size_matrix, nb_qubits=nb_qubits
        )
        if len(matrix_cmpl.error) > 0:
            sys.exit(1)
        else:
            print("Parameters ok.")

        # Create K matrix
        matrix_cmpl.gen_kmatrix()
        # Matrix injection of u
        matrix_cmpl.u_injection()
        # Doing completion
        matrix_cmpl.do_completion()
        # Calc error
        matrix_cmpl.calc_error()

        # Register completed matrix
        file_save = "cmpl_" + file_name
        dir_save = "{}/../resources/cmpl_matrix/{}/".format(current_dir, backend)
        if not os.path.isdir(dir_save):
            os.makedirs(dir_save)

        save(dir_save + file_save, matrix_cmpl.final_cmpl)

        # Gen telemetry
        completion_telemetry(
            size_bn=matrix_cmpl.size_bn,
            size_ln=matrix_cmpl.size_ln,
            over_u=matrix_cmpl.over_u,
            size_np=matrix_cmpl.size_bn + matrix_cmpl.size_ln,
            pourcent_sparcity=matrix_cmpl.sparsity,
            time_cmpl=matrix_cmpl.time_cmpl,
            error_mse=matrix_cmpl.mse,
            error_norm=matrix_cmpl.norm_err,
            comment=matrix_cmpl.comment,
        )

        return str(backend + "/" + file_save + ".npy")

    @staticmethod
    def end2end_flow(
        circuit_tpl_id: [int],
        width: int = 3,
        layer: int = 1,
        seed1: int = 42,
        seed2: int = 4242,
        matrix_size: List[int] = None,
        backend: str = "ibmq_qasm_simulator",
        shots: int = 1024,
    ):
        """Command for end 2 end Workflow.

        Args:
            circuit_tpl_id: list of circuit id to run as template
            width: number of qubits
            layer: number of reps for the tpl
            seed1: seed for x axes
            seed2: seed for y axes
            matrix_size: matrix size for seed coordinate [x, y]
            backend: backend for running circuit
            shots: number of shots for the circuit

        Return:
            Status of the workflow.
        """
        kernel_metadata = Workflow.kernel_flow(
            circuit_tpl_id=circuit_tpl_id,
            width=width,
            layer=layer,
            seed1=seed1,
            seed2=seed2,
            matrix_size=matrix_size,
            backend=backend,
            shots=shots,
        )
        print("Kernel generated : ", kernel_metadata)

        for kernel in kernel_metadata:
            name_backend = kernel.split("/")
            matrix_completed = Workflow.completion_flow(
                file_name=name_backend[1],
                backend=name_backend[0],
                nb_qubits=width,
                size_matrix=matrix_size[0],
            )
            print("Matrix generated : ", matrix_completed)

        return "Workflow end successfully !"

    @staticmethod
    def view_kernel(
        file_name: str,
        backend: str = "ibmq_qasm_simulator",
        resources_path: str = "resources/kernel_metadata",
    ) -> pd.DataFrame:
        """Commands for decode kernel files.

        Args:
            file_name: name of the file to decode in resources/kernel_metadata
            backend: backend of the experiment of the resource file
            resources_path: path of the resources files

        Return:
            Return file_name decode as pandas.Dataframe
        """
        local = "../" + resources_path + "/" + backend
        current_dir = os.path.dirname(os.path.abspath(__file__))

        data_fea = pd.read_feather("{}/{}/".format(current_dir, local) + file_name)

        print(
            "::set-output name={name}::{value}".format(
                name=file_name, value="\n" + str(data_fea)
            )
        )

        return data_fea

    @staticmethod
    def view_telemetry(
        file_name: str = "telemetry_info.csv",
        resources_path: str = "resources/kernel_metadata",
    ) -> pd.DataFrame:
        """Commands for decode telemetry files.

        Args:
            file_name: name of the file to decode in resources/kernel_metadata
            resources_path: path of the resources files

        Return:
            Return file_name decode as pandas.Dataframe
        """
        local = "../" + resources_path
        current_dir = os.path.dirname(os.path.abspath(__file__))

        data_fea = pd.read_feather("{}/{}/".format(current_dir, local) + file_name)

        print(
            "::set-output name={name}::{value}".format(
                name=file_name, value="\n" + str(data_fea)
            )
        )

        return data_fea

    @staticmethod
    def view_matrix(
        file_name: str,
        backend: str = "ibmq_qasm_simulator",
        resources_path: str = "resources/cmpl_matrix",
    ) -> matrix:
        """Commands for decode matrix files.

        Args:
            file_name: name of the file to decode in resources/cmpl_matrix
            backend: backend name
            resources_path: path of the resources files

        Return:
            Return file_name decode as pandas.Dataframe
        """
        local = "../" + resources_path + "/" + backend
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(
            "{}/{}/{}".format(current_dir, local, file_name), "rb"
        ) as file_matrix:
            my_matrix = matrix(load(file_matrix))

        print(
            "::set-output name={name}::{value}".format(
                name=file_name, value="\n" + str(my_matrix)
            )
        )

        return my_matrix

    @staticmethod
    def sync_data(
        sha_folder: str = "resources/shared_folder",
        kernel_metadata_sync: bool = True,
        telemetry_sync: bool = True,
        git_sync: bool = True,
    ) -> str:
        """Commands for sync data to shared folder.

        Args:
            sha_folder: shared folder
            kernel_metadata_sync: sync the kernel metadata True / False
            telemetry_sync: sync the telemetry file True / False
            git_sync: push to git True / False

        Return:
            Ok or error
        """
        local = "../resources/kernel_metadata"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        lockfile = "{}/../{}/.busy".format(current_dir, sha_folder)
        sha_folder = "../" + sha_folder + "/kernel_metadata"

        # check lockfile
        while os.path.isfile(lockfile):
            print("Wait 3 seconds, someone is doing a sync...")
            time.sleep(3)

        with open(lockfile, "w") as lockfile_content:
            lockfile_content.write(
                "Lockfile to avoid multiple sync at the same time..."
            )

        result_str = sync_endpoint(
            current_dir=current_dir,
            local=local,
            sha_folder=sha_folder,
            kernel_metadata_sync=kernel_metadata_sync,
            telemetry_sync=telemetry_sync,
        )

        os.remove(lockfile)

        if git_sync:
            # Try to Git commit / push
            try:
                subprocess.call("git add resources/kernel_metadata/", shell=True)
                subprocess.call('git commit -m "sync resources"', shell=True)
                subprocess.call("git push", shell=True)
                return "sync data done & pushed to GitHub !"
            except Exception as _:  # pylint: disable=broad-except
                return "Don't forget to update the resources file in GitHub"
        else:
            return result_str
