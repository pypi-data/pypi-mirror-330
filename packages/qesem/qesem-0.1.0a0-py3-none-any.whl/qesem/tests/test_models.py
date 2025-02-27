# pylint: disable=missing-function-docstring,missing-class-docstring,missing-module-docstring
import datetime
import json

import pytest
import qiskit.circuit
import qiskit.qasm2
import qiskit.qasm3

from qedma_api import models


class TestModels:
    @pytest.mark.parametrize(
        argnames=("invalid_observable",),
        argvalues=[
            ({"X0,a": 1.0, "Y1": 2.0, "Z2": 3.0},),
            ({"X0_a": 1.0, "Y1": 2.0, "Z2": 3.0},),
            ({"X0cfgdhfgh45464": 1.0},),
            ({"X0": 1.0, "W2": 1.0},),
        ],
    )
    def test_invalid_observables_validation(self, invalid_observable: dict[str, float]) -> None:
        with pytest.raises(ValueError):
            models.Observable(root=invalid_observable)

    @pytest.mark.parametrize(
        argnames=("valid_observable",),
        argvalues=[
            ({"X0": 1.0},),
            ({"X0": 1.0, "Y1": 2.0},),
            ({"X0": 1.0, "Y1": 2.0, "Z2": 3.0},),
            ({"X0,Y1,Z32": 1.0},),
        ],
    )
    def test_valid_observables_validation(self, valid_observable: dict[str, float]) -> None:
        models.Observable(root=valid_observable)

    def test_observable_dump_load(self) -> None:
        observable = models.Observable(root={"X0": 1.0, "Y1": 2.0, "Z2": 3.0})
        assert models.Observable.model_validate_json(observable.model_dump_json()) == observable

    def test_expectation_value_dump_load(self) -> None:
        expectation_value = models.ExpectationValue(value=0.43120, error_bar=0.1)
        assert (
            models.ExpectationValue.model_validate_json(expectation_value.model_dump_json())
            == expectation_value
        )

    def test_expectation_values_dump_load(self) -> None:
        expectation_values = models.ExpectationValues(
            [
                (
                    models.Observable({"X0": 1.0}),
                    models.ExpectationValue(value=0.3420, error_bar=0.1),
                ),
                (
                    models.Observable({"Y1": 2.0}),
                    models.ExpectationValue(value=0.021, error_bar=0.1),
                ),
                (
                    models.Observable({"Z2": 3.0}),
                    models.ExpectationValue(value=0.03, error_bar=0.1),
                ),
            ]
        )
        assert (
            models.ExpectationValues.model_validate_json(expectation_values.model_dump_json())
            == expectation_values
        )

    def test_job_details_dump_load(self) -> None:
        job_details = models.JobDetails(
            account_id="1234",
            masked_account_token="****",
            masked_qpu_token="****",
            total_execution_time=datetime.timedelta(seconds=10),
            job_id="1234",
            status=models.JobStatus.RUNNING,
            circuit=None,
            results=models.ExpectationValues(
                [
                    (
                        models.Observable({"X0": 1.0}),
                        models.ExpectationValue(value=0.3420, error_bar=0.1),
                    ),
                    (
                        models.Observable({"Y1": 2.0}),
                        models.ExpectationValue(value=0.021, error_bar=0.1),
                    ),
                    (
                        models.Observable({"Z2": 3.0}),
                        models.ExpectationValue(value=0.03, error_bar=0.1),
                    ),
                ]
            ),
            qpu_name="ibmq_qasm_simulator",
            analytical_qpu_time_estimation=datetime.timedelta(seconds=10),
            empirical_qpu_time_estimation=datetime.timedelta(seconds=20),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            qpu_time={
                "execution": datetime.timedelta(seconds=10),
                "estimation": datetime.timedelta(seconds=2),
            },
        )
        assert models.JobDetails.model_validate_json(job_details.model_dump_json()) == job_details

    def test_iter_observable(self) -> None:
        observable = models.Observable(root={"X0": 1.0, "Y1": 2.0, "Z2": 3.0})
        assert list(observable) == ["X0", "Y1", "Z2"]
        assert observable["X0"] == 1.0
        assert observable["Y1"] == 2.0
        assert len(observable) == 3
        assert "X0" in observable

    def test_iter_expectation_values(self) -> None:
        expectation_values = models.ExpectationValues(
            root=[
                (
                    models.Observable(root={"X0": 1.0}),
                    models.ExpectationValue(value=0.0, error_bar=0.1),
                ),
                (
                    models.Observable(root={"Y1": 2.0}),
                    models.ExpectationValue(value=0.0, error_bar=0.1),
                ),
                (
                    models.Observable(root={"Z2": 3.0}),
                    models.ExpectationValue(value=0.0, error_bar=0.1),
                ),
            ]
        )
        assert list(expectation_values) == [
            (
                models.Observable(root={"X0": 1.0}),
                models.ExpectationValue(value=0.0, error_bar=0.1),
            ),
            (
                models.Observable(root={"Y1": 2.0}),
                models.ExpectationValue(value=0.0, error_bar=0.1),
            ),
            (
                models.Observable(root={"Z2": 3.0}),
                models.ExpectationValue(value=0.0, error_bar=0.1),
            ),
        ]
        assert len(expectation_values) == 3
        assert expectation_values[0] == (
            models.Observable(root={"X0": 1.0}),
            models.ExpectationValue(value=0.0, error_bar=0.1),
        )
        assert expectation_values[1] == (
            models.Observable(root={"Y1": 2.0}),
            models.ExpectationValue(value=0.0, error_bar=0.1),
        )
        assert expectation_values[2] == (
            models.Observable(root={"Z2": 3.0}),
            models.ExpectationValue(value=0.0, error_bar=0.1),
        )

    def test_wrong_parameters_raises(self) -> None:
        valid_job_options = models.JobOptions(execution_mode=models.ExecutionMode.SESSION)
        assert valid_job_options.execution_mode == models.ExecutionMode.SESSION
        with pytest.raises(ValueError):
            # type mismatch
            models.JobOptions(execution_mode=1)  # type: ignore[arg-type] # for the test
        with pytest.raises(ValueError):
            # implicit type mismatch
            models.JobOptions(execution_mode="WRONG")  # type: ignore[arg-type] # for the test
        with pytest.raises(ValueError):
            # wrong name
            models.JobOptions(
                ExecutionMode=models.ExecutionMode.SESSION,  # type: ignore[call-arg] # for the test
            )
        with pytest.raises(ValueError):
            # extra parameter
            models.JobOptions(
                execution_mode=models.ExecutionMode.SESSION,
                extra_param=1,  # type: ignore[call-arg] # for the test
            )

    def test_extra_details_in_response(self) -> None:
        job_details = models.JobDetails(
            account_id="1234",
            masked_account_token="****",
            masked_qpu_token="****",
            total_execution_time=datetime.timedelta(seconds=10),
            job_id="1234",
            status=models.JobStatus.RUNNING,
            circuit=None,
            results=models.ExpectationValues(
                [
                    (
                        models.Observable({"X0": 1.0}),
                        models.ExpectationValue(value=0.3420, error_bar=0.1),
                    ),
                    (
                        models.Observable({"Y1": 2.0}),
                        models.ExpectationValue(value=0.021, error_bar=0.1),
                    ),
                    (
                        models.Observable({"Z2": 3.0}),
                        models.ExpectationValue(value=0.03, error_bar=0.1),
                    ),
                ]
            ),
            qpu_name="ibmq_qasm_simulator",
            analytical_qpu_time_estimation=datetime.timedelta(seconds=10),
            empirical_qpu_time_estimation=datetime.timedelta(seconds=20),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            qpu_time={
                "execution": datetime.timedelta(seconds=10),
                "estimation": datetime.timedelta(seconds=2),
            },
        )

        job_details_with_extra = models.JobDetails(  # type: ignore[call-arg] # for the test
            **job_details.model_dump(), extra_field_unknown="extra"
        )
        assert set(job_details_with_extra.model_dump().keys()) == set(
            job_details.model_dump().keys()
        )

    @pytest.mark.parametrize(
        "mode",
        ["qasm2", "qasm3", "qiskit"],
    )
    def test_valid_circuit(self, mode: str) -> None:
        qcirc = qiskit.QuantumCircuit(2)
        if mode != "qasm2":
            qcirc.rz(qiskit.circuit.Parameter("param"), 0)
            qcirc.rx(qiskit.circuit.Parameter("param2"), 0)
            qcirc.rx(qiskit.circuit.Parameter("θ"), 1)
        qcirc.cx(1, 0)

        if mode == "qasm2":
            ser_circ = qiskit.qasm2.dumps(qcirc)
        elif mode == "qasm3":
            ser_circ = qiskit.qasm3.dumps(qcirc)
        else:
            ser_circ = qcirc

        circ = models.Circuit(
            circuit=ser_circ,
            observables=(
                models.Observable(root={"X0": 1.0}),
                models.Observable(root={"X0": 2.0}),
            ),
            parameters={"param": (1.0, 2.0), "param2": (1.0, 2.0), "θ": (4, 6.0)}
            if mode != "qasm2"
            else None,
            precision=0.1,
            options=models.CircuitOptions(),
        )
        assert json.loads(circ.model_dump_json())["circuit"] == qiskit.qasm3.dumps(qcirc)

    @pytest.mark.parametrize(
        ["num_observables", "parameters"],
        [
            (2, {"param": (1.0, 2.0, 3.0)}),
            (3, {"param": (1.0, 2.0)}),
            (2, {"param": (1.0, 2.0), "param2": (3.0,)}),
            (2, {"param": (1.0, 2.0), "param2": (3.0,), "param3": (4.0, 5.0)}),
            (2, {"param": (1.0, 2.0), "param2": (4.0, 5.0, 6.0)}),
            (2, {"param": (1.0, 2.0), qiskit.circuit.Parameter("param3"): (4.0, 5.0, 6.0)}),
            (2, {"x[0]": (1.0, 2.0), "param2": (4.0, 5.0)}),
        ],
        ids=[
            "too_many_values",
            "too_few_values",
            "parameters_have_different_lengths",
            "parameters_have_different_lengths_2",
            "parameters_have_different_lengths_3",
            "parameters_have_different_lengths_qiskit_param",
            "invalid_param_name",
        ],
    )
    def test_invalid_circuit(
        self, num_observables: int, parameters: dict[str, tuple[float, ...]]
    ) -> None:
        circ = qiskit.QuantumCircuit(2)
        for p in parameters:
            circ.rz(qiskit.circuit.Parameter(p) if isinstance(p, str) else p, 0)
        circ.cx(1, 0)

        with pytest.raises(ValueError):
            models.Circuit(
                circuit=circ,
                observables=(models.Observable(root={"X0": 1.0}),) * num_observables,
                parameters=parameters,
                precision=0.1,
                options=models.CircuitOptions(),
            )
