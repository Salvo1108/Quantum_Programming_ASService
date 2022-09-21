from abc import ABC, abstractmethod
from flask import request
from qiskit import *
from qiskit.providers.ibmq import least_busy


class ProviderStrategy(ABC):

    @abstractmethod
    def connect(self, num_qbit: int):
        """verifica disponibilità macchina quantistica e ritorna il nome"""
        pass


class Qiskit(ProviderStrategy):

    def connect(self, num_qbit: int):
        super().connect(num_qbit)
        IBMQ.save_account(
            '3bcafaa7577ea475b89cd6cead08d8db9eb1122f2f873c0d31e1704e1c0fb51503881220945b3443ed4ce738996b5ea2f6281cd39bedd0936f02c7400aa71ccf'
            , overwrite=True)
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='ibm-q')
        backend = least_busy(provider.backends(filters=lambda x: \
            x.configuration().n_qubits >= num_qbit + 1 \
            and not x.configuration().simulator \
            and x.status().operational == True))
        device = provider.get_backend(str(backend))

        return device
