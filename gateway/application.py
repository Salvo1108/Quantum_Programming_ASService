#!/usr/bin/python
# -*- coding: utf-8 -*-
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
from database import *
from algorithms import *
from qiskit.tools.visualization import plot_histogram
import os

app = Flask(__name__)
db = Database.connect()
qiskit = Qiskit()
algoritmo = AlgorithmsStrategy()


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


@app.route('/APIquantum', methods=['POST'])
def personaQuantumAPI():
    """nome dell'algoritmo preso dalla richiesta"""
    algo = request.form.get('name_algorithm', type=str)
    """numero qbit preso dalla richiesta necessario per verificare quale macchina quantistica è più libera"""
    num_qbit = request.form.get('num_qbit', type=int)

    algoritmopersonal = AlgorithmsStrategy.PersonalAlgorithms(algoritmo,algo, num_qbit, db, qiskit)

    return algoritmopersonal

@app.route('/quantumAPI', methods=['POST'])
def quantumAPI():
    switch = request.form.get('type_selected', type=str)
    log_size = request.form.get('log_size', type=int)
    case = request.form.get('case_selected', type=str)
    num_qbitMaschine = request.form.get('NumQubitsMaschine', type=int)
    num_qubits = request.form.get('num_qubits', type=int)
    bynary_string = request.form.get('bynary_string', type=str)
    n_count = request.form.get('num_qubits', type=int)
    a = request.form.get('num', type=int)

    if switch == 'DeutschJozsa':

        deutJozsa = AlgorithmsStrategy.DeutschJozsa(algoritmo, log_size, case, num_qbitMaschine, db, qiskit)

        return render_template('result.html', message='Deutsch Jozsa algorithm executed correctly', circuit=deutJozsa,
                               page='execution')

    elif switch == 'BernsteinVazirani':

        bernVazirani = AlgorithmsStrategy.BernsteinVazirani(algoritmo, num_qubits, bynary_string, num_qbitMaschine, db, qiskit)

        return render_template('result.html',
                               message='Bernstein Vazirani algorithm executed correctly'
                               , circuit=bernVazirani, page='execution')
    elif switch == 'Simons':

        simons = AlgorithmsStrategy.Simons(algoritmo, num_qubits, bynary_string, num_qbitMaschine, db, qiskit)

        return render_template('result.html',
                               message='Simons algorithm executed correctly'
                               , circuit=simons, page='execution')
    elif switch == 'Shors':

        shors = AlgorithmsStrategy.Shors(algoritmo, n_count, a, num_qbitMaschine, db, qiskit)

        return render_template('result.html',
                               message="Shor's algorithm executed correctly"
                               , circuit=shors, page='execution')
    elif switch == 'Grovers':

        grovers = AlgorithmsStrategy.Grovers(algoritmo, num_qubits, num_qbitMaschine, db, qiskit)

        return render_template('result.html',
                               message="Grover's algorithm executed correctly"
                               , circuit=grovers, page='execution')

    elif switch == 'WalkSerachHypercube':

        walkHyper = AlgorithmsStrategy.WalkSerachHypercube(algoritmo, num_qubits, num_qbitMaschine, db, qiskit)

        return render_template('result.html',
                               message='Walk Serach Hypercube algorithm executed correctly'
                               , circuit=walkHyper, page='execution')
    else:

        return render_template('result.html', message='Error!',
                               circuit='error.png', page='execution')


@app.route('/insertAlgorithm', methods=['GET', 'POST'])
def insertAlgorithm():
    name = request.form.get('name_selected', type=str)
    algoritmo = request.form.get('algorithm', type=str)
    descrizione = request.form.get('description', type=str)

    insert = AlgorithmsStrategy.insert(algoritmo, name, algoritmo, descrizione, db)

    return render_template('result.html',
                           message='Algorithm upload successfully!',
                           circuit='Success.png', page='insert')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
