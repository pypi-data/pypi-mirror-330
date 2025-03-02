import qiskit
import numpy as np
import pennylane as qml

from .base import QubitGate
from .single import X, Y, Z
from ...quantum_info.state import Statevector


class DeutschOracle(QubitGate):
    """
    Oracle for Deutsch algorithm with ancilla qubit.
    Implements |x,y⟩ -> |x, y⊕f(x)⟩

    :param f: Function that takes an integer x (0 or 1) and returns 0 or 1
    """

    def __new__(cls, f):
        matrix = np.zeros((4, 4))
        for x in [0, 1]:
            matrix[x * 2 + f(x), x * 2] = 1  # |x,0⟩ -> |x,f(x)⟩
            matrix[x * 2 + (1 - f(x)), x * 2 + 1] = 1  # |x,1⟩ -> |x,1-f(x)⟩

        return super().__new__(cls, matrix)

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        # Reverse the order of qubits for Qiskit's little-endian convention
        return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label="DeutschOracle")


class DeutschJozsaOracle(QubitGate):
    """
    Oracle for Deutsch-Jozsa algorithm.

    For input x and output f(x), the oracle applies phase (-1)^f(x).
    - Constant function: f(x) is same for all x
    - Balanced function: f(x) = 1 for exactly half of inputs

    :param f: Function that takes an integer x (0 to 2^n-1) and returns 0 or 1
    :param n_bits: Number of input bits
    """

    def __new__(cls, f, n_bits: int):
        n_states = 2**n_bits
        outputs = [f(x) for x in range(n_states)]
        if not all(v in [0, 1] for v in outputs):
            raise ValueError("Function must return 0 or 1")

        ones = sum(outputs)
        if ones != 0 and ones != n_states and ones != n_states // 2:
            raise ValueError("Function must be constant or balanced")

        oracle_matrix = np.eye(n_states)
        for x in range(n_states):
            oracle_matrix[x, x] = (-1) ** f(x)

        return super().__new__(cls, oracle_matrix)

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        # Reverse the order of qubits for Qiskit's little-endian convention
        return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label="DeutschJozsaOracle")


class PhaseOracle(QubitGate):
    """
    Phase Oracle as used in Grover's search algorithm.
    :param target_state: The target state to mark.
    target_state is assumed to be in Big-Endian format.
    """

    def __new__(cls, target_state: np.ndarray):
        state = Statevector(target_state)
        n_qubits = state.num_qubits
        identity = np.eye(2**n_qubits)
        oracle_matrix = identity - 2 * np.outer(target_state, target_state.conj())
        return super().__new__(cls, oracle_matrix)

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        # Reverse the order of qubits for Qiskit's little-endian convention
        return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label="PhaseOracle")


class GroverDiffusion(QubitGate):
    """
    Grover Diffusion Operator Gate as used in Grover's search algorithm.
    This gate amplifies the amplitude of the marked state.
    :param n_qubits: The number of qubits in the system.
    """

    def __new__(cls, n_qubits: int):
        assert n_qubits >= 1, "GroverDiffusionGate must have at least one qubit."
        # Equal superposition state vector
        size = 2**n_qubits
        equal_superposition = np.ones(size) / np.sqrt(size)
        # Grover diffusion operator: 2|ψ⟩⟨ψ| - I
        diffusion_matrix = 2 * np.outer(equal_superposition, equal_superposition) - np.eye(size)
        return super().__new__(cls, diffusion_matrix)

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        # Reverse the order of qubits for Qiskit's little-endian convention
        return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label="GroverDiffusion")


