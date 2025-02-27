"""
This module contains helper functions for the qesem module.
"""
import re

import qiskit.providers.backend

from qesem import models


def _embed_observable(
    observable: models.Observable, qubit_map: dict[int, int]
) -> models.Observable:
    new_observable = {}
    for k, v in observable.root.items():
        old_terms = [(op, int(s)) for op, s in re.findall(r"([XYZ])(\d+)", k)]
        new_observable[",".join([o + str(qubit_map[q]) for o, q in old_terms])] = v
    return models.Observable(new_observable)


def adapt_to_backend(  # type: ignore[no-any-unimported]
    circ: qiskit.QuantumCircuit,
    observables: list[models.Observable],
    *,
    backend: qiskit.providers.backend.BackendV2,
) -> tuple[qiskit.QuantumCircuit, list[models.Observable]]:
    """
    Adapt a circuit and observables to a backend qubits layout and basis gates.

    Useful for running with QESEM and transpilation level 0.
    """
    cm = [list(e) for e in backend.coupling_map]
    cm = cm + [e[::-1] for e in cm]
    transpiled_circ = qiskit.transpile(
        circ, optimization_level=1, coupling_map=cm, basis_gates=backend.operation_names
    )
    qmap = dict(enumerate(transpiled_circ.layout.final_index_layout()))
    transpiled_observables = [_embed_observable(o, qmap) for o in observables]

    return transpiled_circ, transpiled_observables
