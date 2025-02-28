'''
QENTANGLE Quantum Education Library
==========================
A simple Python 3.11 library to introduce quantum computing concepts to G6-12/post-secondary students.  A companion to the Entangled: Jasmine & the Quantum Sword educational program by the Center for Science Engagement.  engagescience.org. 
This library provides basic quantum gates, quantum circuits, and entanglement operations.

Features:
---------
- Basic quantum gates: Identity, Hadamard, Pauli-X, CNOT
- Bell state creation
- GHZ state creation
- Quantum circuit simulation
'''

import numpy as np

# Quantum Gates
def I():  # Identity Gate
    """Returns the Identity gate."""
    return np.array([[1, 0], [0, 1]])

def H():  # Hadamard Gate
    """Returns the Hadamard gate, which creates superposition."""
    return np.array([[1, 1], [1, -1]]) / np.sqrt(2)

def X():  # Pauli-X (NOT Gate)
    """Returns the Pauli-X gate, which flips qubit states."""
    return np.array([[0, 1], [1, 0]])

def CNOT():  # Controlled-NOT Gate
    """Returns the Controlled-NOT (CNOT) gate for two qubits."""
    return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

# Quantum Circuit Class
class QuantumCircuit:
    """Represents a quantum circuit with basic gate operations and entanglement."""
    
    def __init__(self, num_qubits):
        """Initializes a quantum circuit with the given number of qubits."""
        self.num_qubits = num_qubits
        self.state = np.zeros(2**num_qubits)
        self.state[0] = 1  # Start in |00..0> state
        self.gates = []

    def apply_gate(self, gate, qubit):
        """Applies a single-qubit gate to the specified qubit."""
        self.gates.append((gate.__name__, qubit))
        self.state = np.dot(np.kron(np.eye(2**qubit), np.kron(gate(), np.eye(2**(self.num_qubits-qubit-1)))), self.state)

    def cnot(self, control, target):
        """Applies a Controlled-NOT gate between control and target qubits."""
        self.gates.append(('CNOT', control, target))
        self.state = np.dot(CNOT(), self.state)

    def create_bell_pair(self):
        """Creates a Bell state: (|00> + |11>) / sqrt(2)."""
        self.apply_gate(H, 0)
        self.cnot(0, 1)

    def create_ghz_state(self):
        """Creates a GHZ state: (|000> + |111>) / sqrt(2) for num_qubits >= 2."""
        if self.num_qubits < 2:
            raise ValueError("GHZ state requires at least 2 qubits")
        self.apply_gate(H, 0)
        for i in range(self.num_qubits - 1):
            self.cnot(i, i + 1)

    def draw(self):
        """Displays the applied gates in sequence."""
        for gate in self.gates:
            print(f"Applied {gate}")

    def simulate(self):
        """Simulates the quantum circuit and prints the probability distribution."""
        probabilities = np.abs(self.state) ** 2
        for i, prob in enumerate(probabilities):
            print(f"State |{bin(i)[2:].zfill(self.num_qubits)}> : {prob:.2f}")

# Example usage
if __name__ == "__main__":
    qc = QuantumCircuit(2)
    qc.create_bell_pair()
    qc.draw()
    qc.simulate()

    qc2 = QuantumCircuit(3)
    qc2.create_ghz_state()
    qc2.draw()
    qc2.simulate()
