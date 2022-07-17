from flask import Flask, request
from deutschJozsa import *
from bernsteinVazirani import *
from simons import *
from shors import *
from grovers import *
from walkSearch import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Flask server"


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



