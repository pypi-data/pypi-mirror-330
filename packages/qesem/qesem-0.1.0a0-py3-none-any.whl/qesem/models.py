"""Qedma Public API"""
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
import contextlib
import datetime
import enum
import re
from collections.abc import Generator
from typing import Annotated, Literal

import loguru
import pydantic
import qiskit.qasm3
from typing_extensions import NotRequired, TypedDict


logger = loguru.logger


class RequestBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=False,
    )


class ResponseBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        extra="ignore",
        validate_assignment=True,
        arbitrary_types_allowed=False,
    )


class JobStatus(str, enum.Enum):
    ESTIMATING = "ESTIMATING"
    ESTIMATED = "ESTIMATED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

    def __str__(self) -> str:
        return self.value


class TranspilationLevel(enum.IntEnum):
    LEVEL_0 = 0
    LEVEL_1 = 1


class IBMQProvider(RequestBase):
    name: Literal["ibmq"] = "ibmq"
    token_ref: str
    instance: str  # hub/group/project
    channel: str = "ibm_quantum"


_PAULI_STRING_REGEX_STR = "^[XYZ][0-9]+(,[XYZ][0-9]+)*$"
Pauli = Annotated[str, pydantic.Field(pattern=_PAULI_STRING_REGEX_STR)]


class Observable(pydantic.RootModel[dict[Pauli, float]]):
    def __iter__(self) -> Generator[Pauli, None, None]:  # type: ignore[override]
        # pydantic suggests to override __iter__ method (
        # https://docs.pydantic.dev/latest/concepts/models/#rootmodel-and-custom-root-types)
        # but __iter__ method is already implemented in pydantic.BaseModel, so we just ignore the
        # warning and hope that it works as expected (tests covers dump/load methods and iter)
        yield from iter(self.root)

    def __getitem__(self, key: Pauli) -> float:
        return self.root[key]

    def __contains__(self, key: Pauli) -> bool:
        return key in self.root

    def __len__(self) -> int:
        return len(self.root)

    def __str__(self) -> str:
        return str(self.root)

    def __repr__(self) -> str:
        return "Observable(" + repr(self.root) + ")"


class ExpectationValue(ResponseBase):
    """Expectation value of an observable"""

    value: float
    error_bar: float

    def __str__(self) -> str:
        return f"{self.value} ± {self.error_bar}"


class ExpectationValues(pydantic.RootModel[list[tuple[Observable, ExpectationValue]]]):
    def __iter__(self) -> Generator[tuple[Observable, ExpectationValue], None, None]:  # type: ignore[override] # pylint: disable=line-too-long
        # pydantic suggests to override __iter__ method (
        # https://docs.pydantic.dev/latest/concepts/models/#rootmodel-and-custom-root-types)
        # but __iter__ method is already implemented in pydantic.BaseModel, so we just ignore the
        # warning and hope that it works as expected (tests covers dump/load methods and iter)
        yield from iter(self.root)

    def __getitem__(self, key: int) -> tuple[Observable, ExpectationValue]:
        return self.root[key]

    def __len__(self) -> int:
        return len(self.root)

    def __str__(self) -> str:
        return "[" + ", ".join([f"{obs}: ({exp})" for obs, exp in self.root]) + "]"

    def __repr__(self) -> str:
        return (
            "ExpectationValues(["
            + ",".join([f"{repr(obs)}: {repr(exp)}" for obs, exp in self.root])
            + "])"
        )


class PrecisionMode(str, enum.Enum):
    """The mode of execution."""

    JOB = "JOB"
    CIRCUIT = "CIRCUIT"

    def __str__(self) -> str:
        return self.value


class ExecutionMode(str, enum.Enum):
    """The mode of execution."""

    SESSION = "SESSION"
    BATCH = "BATCH"

    def __str__(self) -> str:
        return self.value


class JobOptions(RequestBase):
    """Additional options for a job request"""

    execution_mode: ExecutionMode | None = None


class CircuitOptions(RequestBase):
    """Qesem circuits circuit_options"""

    transpilation_level: TranspilationLevel = pydantic.Field(default=TranspilationLevel.LEVEL_1)


class Circuit(RequestBase):  # type: ignore[no-any-unimported]
    """Circuit to be executed on QPU"""

    circuit: qiskit.QuantumCircuit  # type: ignore[no-any-unimported]
    observables: tuple[Observable, ...]
    parameters: dict[str, tuple[float, ...]] | None = None
    precision: float
    options: CircuitOptions

    @pydantic.field_validator("circuit", mode="plain", json_schema_input_type=str)
    @classmethod
    def check_circuit(cls, value: qiskit.QuantumCircuit | str) -> qiskit.QuantumCircuit:  # type: ignore[no-any-unimported] # pylint: disable=line-too-long
        if isinstance(value, str):
            with contextlib.suppress(Exception):
                value = qiskit.qasm3.loads(value)

        if isinstance(value, str):
            with contextlib.suppress(Exception):
                value = qiskit.QuantumCircuit.from_qasm_str(value)

        if not isinstance(value, qiskit.QuantumCircuit):
            raise ValueError("Circuit must be a valid Qiskit QuantumCircuit or QASM string")

        return value

    @pydantic.field_serializer("circuit", mode="plain", return_type=str)
    def serialize_circuit(self, value: qiskit.QuantumCircuit) -> str:  # type: ignore[no-any-unimported] # pylint: disable=line-too-long
        result = qiskit.qasm3.dumps(value)
        if not isinstance(result, str):
            raise ValueError("Failed to serialize the circuit")

        return result

    @pydantic.model_validator(mode="after")
    def check_parameters(self) -> "Circuit":
        if self.parameters is None:
            if len(set(map(str, self.circuit.parameters))) > 0:
                raise ValueError("Parameters must match the circuit parameters")
            return self

        if set(map(str, self.parameters.keys())) != set(map(str, self.circuit.parameters)):
            raise ValueError("Parameters must match the circuit parameters")

        if len(self.parameters) > 0:
            if any(
                re.search(r"[^\w\d]", p, flags=re.U)
                for p in self.parameters  # pylint: disable=not-an-iterable
            ):
                raise ValueError(
                    "Parameter names must contain only alphanumeric characters, got: "
                    f"{list(self.parameters.keys())}"
                )

            # check all parameters are of the same length
            parameter_value_lengths = set(len(v) for v in self.parameters.values())
            if len(parameter_value_lengths) > 1:
                raise ValueError("All parameter values must have the same length")

            # check that the number of observables is equal to the number of parameters values
            if len(self.observables) != list(parameter_value_lengths)[0]:
                raise ValueError(
                    "Number of observables must be equal to the number of parameter values"
                )

        return self


class QPUTime(TypedDict):
    execution: datetime.timedelta
    estimation: NotRequired[datetime.timedelta]


class JobDetails(ResponseBase):
    account_id: str
    job_id: str
    description: str = ""
    masked_account_token: str
    masked_qpu_token: str
    qpu_name: str
    circuit: Circuit | None = None
    precision_mode: PrecisionMode | None = None
    status: JobStatus
    analytical_qpu_time_estimation: datetime.timedelta | None
    empirical_qpu_time_estimation: datetime.timedelta | None = None
    total_execution_time: datetime.timedelta
    created_at: datetime.datetime
    updated_at: datetime.datetime
    qpu_time: QPUTime
    qpu_time_limit: datetime.timedelta | None = None
    warnings: list[str] | None = None
    errors: list[str] | None = None
    intermediate_results: ExpectationValues | None = None
    results: ExpectationValues | None = None
    noisy_results: ExpectationValues | None = None
