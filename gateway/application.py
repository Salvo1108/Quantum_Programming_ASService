from flask import Flask, request, url_for, redirect, render_template
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
    return render_template('welcomePage.html')

@app.route('/choise_Algorithms', methods=['GET', 'POST'])
def choise_Algorithms():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('choiseAlgorithms.html')

@app.route('/insert_Algorithms', methods=['GET', 'POST'])
def insert_Algorithms():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('insertAlgorithms.html')

@app.route('/back', methods=['GET', 'POST'])
def back():
    return redirect(url_for('index'))


@app.route('/quantumAPI', methods=['POST'])
def quantumAPI():

    switch = request.form.get('type_selected', type=int)
    print(switch,flush=True)
    if switch == 1:
        log_size = request.form.get('log_size', type=int)
        case = request.form.get('case_selected', type=str)
        # Getting the current date and time
        dt = datetime.now()
        oracle_gate = dj_oracle(case, log_size)
        dj_circuit = dj_algorithm(oracle_gate, log_size)
        cir = dj_circuit.draw(output='mpl')
        pathImg = './static/DeutschJozsa_' + dt.strftime("%m-%d-%Y_%H:%M:%S") + '.png'
        cir.savefig(pathImg)
        dj_circuit.qasm(formatted=True, filename="DeutschJozsa.qasm")

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
        pathImgNew = pathImg.replace("./static/","")

        return render_template('result.html', message="Deutsch Jozsa algorithm executed correctly", circuit=pathImgNew)

    elif switch == 2:
        num_qubits = request.form.get('num_qubits', type=int)
        bynary_string = request.form.get('bynary_string', type=str)
        # Getting the current date and time
        dt = datetime.now()
        bV_circuit = bv_algorithm(num_qubits, bynary_string)
        cir = bV_circuit.draw(output='mpl')
        pathImg = './static/DeutschJozsa_' + dt.strftime("%m-%d-%Y_%H:%M:%S") + '.png'
        cir.savefig(pathImg)
        bV_circuit.qasm(formatted=True, filename="BernsteinVazirani.qasm")
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
        pathImgNew = pathImg.replace("./static/", "")

        return render_template('result.html', message="Bernstein Vazirani algorithm executed correctly", circuit=pathImgNew)

    elif switch == 3:
        num_qubits = request.form.get('num_qubits', type=int)
        bynary_string = request.form.get('bynary_string', type=str)
        S_circuit = s_algorithm(bynary_string, num_qubits)
        # Getting the current date and time
        dt = datetime.now()
        cir = S_circuit.draw(output='mpl')
        pathImg = './static/AlgoritmoSimons_' + dt.strftime("%m-%d-%Y_%H:%M:%S") + '.png'
        cir.savefig(pathImg)
        S_circuit.qasm(formatted=True, filename="AlgoritmoSimons.qasm")

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
        pathImgNew = pathImg.replace("./static/", "")
        return render_template('result.html', message="Simons algorithm executed correctly",
                               circuit=pathImgNew)

    elif switch == 4:
        n_count = request.form.get('num_qubits', type=int)
        a = request.form.get('num', type=int)
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
        # Getting the current date and time
        dt = datetime.now()

        cir = qc.draw(fold=-1, output='mpl') # -1 means 'do not fold'
        pathImg = './static/AlgoritmoShors_' + dt.strftime("%m-%d-%Y_%H:%M:%S") + '.png'
        cir.savefig(pathImg)
        qc.qasm(formatted=True, filename="AlgoritmoShor's.qasm")

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
        pathImgNew = pathImg.replace("./static/", "")
        return render_template('result.html', message="Shor's algorithm executed correctly",
                               circuit=pathImgNew)

    elif switch == 5:
        num_qubits = request.form.get('num_qubits', type=int)
        circuit = gr_algorithm(num_qubits)
        # Getting the current date and time
        dt = datetime.now()
        cir = circuit.draw(output='mpl')
        pathImg = './static/AlgoritmoGrovers_' + dt.strftime("%m-%d-%Y_%H:%M:%S") + '.png'
        cir.savefig(pathImg)
        circuit.qasm(formatted=True, filename="AlgoritmoGrover's.qasm")

        with open("AlgoritmoGrover's.qasm", "rb") as f:
            encoded = Binary(f.read())

        mycol.insert_one({
            "nome": "Algoritmo Grover's",
            "num_qubits": num_qubits,
            "data": dt,
            "file": encoded,
        })
        os.remove("AlgoritmoGrover's.qasm")
        pathImgNew = pathImg.replace("./static/", "")
        return render_template('result.html', message="Grover's algorithm executed correctly",
                               circuit=pathImgNew)

    elif switch == 6:
        num_qubits = request.form.get('num_qubits', type=int)
        circuit = ws_algorithm(num_qubits)
        # Getting the current date and time
        dt = datetime.now()
        cir = circuit.draw(output='mpl')
        pathImg = './static/AlgoritmoWalkSerachHypercube_' + dt.strftime("%m-%d-%Y_%H:%M:%S") + '.png'
        cir.savefig(pathImg)
        circuit.qasm(formatted=True, filename="AlgoritmoWalkSerachHypercube.qasm")

        with open("AlgoritmoWalkSerachHypercube.qasm", "rb") as f:
            encoded = Binary(f.read())

        mycol.insert_one({
            "nome": "Algoritmo Walk Serach Hypercube",
            "num_qubits": num_qubits,
            "data": dt,
            "file": encoded,
        })
        os.remove("AlgoritmoWalkSerachHypercube.qasm")
        pathImgNew = pathImg.replace("./static/", "")
        return render_template('result.html', message="Walk Serach Hypercube algorithm executed correctly",
                               circuit=pathImgNew)

    else:
        return render_template('result.html', message="Error!",
                               circuit="error.png")


@app.route('/getAlgorithmFilebyName', methods=['GET', 'POST'])
def getAlgorithmFile():
    nome_algoritmo = request.args.get('name', type=str)
    query = mycol.find({'nome': nome_algoritmo})
    for a in query:
       file = a["file"]

    return file

@app.route('/insertAlgorithm', methods=['GET', 'POST'])
def insertAlgorithm():
    name = request.form.get('name_selected', type=str)
    algoritmo = request.form.get('algorithm', type=str)
    # Getting the current date and time
    dt = datetime.now()
    pathName = "Algoritmo_personal_" + dt.strftime("%m-%d-%Y_%H:%M:%S") + '.txt'
    text_file = open(pathName, "w")
    n = text_file.write(algoritmo)
    text_file.close()

    with open(pathName, "rb") as f:
        encoded = Binary(f.read())

    mycol.insert_one({
        "nome": name,
        "data": dt,
        "file": encoded,
    })

    os.remove(pathName)

    return render_template('result.html', message="Algorithm upload successfully!",
                           circuit="Success.png", page="insert")


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



