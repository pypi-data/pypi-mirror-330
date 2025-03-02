from qubots.base_optimizer import BaseOptimizer

class QuantumClassicalPipeline(BaseOptimizer):
    def __init__(self, quantum_routine, classical_optimizer):
        self.quantum_routine = quantum_routine
        self.classical_optimizer = classical_optimizer

    def optimize(self, problem):
        
        # Run the quantum routine with the QUBO data.
        print("Running quantum routine...")
        
        quantum_solution, quantum_cost = self.quantum_routine.optimize(
            problem
        )
        print(f"Quantum routine produced cost: {quantum_cost}")
        
        # Now run the classical optimizer, seeding it with the quantum solution.
        print("Refining solution using classical optimizer...")
        classical_solution, classical_cost = self.classical_optimizer.optimize(
            problem, initial_solution=quantum_solution
        )
        print(f"Classical optimizer refined cost: {classical_cost}")
        
        return classical_solution, classical_cost

def create_quantum_classical_pipeline(quantum_routine, classical_optimizer):
    return QuantumClassicalPipeline(quantum_routine, classical_optimizer)