class QFT(QubitGate):
    """
    n-qubit Quantum Fourier Transform gate.
    :param n_qubits: The number of qubits in the system.
    :param inverse: Whether to use the inverse QFT.
    - For example, in Shor's algorithm we use the inverse QFT.
    """

    def __new__(cls, n_qubits: int, inverse: bool = False):
        dim = 2**n_qubits
        matrix = np.zeros((dim, dim), dtype=complex)
        # Use positive exponent for QFT, negative for QFT†
        sign = -1 if inverse else 1
        omega = np.exp(sign * 2j * np.pi / dim)

        for i in range(dim):
            for j in range(dim):
                matrix[i, j] = omega ** (i * j) / np.sqrt(dim)

        instance = super().__new__(cls, matrix)
        instance.inverse = inverse
        return instance

    def to_qiskit(self):
        """Convert to a Qiskit circuit implementing QFT or QFT†."""
        n = self.num_qubits
        name = "QFT†" if self.inverse else "QFT"

        def create_qft(n_qubits):
            circuit = qiskit.QuantumCircuit(n_qubits, name=name)
            for i in range(n_qubits):
                circuit.h(i)
                for j in range(i + 1, n_qubits):
                    circuit.cp(2 * np.pi / 2 ** (j - i + 1), i, j)
            return circuit

        qc = create_qft(n)
        if self.inverse:
            qc = qc.inverse()
        qc.name = name
        return qc

    def to_qasm(self, qubits: list[int]) -> str:
        """Convert to OpenQASM code."""
        n = self.num_qubits
        assert len(qubits) == n, f"OpenQASM QFT requires {n} qubits."

        name = "QFT†" if self.inverse else "QFT"
        qasm_str = f"// {name} circuit (big-endian convention)\n"

        if self.inverse:
            for i in range(n // 2):
                qasm_str += f"swap q[{qubits[i]}], q[{qubits[n-i-1]}];\n"
            for i in range(n - 1, -1, -1):
                for j in range(n - 1, i, -1):
                    angle = -np.pi / (2 ** (j - i))
                    qasm_str += f"cu1({angle}) q[{qubits[i]}], q[{qubits[j]}];\n"
                qasm_str += f"h q[{qubits[i]}];\n"
        else:
            for i in range(n):
                qasm_str += f"h q[{qubits[i]}];\n"
                for j in range(i + 1, n):
                    angle = np.pi / (2 ** (j - i))
                    qasm_str += f"cu1({angle}) q[{qubits[i]}], q[{qubits[j]}];\n"
            for i in range(n // 2):
                qasm_str += f"swap q[{qubits[i]}], q[{qubits[n-i-1]}];\n"

        qasm_str += f"// End of {name} circuit\n"
        return qasm_str


class CX(QubitGate):
    """
    Controlled-X (CNOT) gate.
    Used to entangle two qubits.
    If the control qubit is |1>, the target qubit is flipped.
    """

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

    def to_qiskit(self) -> qiskit.circuit.library.CXGate:
        return qiskit.circuit.library.CXGate()

    def to_pennylane(self, wires: list[int]) -> qml.CNOT:
        assert len(wires) == 2, "PennyLane CX gate requires 2 wires."
        return qml.CNOT(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CX gate requires 2 qubits."
        return f"cx q[{qubits[0]}], q[{qubits[1]}];"


class CY(QubitGate):
    """Controlled-Y gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]])

    def to_qiskit(self) -> qiskit.circuit.library.CYGate:
        return qiskit.circuit.library.CYGate()

    def to_pennylane(self, wires: list[int]) -> qml.CY:
        assert len(wires) == 2, "PennyLane CY gate requires 2 wires."
        return qml.CY(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CY gate requires 2 qubits."
        return f"cy q[{qubits[0]}], q[{qubits[1]}];"


class CZ(QubitGate):
    """Controlled-Z gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])

    def to_qiskit(self) -> qiskit.circuit.library.CZGate:
        return qiskit.circuit.library.CZGate()

    def to_pennylane(self, wires: list[int]) -> qml.CZ:
        assert len(wires) == 2, "PennyLane CZ gate requires 2 wires."
        return qml.CZ(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CZ gate requires 2 qubits."
        return f"cz q[{qubits[0]}], q[{qubits[1]}];"


class CH(QubitGate):
    """Controlled-Hadamard gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1 / np.sqrt(2), 1 / np.sqrt(2)], [0, 0, 1 / np.sqrt(2), -1 / np.sqrt(2)]])

    def to_qiskit(self) -> qiskit.circuit.library.CHGate:
        return qiskit.circuit.library.CHGate()

    def to_pennylane(self, wires: list[int]) -> qml.CH:
        assert len(wires) == 2, "PennyLane CH gate requires 2 wires."
        return qml.CH(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CH gate requires 2 qubits."
        return f"ch q[{qubits[0]}], q[{qubits[1]}];"


class CPhase(QubitGate):
    """General controlled phase shift gate.
    :param phi: The phase shift angle in radians.
    """

    def __new__(cls, phi: float):
        obj = super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp(1j * phi)]])
        obj.phi = phi
        return obj

    def to_qiskit(self) -> qiskit.circuit.library.CPhaseGate:
        return qiskit.circuit.library.CPhaseGate(self.phi)

    def to_pennylane(self, wires: list[int]) -> qml.CPhase:
        assert len(wires) == 2, "PennyLane CPhase gate requires 2 wires."
        return qml.CPhase(phi=self.phi, wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CPhase gate requires 2 qubits."
        return f"cp({self.phi}) q[{qubits[0]}], q[{qubits[1]}];"


class CS(CPhase):
    """Controlled-S gate."""

    def __new__(cls):
        phi = np.pi / 2
        return super().__new__(cls, phi=phi)

    def to_qiskit(self) -> qiskit.circuit.library.CSGate:
        return qiskit.circuit.library.CSGate()


class CT(CPhase):
    """Controlled-T gate."""

    def __new__(cls):
        phi = np.pi / 4
        return super().__new__(cls, phi=phi)

    def to_qiskit(self) -> qiskit.circuit.library.TGate:
        return qiskit.circuit.library.TGate().control(1)


class SWAP(QubitGate):
    """Swap gate. Swaps the states of two qubits."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])

    def to_qiskit(self) -> qiskit.circuit.library.SwapGate:
        return qiskit.circuit.library.SwapGate()

    def to_pennylane(self, wires: list[int]) -> qml.SWAP:
        assert len(wires) == 2, "PennyLane SWAP gate requires 2 wires."
        return qml.SWAP(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM SWAP gate requires 2 qubits."
        return f"swap q[{qubits[0]}], q[{qubits[1]}];"


class CSwap(QubitGate):
    """A controlled-SWAP gate. Also known as the Fredkin gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1]])

    def to_qiskit(self) -> qiskit.circuit.library.CSwapGate:
        return qiskit.circuit.library.CSwapGate()

    def to_pennylane(self, wires: list[int]) -> qml.CSWAP:
        return qml.CSWAP(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 3, "OpenQASM CSWAP gate requires 3 qubits."
        return f"cswap q[{qubits[0]}], q[{qubits[1]}], q[{qubits[2]}];"


class CCX(QubitGate):
    """A 3-qubit controlled-controlled-X (CCX) gate. Also known as the Toffoli gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0]])

    def to_qiskit(self) -> qiskit.circuit.library.CCXGate:
        return qiskit.circuit.library.CCXGate()

    def to_pennylane(self, wires: list[int]) -> qml.Toffoli:
        return qml.Toffoli(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 3, "OpenQASM CCX (Toffoli) gate requires 3 qubits."
        return f"ccx q[{qubits[0]}], q[{qubits[1]}], q[{qubits[2]}];"


class CCY(QubitGate):
    """A 3-qubit controlled-controlled-Y (CCY) gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, -1j], [0, 0, 0, 0, 0, 0, 1j, 0]])

    def to_qiskit(self) -> qiskit.circuit.library.YGate:
        # There is no native CCY gate in Qiskit so we construct it.
        return qiskit.circuit.library.YGate().control(2)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 3, "OpenQASM CCY gate requires 3 qubits."
        # Custom OpenQASM implementation
        # sdg is an inverse s gate
        return f"""sdg q[{qubits[2]}];\ncx q[{qubits[1]}], q[{qubits[2]}];\ns q[{qubits[2]}];\ncx q[{qubits[0]}], q[{qubits[2]}];\nsdg q[{qubits[2]}];\ncx q[{qubits[1]}], q[{qubits[2]}];\ns q[{qubits[2]}];\ny q[{qubits[2]}];"""


class CCZ(QubitGate):
    """A 3-qubit controlled-controlled-Z (CCZ) gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, -1]])

    def to_qiskit(self) -> qiskit.circuit.library.CCZGate:
        return qiskit.circuit.library.CCZGate()

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 3, "OpenQASM CCZ gate requires 3 qubits."
        # CCZ = CCX sandwiched between two H gates on last qubit.
        return f"""h q[{qubits[2]}];\nccx q[{qubits[0]}], q[{qubits[1]}], q[{qubits[2]}];\nh q[{qubits[2]}];"""


