from typing import Callable

from ..gates.qubit.multi import DeutschOracle, DeutschJozsaOracle
from ..gates.qubit.single import I, X, H, Measure
from .circuit import Circuit, Concat


class Deutsch:
    """Deutsch's algorithm."""

    def circuit(self, f: Callable, measure: bool = True) -> Circuit:
        """
        Deutsch's algorithm
        :param f: Binary function that maps a single bit to a single bit.
        :param measure: Whether to measure the qubits.
        :return: skq Circuit that implements Deutsch's algorithm.
        """
        circuit = [
            Concat([I(), X()]),
            Concat([H(), H()]),
            DeutschOracle(f),
            Concat([H(), I()]),
        ]
        if measure:
            circuit.append(Measure())
        return Circuit(circuit)


class DeutschJozsa:
    """Deutsch-Jozsa algorithm."""

    def circuit(self, f: Callable, n_bits: int, measure: bool = True) -> Circuit:
        """
        Deutsch-Josza algorithm
        :param f: Binary function that maps a single bit to a single bit.
        :return: skq Circuit that implements Deutsch-Josza algorithm.
        """
        circuit = [
            Concat([I() for _ in range(n_bits - 1)] + [X()]),
            Concat([H() for _ in range(n_bits)]),
            DeutschJozsaOracle(f, n_bits=n_bits),
            Concat([H() for _ in range(n_bits)]),
        ]
        if measure:
            circuit.append(Measure())
        return Circuit(circuit)
