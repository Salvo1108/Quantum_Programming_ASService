from abc import ABC, abstractmethod
from flask import request
from qiskit import *
from flask import Flask, request, url_for, redirect, render_template
from provider import *
from deutschJozsa import *
from bernsteinVazirani import *
from simons import *
from shors import *
from grovers import *
from walkSearch import *
import pymongo
from pymongo import MongoClient
from datetime import datetime
from bson.binary import Binary
from qiskit import *
from qiskit.tools.visualization import plot_histogram
import os
from qiskit.providers.ibmq import least_busy


class AlgorithmsStrategy:

    def DeutschJozsa(self, log_size: int, case_selected: str, num_qbit: int, db, provider):
        log_size = request.form.get('log_size', type=int)
        case = request.form.get('case_selected', type=str)

        # Getting the current date and time

        dt = datetime.now()
        oracle_gate = dj_oracle(case, log_size)
        dj_circuit = dj_algorithm(oracle_gate, log_size)

        """verifica disponibilità macchina quantistica"""
        macchina_free = provider.connect(num_qbit)

        """esecuzione circuito"""
        result = execute(dj_circuit, backend=macchina_free).result()
        final = result.get_counts(dj_circuit)

        cir = dj_circuit.draw(output='mpl')
        pathImg = './static/DeutschJozsa_' \
                  + dt.strftime('%m-%d-%Y_%H:%M:%S') + '.png'
        cir.savefig(pathImg)
        dj_circuit.qasm(formatted=True, filename='DeutschJozsa.qasm')

        with open('DeutschJozsa.qasm', 'rb') as f:
            encoded = Binary(f.read())

        db.insert_one({
            'nome': 'Deutsch Jozsa',
            'log_size': log_size,
            'data': dt,
            'case': case,
            'insert': False,
            'file': encoded,
            'result': final,
        })
        os.remove('DeutschJozsa.qasm')
        pathImgNew = pathImg.replace('./static/', '')

        return pathImgNew

    def BernsteinVazirani(self, num_qubits: int, bynary_string: str, num_qbit: int, db, provider):
        # Getting the current date and time

        dt = datetime.now()
        bV_circuit = bv_algorithm(num_qubits, bynary_string)

        """verifica disponibilità macchina quantistica"""
        macchina_free = provider.connect(num_qbit)

        """esecuzione circuito"""
        result = execute(bV_circuit, backend=macchina_free).result()
        final = result.get_counts(bV_circuit)

        cir = bV_circuit.draw(output='mpl')
        pathImg = './static/BernsteinVazirani_' \
                  + dt.strftime('%m-%d-%Y_%H:%M:%S') + '.png'
        cir.savefig(pathImg)
        bV_circuit.qasm(formatted=True,
                        filename='BernsteinVazirani.qasm')
        with open('BernsteinVazirani.qasm', 'rb') as f:
            encoded = Binary(f.read())

        db.insert_one({
            'nome': 'Bernstein Vazirani',
            'num_qubits': num_qubits,
            'data': dt,
            'bynary_string': bynary_string,
            'insert': False,
            'file': encoded,
            'result': final,
        })
        os.remove('BernsteinVazirani.qasm')
        pathImgNew = pathImg.replace('./static/', '')

        return pathImgNew

    def Simons(self, num_qubits: int, bynary_string: str, num_qbit: int, db, provider):
        # Getting the current date and time

        S_circuit = s_algorithm(bynary_string, num_qubits)

        """verifica disponibilità macchina quantistica"""
        macchina_free = provider.connect(num_qbit)

        """esecuzione circuito"""
        result = execute(S_circuit, backend=macchina_free).result()
        final = result.get_counts(S_circuit)

        # Getting the current date and time

        dt = datetime.now()
        cir = S_circuit.draw(output='mpl')
        pathImg = './static/AlgoritmoSimons_' \
                  + dt.strftime('%m-%d-%Y_%H:%M:%S') + '.png'
        cir.savefig(pathImg)
        S_circuit.qasm(formatted=True, filename='AlgoritmoSimons.qasm')

        with open('AlgoritmoSimons.qasm', 'rb') as f:
            encoded = Binary(f.read())

        db.insert_one({
            'nome': 'Algoritmo Simons',
            'num_qubits': num_qubits,
            'data': dt,
            'bynary_string': bynary_string,
            'insert': False,
            'file': encoded,
            'result': final,
        })
        os.remove('AlgoritmoSimons.qasm')
        pathImgNew = pathImg.replace('./static/', '')

        return pathImgNew

    def Shors(self, n_count: int, a: int, num_qbit: int, db, provider):
        # Create QuantumCircuit with n_count counting qubits
        # plus 4 qubits for U to act on

        qc = QuantumCircuit(n_count + 4, n_count)

        # Initialize counting qubits
        # in state |+>

        for q in range(n_count):
            qc.h(q)

        # And auxiliary register in state |1>

        qc.x(3 + n_count)

        # Do controlled-U operations

        for q in range(n_count):
            qc.append(c_amod15(a, 2 ** q), [q] + [i + n_count for i in
                                                  range(4)])

        # Do inverse-QFT

        qc.append(qft_dagger(n_count), range(n_count))

        # Measure circuit

        qc.measure(range(n_count), range(n_count))

        # Getting the current date and time

        dt = datetime.now()
        """verifica disponibilità macchina quantistica"""
        macchina_free = provider.connect(num_qbit)

        """esecuzione circuito"""
        result = execute(qc, backend=macchina_free).result()
        final = result.get_counts(qc)

        cir = qc.draw(fold=-1, output='mpl')  # -1 means 'do not fold'
        pathImg = './static/AlgoritmoShors_' \
                  + dt.strftime('%m-%d-%Y_%H:%M:%S') + '.png'
        cir.savefig(pathImg)
        qc.qasm(formatted=True, filename="AlgoritmoShor's.qasm")

        with open("AlgoritmoShor's.qasm", 'rb') as f:
            encoded = Binary(f.read())

        db.insert_one({
            'nome': "Algoritmo Shor's",
            'num_qubits': n_count,
            'data': dt,
            'num': a,
            'insert': False,
            'file': encoded,
            'result': final,
        })
        os.remove("AlgoritmoShor's.qasm")
        pathImgNew = pathImg.replace('./static/', '')

        return pathImgNew

    def Grovers(self, num_qubits: int, num_qbit: int, db, provider):
        circuit = gr_algorithm(num_qubits)

        """verifica disponibilità macchina quantistica"""
        macchina_free = provider.connect(num_qbit)

        """esecuzione circuito"""
        result = execute(circuit, backend=macchina_free).result()
        final = result.get_counts(circuit)

        # Getting the current date and time

        dt = datetime.now()
        cir = circuit.draw(output='mpl')
        pathImg = './static/AlgoritmoGrovers_' \
                  + dt.strftime('%m-%d-%Y_%H:%M:%S') + '.png'
        cir.savefig(pathImg)
        circuit.qasm(formatted=True, filename="AlgoritmoGrover's.qasm")

        with open("AlgoritmoGrover's.qasm", 'rb') as f:
            encoded = Binary(f.read())

        db.insert_one({
            'nome': "Algoritmo Grover's",
            'num_qubits': num_qubits,
            'data': dt,
            'insert': False,
            'file': encoded,
            'result': final,
        })
        os.remove("AlgoritmoGrover's.qasm")
        pathImgNew = pathImg.replace('./static/', '')

        return pathImgNew

    def WalkSerachHypercube(self, num_qubits: int, num_qbit: int, db, provider):
        circuit = ws_algorithm(num_qubits)

        """verifica disponibilità macchina quantistica"""
        macchina_free = provider.connect(num_qbit)

        """esecuzione circuito"""
        result = execute(circuit, backend=macchina_free).result()
        final = result.get_counts(circuit)

        # Getting the current date and time

        dt = datetime.now()
        cir = circuit.draw(output='mpl')
        pathImg = './static/AlgoritmoWalkSerachHypercube_' \
                  + dt.strftime('%m-%d-%Y_%H:%M:%S') + '.png'
        cir.savefig(pathImg)
        circuit.qasm(formatted=True,
                     filename='AlgoritmoWalkSerachHypercube.qasm')

        with open('AlgoritmoWalkSerachHypercube.qasm', 'rb') as f:
            encoded = Binary(f.read())

        db.insert_one({
            'nome': 'Algoritmo Walk Serach Hypercube',
            'num_qubits': num_qubits,
            'data': dt,
            'insert': False,
            'file': encoded,
        })
        os.remove('AlgoritmoWalkSerachHypercube.qasm')
        pathImgNew = pathImg.replace('./static/', '')

        return pathImgNew

    def PersonalAlgorithms(self, algo: str, num_qbit: int, db, provider):

        """nome dell'algoritmo preso dalla richiesta"""
        algo = request.form.get('name_algorithm', type=str)
        """numero qbit preso dalla richiesta necessario per verificare quale macchina quantistica è più libera"""
        num_qbit = request.form.get('num_qbit', type=int)

        """check sul db se è presente l'algoritmo richiesto"""
        result = db.find({'nome': algo})
        for x in result:
            if x['nome'] == algo:
                """salvataggio dell'algoritmo"""
                stringa_algo = x['algoritmo']
                """conversione stringa algoritmo salvata precedentemente in circuito"""
                new_circuito = QuantumCircuit.from_qasm_str(stringa_algo)
                new_circuito.draw()
                """verifica disponibilità macchina quantistica"""
                macchina_free = provider.connect(num_qbit)

                """esecuzione circuito"""
                result = execute(new_circuito, backend=macchina_free).result()
                final = result.get_counts(new_circuito)

                return final, 200

        return 'Algoritmo non presente!', 400

    def insert(self, name: str, algoritmo: str, descrizione: str, db):
        # Getting the current date and time
        dt = datetime.now()

        db.insert_one({
            'nome': name,
            'data': dt,
            'description': descrizione,
            'insert': True,
            'algoritmo': algoritmo,
        })

        return "Inserimento Ok", 200