class MCX(QubitGate):
    """
    Multi controlled-X (MCX) gate.
    :param num_ctrl_qubits: Number of control qubits.
    """

    def __new__(cls, num_ctrl_qubits: int):
        assert num_ctrl_qubits >= 1, "MCX gate must have at least one control qubit."
        cls.num_ctrl_qubits = num_ctrl_qubits
        levels = 2 ** (num_ctrl_qubits + 1)
        gate = np.identity(levels)
        gate[-2:, -2:] = X()
        return super().__new__(cls, gate)

    def to_qiskit(self) -> qiskit.circuit.library.CXGate | qiskit.circuit.library.CCXGate | qiskit.circuit.library.C3XGate | qiskit.circuit.library.C4XGate | qiskit.circuit.library.MCXGate:
        if self.num_ctrl_qubits == 1:
            return qiskit.circuit.library.CXGate()
        elif self.num_ctrl_qubits == 2:
            return qiskit.circuit.library.CCXGate()
        elif self.num_ctrl_qubits == 3:
            return qiskit.circuit.library.C3XGate()
        elif self.num_ctrl_qubits == 4:
            return qiskit.circuit.library.C4XGate()
        else:
            return qiskit.circuit.library.MCXGate(num_ctrl_qubits=self.num_ctrl_qubits)

    def to_pennylane(self, wires: list[int]) -> qml.CNOT | qml.QubitUnitary:
        if self.num_ctrl_qubits == 1:
            return qml.CNOT(wires=wires)
        else:
            return super().to_pennylane(wires)


