# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, IBMQ
# Loading your IBM Q account(s)

# Shift operator function for 4d-hypercube
def shift_operator(circuit):
    for i in range(0,4):
        circuit.x(4)
        if i%2==0:
            circuit.x(5)
        circuit.ccx(4,5,i)

def ws_algorithm(qubits):
    one_step_circuit = QuantumCircuit(qubits, name=' ONE STEP')
    # Coin operator
    one_step_circuit.h([4,5])
    one_step_circuit.z([4,5])
    one_step_circuit.cz(4,5)
    one_step_circuit.h([4,5])
    one_step_circuit.draw()

    shift_operator(one_step_circuit)
    one_step_gate = one_step_circuit.to_instruction()

    return one_step_gate
