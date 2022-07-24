from flask import Flask, request
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
from flask import  request
import os

# establish a connection to the database
connection = pymongo.MongoClient()


app = Flask(__name__)
try:
    conn = MongoClient("mongodb://localhost:27017/")
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")


mydb = conn["QuantumAPI"]
mycol = mydb["algorithm"]

@app.route('/', methods=['GET'])
def index():

    return "Welcome on board!"


@app.route('/quantumAPI', methods=['POST'])
def quantumAPI():

    switch = request.args.get('type', type=int)
    if switch == 1:
        log_size = request.args.get('log_size', type=int)
        case = request.args.get('case', type=str)
        oracle_gate = dj_oracle(case, log_size)
        dj_circuit = dj_algorithm(oracle_gate, log_size)
        dj_circuit.draw()
        dj_circuit.qasm(formatted=True, filename="DeutschJozsa.qasm")
        # Getting the current date and time
        dt = datetime.now()
        with open("DeutschJozsa.qasm", "rb") as f:
            encoded = Binary(f.read())

        mycol.insert_one({
            "nome": "Deutsch Jozsa",
            "log_size": log_size,
            "data": dt,
            "case": case,
            "file": encoded,
        })
        os.remove("DeutschJozsa.qasm")

        return "Algoritmo Deutsch Jozsa OK"

    elif switch == 2:
        num_qubits = request.args.get('num_qubits', type=int)
        bynary_string = request.args.get('bynary_string', type=str)
        bV_circuit = bv_algorithm(num_qubits, bynary_string)
        bV_circuit.draw()
        bV_circuit.qasm(formatted=True, filename="BernsteinVazirani.qasm")
        # Getting the current date and time
        dt = datetime.now()
        with open("BernsteinVazirani.qasm", "rb") as f:
            encoded = Binary(f.read())

        mycol.insert_one({
            "nome": "Bernstein Vazirani",
            "num_qubits": num_qubits,
            "data": dt,
            "bynary_string": bynary_string,
            "file": encoded,
        })
        os.remove("BernsteinVazirani.qasm")

        return "Algoritmo Bernstein Vazirani OK"

    elif switch == 3:
        num_qubits = request.args.get('num_qubits', type=int)
        bynary_string = request.args.get('bynary_string', type=str)
        S_circuit = s_algorithm(bynary_string, num_qubits)
        S_circuit.draw()
        S_circuit.qasm(formatted=True, filename="AlgoritmoSimons.qasm")
        # Getting the current date and time
        dt = datetime.now()
        with open("AlgoritmoSimons.qasm", "rb") as f:
            encoded = Binary(f.read())

        mycol.insert_one({
            "nome": "Algoritmo Simons",
            "num_qubits": num_qubits,
            "data": dt,
            "bynary_string": bynary_string,
            "file": encoded,
        })
        os.remove("AlgoritmoSimons.qasm")
        return "Algoritmo Simons OK"

    elif switch == 4:
        n_count = request.args.get('num_qubits', type=int)
        a = request.args.get('num', type=int)
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
            qc.append(c_amod15(a, 2 ** q),
                      [q] + [i + n_count for i in range(4)])
        # Do inverse-QFT
        qc.append(qft_dagger(n_count), range(n_count))
        # Measure circuit
        qc.measure(range(n_count), range(n_count))
        qc.draw(fold=-1)  # -1 means 'do not fold'
        qc.qasm(formatted=True, filename="AlgoritmoShor's.qasm")
        # Getting the current date and time
        dt = datetime.now()
        with open("AlgoritmoShor's.qasm", "rb") as f:
            encoded = Binary(f.read())

        mycol.insert_one({
            "nome": "Algoritmo Shor's",
            "num_qubits": n_count,
            "data": dt,
            "num": a,
            "file": encoded,
        })
        os.remove("AlgoritmoShor's.qasm")
        return "Algoritmo Shor's OK"

    elif switch == 4:
        num_qubits = request.args.get('num_qubits', type=int)
        circuit = gr_algorithm(num_qubits)
        circuit.draw()
        circuit.qasm(formatted=True, filename="AlgoritmoGrover's.qasm")
        # Getting the current date and time
        dt = datetime.now()
        with open("AlgoritmoGrover's.qasm", "rb") as f:
            encoded = Binary(f.read())

        mycol.insert_one({
            "nome": "Algoritmo Grover's",
            "num_qubits": num_qubits,
            "data": dt,
            "file": encoded,
        })
        os.remove("AlgoritmoGrover's.qasm")
        return "Algoritmo Grover's OK"

    elif switch == 5:
        num_qubits = request.args.get('num_qubits', type=int)
        circuit = ws_algorithm(num_qubits)
        circuit.draw()
        circuit.qasm(formatted=True, filename="AlgoritmoWalkSerachHypercube.qasm")
        # Getting the current date and time
        dt = datetime.now()
        with open("AlgoritmoWalkSerachHypercube.qasm", "rb") as f:
            encoded = Binary(f.read())

        mycol.insert_one({
            "nome": "Algoritmo Walk Serach Hypercube",
            "num_qubits": num_qubits,
            "data": dt,
            "file": encoded,
        })
        os.remove("AlgoritmoWalkSerachHypercube.qasm")
        return "Algoritmo Walk Serach Hypercube OK"

    else:
        return "Nessun Algoritmo trovato"