class MCY(QubitGate):
    """Multi controlled-Y (MCY) gate."""

    def __new__(cls, num_ctrl_qubits: int):
        assert num_ctrl_qubits >= 1, "MCY gate must have at least one control qubit."
        cls.num_ctrl_qubits = num_ctrl_qubits
        levels = 2 ** (num_ctrl_qubits + 1)
        gate = np.identity(levels)
        gate[-2:, -2:] = Y()
        return super().__new__(cls, gate)

    def to_qiskit(self) -> qiskit.circuit.library.YGate:
        return qiskit.circuit.library.YGate().control(self.num_ctrl_qubits)

    def to_pennylane(self, wires: list[int]) -> qml.CY | qml.QubitUnitary:
        if self.num_ctrl_qubits == 1:
            return qml.CY(wires=wires)
        else:
            return super().to_pennylane(wires)


class MCZ(QubitGate):
    """Multi controlled-Z (MCZ) gate."""

    def __new__(cls, num_ctrl_qubits: int):
        assert num_ctrl_qubits >= 1, "MCZ gate must have at least one control qubit."
        cls.num_ctrl_qubits = num_ctrl_qubits
        levels = 2 ** (num_ctrl_qubits + 1)
        gate = np.identity(levels)
        gate[-2:, -2:] = Z()
        return super().__new__(cls, gate)

    def to_qiskit(self) -> qiskit.circuit.library.ZGate:
        return qiskit.circuit.library.ZGate().control(self.num_ctrl_qubits)

    def to_pennylane(self, wires: list[int]) -> qml.CZ | qml.QubitUnitary:
        if self.num_ctrl_qubits == 1:
            return qml.CZ(wires=wires)
        else:
            return super().to_pennylane(wires)


