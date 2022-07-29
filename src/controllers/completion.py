"""
#############################################
#
# completion.py
#
# object for completion programs
#
#
#############################################
"""
from time import time
from copy import copy
from cvxopt import matrix, sparse
from statsmodels.stats.correlation_tools import corr_clipped
import chompack as cp
import numpy as np
import pandas as pd


class Completion:
    """Completion class.
    Everything about completion object.
    """

    def __init__(
        self,
        matrix_data: pd.DataFrame,
        nb_qubits: int,
        size_matrix: int,
        overlaps: float = 1,
    ):
        """Completion init.

        Args:
            matrix_data: the whole matrix fully complete
            nb_qubits: number of qubits used to generated the data
            size_matrix: [x, y] of the matrix
            overlaps: customize the overlaps
        """
        # Gen matrix data parameters
        self.matrix_data = matrix_data
        self.nb_qubits = nb_qubits
        self.size_matrix = size_matrix
        self.list_seedx = self.matrix_data["seed_x"].tolist()
        self.list_seedy = self.matrix_data["seed_y"].tolist()
        self.list_result = self.matrix_data["fidelity"].tolist()

        # Temp parameters
        self.error = []
        self.full_matrix = None
        self.matrix_status = ""
        self.np_matrix = None
        self.ku_matrix = None
        self.sparsity = 0
        self.final_cmpl = None
        self.mse = 0
        self.norm_err = 0
        self.time_cmpl = 0
        self.comment = ""

        # Gen N and n parameters
        self.size_bn = (
            round(self.size_matrix * 0.7)
            if round(self.size_matrix * 0.7) > 4**self.nb_qubits
            else 4**self.nb_qubits + 1
        )
        self.size_ln = self.size_matrix - self.size_bn
        check_size = sum(1 + i for i in range(0, self.size_ln + self.size_bn))
        self.error.append(
            None if check_size <= len(self.list_result) else "Error in size of N/n"
        )

        # Gen rank/u parameters
        self.size_maxu = self.size_ln + self.size_bn - 1
        self.rank = 4**self.nb_qubits
        self.over_u = round(overlaps * self.rank)
        if self.over_u >= self.size_matrix:
            self.over_u = self.size_maxu

        check_size = self.over_u + self.size_ln
        self.error.append(
            None
            if check_size < self.size_matrix
            else "The kernel matrix is not big enough"
        )
        self.error.append(
            None
            if self.over_u < self.size_bn
            else "The kernel matrix is not big enough"
        )

        # Check error
        for error_mes in self.error:
            if error_mes is not None:
                print(str(error_mes) + "\n")
        self.error = [val for val in self.error if val]

    @staticmethod
    def is_semi_pos_def(matrix_tocheck) -> bool:
        """PSD matrix check by eigvals.

        Args:
            matrix_tocheck: full matrix object

        Return:
            True/False
        """
        return np.all(np.linalg.eigvals(matrix_tocheck) >= 0)

    @staticmethod
    def is_semi_pos_def_eigsh(matrix_tocheck, epsilon=1e-10) -> bool:
        """PSD matrix check by eigvalsh.

        Args:
            matrix_tocheck: full matrix object
            epsilon: limit to eigvalsh

        Return:
            True/False
        """
        return np.all(np.linalg.eigvalsh(matrix_tocheck) >= -epsilon)

    def gen_kmatrix(self):
        """Gen full and sparce matrices."""
        matrix_sub = [float(0)] * self.size_matrix
        self.full_matrix = [matrix_sub] * self.size_matrix

        self.full_matrix = matrix(self.full_matrix)

        for row_i, col_i, fidelity_v in zip(
            self.list_seedx, self.list_seedy, self.list_result
        ):
            self.full_matrix[col_i, row_i] = fidelity_v
            self.full_matrix[row_i, col_i] = fidelity_v

        if self.is_semi_pos_def(matrix(self.full_matrix)) or self.is_semi_pos_def_eigsh(
            matrix(self.full_matrix)
        ):
            self.matrix_status = "is PSD naturally !"
        else:
            self.full_matrix = sparse(
                matrix(corr_clipped(np.array(matrix(self.full_matrix))))
            )
            self.matrix_status = "is nearest PSD !"

        self.np_matrix = copy(self.full_matrix)

        for row_i in range(self.size_matrix):
            for col_i in range(self.size_matrix):
                if row_i > self.size_bn - 1 >= col_i:
                    self.np_matrix[row_i, col_i] = 0
                if col_i > self.size_bn - 1 >= row_i:
                    self.np_matrix[row_i, col_i] = 0

        self.np_matrix = sparse([self.np_matrix])

    def u_injection(self):
        """Injection of u to gen Ku matrix."""
        self.ku_matrix = copy(self.np_matrix)

        for tab_u in range(self.over_u):
            listu_i = range(self.size_bn - 1, self.size_maxu)
            fix_tab = [self.size_bn - (tab_u + 1) for i in listu_i]

            for fix, index in zip(fix_tab, listu_i):
                self.ku_matrix[fix, index + 1] = self.full_matrix[fix, index + 1]
                self.ku_matrix[index + 1, fix] = self.full_matrix[index + 1, fix]

        to_estimate = copy(matrix(self.ku_matrix))
        self.sparsity = 1.0 - (
            np.count_nonzero(np.array(to_estimate)) / np.array(to_estimate).size
        )

    def do_completion(self):
        """Final completion."""
        pmcs = cp.maxcardsearch(self.ku_matrix)
        symbolic = cp.symbolic(self.ku_matrix, p=pmcs)
        chordal_sp = cp.cspmatrix(symbolic)
        chordal_sp += self.ku_matrix

        # make the completion
        start_time = time()
        self.final_cmpl = matrix(cp.psdcompletion(chordal_sp))
        self.time_cmpl = time() - start_time
        self.comment = "SUCCESS"

    def norm_error(self):
        """Normalisation Frobenius error.
        Compare the Frobenuis length of the NP matrix and completion matrix.

        Return:
            The error -> float
        """
        return np.linalg.norm(
            matrix(self.full_matrix) - self.final_cmpl, "fro"
        ) / np.linalg.norm(matrix(self.full_matrix), "fro")

    def mean_sqare_er(self):
        """Mean square error.

        Return:
            The error -> float
        """
        difference_array = np.subtract(matrix(self.full_matrix), self.final_cmpl)
        squared_array = np.square(difference_array)
        return squared_array.mean()

    def calc_error(self):
        """Calculate all the completion error."""
        self.mse = self.mean_sqare_er()
        self.norm_err = self.norm_error()
