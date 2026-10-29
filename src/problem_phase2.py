import numpy as np
from qiskit import QuantumCircuit

class Knapsack9QubitQUBO:
    def __init__(self, values=[10, 4, 7, 5, 8], weights=[5, 3, 4, 2, 6], capacity=15, penalty=5.0):
        self.values = np.array(values)
        self.weights = np.array(weights)
        self.capacity = capacity
        self.penalty = penalty
        self.num_items = len(values)
        self.num_slack = 4
        self.num_qubits = self.num_items + self.num_slack
        self.v_star = 26  # Exact classical optimum value
        self.opt_item_tuple = (1, 1, 1, 1, 0)  # Items 0, 1, 2, 3 selected

    def get_qubo_matrix(self):
        Q = np.zeros((self.num_qubits, self.num_qubits))
        
        # Minimization objective: -v_i * x_i
        for i in range(self.num_items):
            Q[i, i] -= self.values[i]
            
        # Linear & quadratic penalty coefficients for all 9 variables
        coeffs = np.zeros(self.num_qubits)
        coeffs[:self.num_items] = self.weights
        for k in range(self.num_slack):
            coeffs[self.num_items + k] = 2**k
            
        # P * (sum c_i z_i - C)^2 expansion
        for i in range(self.num_qubits):
            Q[i, i] += self.penalty * (coeffs[i]**2 - 2 * self.capacity * coeffs[i])
            for j in range(i + 1, self.num_qubits):
                Q[i, j] += 2 * self.penalty * coeffs[i] * coeffs[j]
                
        return Q

    def evaluate_item_tuple(self, x_tuple):
        # x_tuple contains logical (x0, x1, x2, x3, x4)
        x = np.array(x_tuple[:5])
        total_w = np.dot(self.weights, x)
        total_v = np.dot(self.values, x)
        is_feasible = total_w <= self.capacity
        return total_v, total_w, is_feasible

def build_qaoa_circuit(qubo_matrix, gamma, beta):
    n = qubo_matrix.shape[0]
    qc = QuantumCircuit(n)
    qc.h(range(n))
    
    # Cost Layer U(H_C, gamma)
    for i in range(n):
        if abs(qubo_matrix[i, i]) > 1e-6:
            qc.rz(2 * gamma * qubo_matrix[i, i], i)
            
    for i in range(n):
        for j in range(i + 1, n):
            if abs(qubo_matrix[i, j]) > 1e-6:
                qc.cx(i, j)
                qc.rz(2 * gamma * qubo_matrix[i, j], j)
                qc.cx(i, j)
                
    # Mixer Layer U(H_B, beta)
    for i in range(n):
        qc.rx(2 * beta, i)
        
    qc.measure_all()
    return qc