class CR(QubitGate):
    """Simple Cross-Resonance gate."""

    def __new__(cls, theta: float):
        return super().__new__(cls, [[1, 0, 0, 0], [0, np.cos(theta), 0, -1j * np.sin(theta)], [0, 0, 1, 0], [0, -1j * np.sin(theta), 0, np.cos(theta)]])


class SymmetricECR(QubitGate):
    """Symmetric Echoed Cross-Resonance gate."""

    def __new__(cls, theta: float):
        return super().__new__(cls, CR(theta) @ CR(-theta))


class AsymmetricECR(QubitGate):
    """Asymmetric Echoed Cross-Resonance gate."""

    def __new__(cls, theta1: float, theta2: float):
        return super().__new__(cls, CR(theta1) @ CR(theta2))


class CU(QubitGate):
    """
    General Controlled-Unitary gate.
    Applies a unitary operation conditionally based on a control qubit.
    If the control qubit is |1>, the unitary is applied to the target qubit(s).
    Only use this for custom unitaries. Else use standard controlled gates like CX, CY, CZ, CH, CS, CT, CPhase, etc.

    :param unitary: The unitary gate to be controlled. Must be a QubitGate.
    """

    def __new__(cls, unitary: QubitGate):
        assert isinstance(unitary, QubitGate), "Input must be a QubitGate"

        n_target_qubits = unitary.num_qubits
        dim = 2 ** (n_target_qubits + 1)
        matrix = np.eye(dim, dtype=complex)
        block_size = 2**n_target_qubits
        matrix[block_size:, block_size:] = unitary
        obj = super().__new__(cls, matrix)
        obj.unitary = unitary
        obj.n_target_qubits = n_target_qubits
        return obj

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        try:
            base_gate = self.unitary.to_qiskit()
            return base_gate.control(1)
        except (AttributeError, TypeError, ValueError):
            return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label=f"c-{self.unitary.__class__.__name__}")

    def to_pennylane(self, wires: list[int]) -> qml.QubitUnitary:
        """Convert to a PennyLane controlled gate."""
        assert len(wires) == self.num_qubits, f"PennyLane CU gate requires {self.num_qubits} wires."
        return qml.QubitUnitary(self, wires=wires)


class MCU(QubitGate):
    """
    Multi-Controlled Unitary gate.
    Applies a unitary operation conditionally based on multiple control qubits.
    The unitary is applied to target qubit(s) only if all control qubits are |1>.
    Only use this for custom unitaries. Else use standard controlled gates like CX, CY, CZ, CH, CS, CT, CPhase, etc.


    :param unitary: The unitary gate to be controlled. Must be a QubitGate.
    :param num_ctrl_qubits: Number of control qubits.
    """

    def __new__(cls, unitary: QubitGate, num_ctrl_qubits: int):
        assert isinstance(unitary, QubitGate), "Input must be a QubitGate"
        assert num_ctrl_qubits >= 1, "MCU gate must have at least one control qubit."
        n_target_qubits = unitary.num_qubits
        total_qubits = n_target_qubits + num_ctrl_qubits
        dim = 2**total_qubits
        matrix = np.eye(dim, dtype=complex)
        unitary_size = 2**n_target_qubits
        start_idx = dim - unitary_size
        matrix[start_idx:, start_idx:] = unitary

        obj = super().__new__(cls, matrix)
        obj.unitary = unitary
        obj.num_ctrl_qubits = num_ctrl_qubits
        obj.n_target_qubits = n_target_qubits
        return obj

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        """Convert to a Qiskit controlled gate."""
        try:
            base_gate = self.unitary.to_qiskit()
            return base_gate.control(self.num_ctrl_qubits)
        except (AttributeError, TypeError, ValueError):
            return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label=f"mc-{self.unitary.__class__.__name__}")

    def to_pennylane(self, wires: list[int]) -> qml.QubitUnitary:
        """Convert to a PennyLane multi-controlled gate."""
        assert len(wires) == self.num_qubits, f"PennyLane MCU gate requires {self.num_qubits} wires."
        return qml.QubitUnitary(self, wires=wires)