@app.route('/getAlgorithmFilebyName', methods=['GET', 'POST'])
def getAlgorithmFile():
    nome_algoritmo = request.args.get('name', type=str)
    query = mycol.find({'nome': nome_algoritmo})
    for a in query:
       file = a["file"]

    return file

@app.route('/insertAlgorithm', methods=['GET', 'POST'])
def insertAlgorithm():
    algoritmo = request.args.get('algoritmo', type=str)
    a = algoritmo.qasm(formatted=True, filename="Algoritmo_personal.qasm")
    print(a)
    return "Inserimento Algoritmo effettuato con successo!"

@app.route('/deutschJozsa', methods=['POST'])
def algorithmsJozsa():
    log_size = request.args.get('log_size', type=int)
    case = request.args.get('case', type=str)
    oracle_gate = dj_oracle(case, log_size)
    dj_circuit = dj_algorithm(oracle_gate, log_size)
    print(dj_circuit.draw())

    return "Algoritmo Deutsch Jozsa OK"

@app.route('/bernsteinVazirani', methods=['POST'])
def algorithmsVazirani():
    num_qubits = request.args.get('num_qubits', type=int)
    bynary_string = request.args.get('bynary_string', type=str)
    bV_circuit = bv_algorithm(num_qubits, bynary_string)
    print(bV_circuit.draw())

    return "Algoritmo Bernstein Vazirani OK"

@app.route('/simons', methods=['POST'])
def algorithmSimons():
    num_qubits = request.args.get('num_qubits', type=int)
    bynary_string = request.args.get('bynary_string', type=str)
    S_circuit = s_algorithm(bynary_string, num_qubits)
    print(S_circuit.draw())

    return "Algoritmo Simons OK"

@app.route('/shors', methods=['POST'])
def algorithmShors():
    n_count = request.args.get('num_qubits', type=int)
    a = request.args.get('num', type=int)
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
        qc.append(c_amod15(a, 2 ** q),
                  [q] + [i + n_count for i in range(4)])
    # Do inverse-QFT
    qc.append(qft_dagger(n_count), range(n_count))
    # Measure circuit
    qc.measure(range(n_count), range(n_count))
    print(qc.draw(fold=-1))  # -1 means 'do not fold'

    return "Algoritmo Shor's OK"

@app.route('/grovers', methods=['POST'])
def algorithmGrovers():
    num_qubits = request.args.get('num_qubits', type=int)
    circuit = gr_algorithm(num_qubits)
    print(circuit.draw())

    return "Algoritmo Grover's OK"

@app.route('/walkSearchHypercube', methods=['POST'])
def algorithmWalkSearch():
    num_qubits = request.args.get('num_qubits', type=int)
    circuit = ws_algorithm(num_qubits)
    print(circuit.draw())

    return "Algoritmo Walk Serach Hypercube OK"

@app.route('/checkBusyDevice', methods=['POST'])
def checkDevice():
    # Load our saved IBMQ accounts and get the least busy backend device with greater than or equal to (n+1) qubits
    num = request.args.get('num_qbit', type=int)
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= (num + 1) and
                                                             not x.configuration().simulator and x.status().operational == True))
    print("least busy backend: ", backend)

    return "Device Trovato"

@app.route('/saveAccountIBM', methods=['GET'])
def saveAccount():
    IBMQ.save_account(
        "3bcafaa7577ea475b89cd6cead08d8db9eb1122f2f873c0d31e1704e1c0fb51503881220945b3443ed4ce738996b5ea2f6281cd39bedd0936f02c7400aa71ccf", overwrite=True
    )

    return "Account IBM Salvato"

if __name__ == "__main__":
    app.run(port=5000, debug=True)



