"""Qedma Public API"""
import datetime
import json
import math
import os
import time
from collections.abc import Mapping, Sequence
from typing import overload

import loguru
import pydantic
import qiskit
import requests
from typing_extensions import Self

from qedma_api import models


POLLING_INTERVAL = datetime.timedelta(seconds=10)
logger = loguru.logger


class JobRequest(models.RequestBase):
    """Request to create a new job"""

    circuit: models.Circuit
    provider: models.IBMQProvider
    backend: str
    empirical_time_estimation: bool
    precision_mode: models.PrecisionMode | None = None
    description: str = ""

    @pydantic.model_validator(mode="after")
    def validate_precision_mode(self) -> Self:
        """Validates the precision mode."""
        if (self.circuit.parameters is None) != (self.precision_mode is None):
            raise ValueError("Parameters and precision mode must be both set or unset")
        return self


class StartJobRequest(models.RequestBase):
    """Start a job."""

    max_qpu_time: datetime.timedelta
    options: models.JobOptions


class GetJobsDetailsResponse(models.ResponseBase):
    """An internal object."""

    jobs: list[models.JobDetails]


class RegisterQpuTokenRequest(models.RequestBase):
    """Store qpu token request model"""

    qpu_token: str


class RegisterQpuTokenResponse(models.ResponseBase):
    """Store qpu token request model"""

    qpu_token_ref: str


class DecomposeResponse(models.ResponseBase):
    """Decompose response model"""

    parametrized_circ: str
    meas_params: dict[str, list[float]]
    obs_per_basis: list[models.Observable]
    relative_l2_trunc_err: float


class QedmaServerError(Exception):
    """An exception raised when the server returns an error."""

    def __init__(self, message: str, details: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        if self.details is None:
            return super().__str__()
        return f"{super().__str__()}. Details: {self.details}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message}, details={self.details})"


class ResultNotReadyError(QedmaServerError):
    """An exception raised when the server returns an error."""

    def __init__(self) -> None:
        super().__init__("Result is not ready yet")


ENDPOINT_URI = "https://api.qedma.io/v2/qesem"


class Client:
    """The QESEM client object"""

    def __init__(
        self,
        *,
        api_token: str | None = None,
        provider: models.IBMQProvider | None = None,
        uri: str = ENDPOINT_URI,
        timeout: int = 30,
    ) -> None:
        self.api_token = api_token
        self.provider = provider
        self.uri = uri
        self.timeout = timeout

    def set_provider(self, provider: models.IBMQProvider) -> None:
        """Set the provider of the client."""
        self.provider = provider

    @overload
    def create_job(  # type: ignore[no-any-unimported]  # pylint: disable=too-many-arguments
        self,
        *,
        circuit: qiskit.QuantumCircuit,
        observables: models.Observable | Sequence[models.Observable],
        parameters: None = None,
        precision: float,
        backend: str,
        empirical_time_estimation: bool = False,
        description: str = "",
        circuit_options: models.CircuitOptions | None = None,
        precision_mode: None = None,
    ) -> models.JobDetails:
        ...

    @overload
    def create_job(  # type: ignore[no-any-unimported]  # pylint: disable=too-many-arguments
        self,
        *,
        circuit: qiskit.QuantumCircuit,
        observables: models.Observable | Sequence[models.Observable],
        parameters: Mapping[str | qiskit.circuit.Parameter, Sequence[float]],
        precision: float,
        backend: str,
        empirical_time_estimation: bool = False,
        description: str = "",
        circuit_options: models.CircuitOptions | None = None,
        precision_mode: models.PrecisionMode,
    ) -> models.JobDetails:
        ...

    def create_job(  # type: ignore[no-any-unimported]  # pylint: disable=too-many-arguments
        self,
        *,
        circuit: qiskit.QuantumCircuit,
        observables: models.Observable | Sequence[models.Observable],
        parameters: Mapping[str | qiskit.circuit.Parameter, Sequence[float]] | None = None,
        precision: float,
        backend: str,
        empirical_time_estimation: bool = False,
        description: str = "",
        circuit_options: models.CircuitOptions | None = None,
        precision_mode: models.PrecisionMode | None = None,
    ) -> models.JobDetails:
        """
        Submit a new job to the API Gateway.
        :param circuit: The circuit to run.
        :param parameters: The parameters to run the circuit with (mapping from parameter to
         sequence of values, all parameters must have the same number of values)
         If given, the number of observables must be equal to the number of values.
        :param observables: The observables to measure.
        :param precision: The precision to achieve.
        :param backend: The backend (QPU) to run on.
        :param empirical_time_estimation: Whether to use empirical time estimation (default: False).
        :param description: A description for the job (optional) .
        :param circuit_options: Additional options for a circuit (see `CircuitOptions`. Optional).
        :param precision_mode: The precision mode to use (optional). Can only be used when
         parameters are set.
        :return: The job's details including its ID.
        """

        if circuit_options is None:
            circuit_options = models.CircuitOptions()

        if self.provider is None:
            raise ValueError("Provider is not set")

        if isinstance(observables, models.Observable):
            observables = (observables,)

        logger.info("Submitting new job")
        response = requests.post(
            url=f"{self.uri}/job",
            data=JobRequest(
                circuit=models.Circuit(
                    circuit=circuit,
                    parameters={str(k): tuple(v) for k, v in parameters.items()}
                    if parameters is not None
                    else None,
                    observables=tuple(observables),
                    precision=precision,
                    options=circuit_options,
                ),
                provider=self.provider,
                empirical_time_estimation=empirical_time_estimation,
                backend=backend,
                description=description,
                precision_mode=precision_mode,
            ).model_dump_json(),
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=self.timeout,
        )

        _raise_for_status(response)

        resp = models.JobDetails.model_validate_json(response.content)

        logger.info("New job created. job_id: {job_id}", job_id=resp.job_id)

        _print_warnings_and_errors(resp)

        return resp

    def start_job(
        self,
        job_id: str,
        max_qpu_time: datetime.timedelta,
        options: models.JobOptions | None = None,
    ) -> None:
        """
        Start running an estimated job.
        :param job_id: The ID of the job.
        :param max_qpu_time: The maximum allowed time for running the QPU.
        :param options: Additional options for the job (see `JobOptions`. Optional).
        """
        if options is None:
            options = models.JobOptions()

        logger.info("Starting job. job_id: {job_id}", job_id=job_id)

        response = requests.post(
            url=f"{self.uri}/job/{job_id}/start",
            data=StartJobRequest(max_qpu_time=max_qpu_time, options=options).model_dump_json(),
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=self.timeout,
        )

        _raise_for_status(response)

    def _create_decompose_task(
        self,
        mpo_file: str,
        *,
        max_bases: int,
        l2_truncation_err: float,
        op_l2_norm: float,
        k: int,
        pauli_coeff_th: float,
    ) -> str:
        logger.info("Requesting decomposition of MPO")
        if not os.path.exists(mpo_file):
            raise FileNotFoundError(f"File {mpo_file} not found")
        if not os.path.isfile(mpo_file):
            raise FileNotFoundError(f"File {mpo_file} is not a file")

        with open(mpo_file, "rb") as data_file:
            response = requests.post(
                url=f"{self.uri}/hpc/decompose",
                params=[
                    ("max_bases", max_bases),
                    ("l2_truncation_err", l2_truncation_err),
                    ("op_l2_norm", op_l2_norm),
                    ("k", k),
                    ("pauli_coeff_th", pauli_coeff_th),
                ],
                files={"data_file": data_file},
                headers={"Authorization": f"Bearer {self.api_token}"},
                timeout=datetime.timedelta(minutes=5).total_seconds(),
            )

        if response.status_code == 404:
            raise QedmaServerError("API endpoint not enabled")

        _raise_for_status(response)

        resp_json = response.json()
        if "task_id" not in resp_json:
            raise QedmaServerError("Task ID not found in response", details=resp_json)

        task_id = resp_json["task_id"]
        if not isinstance(task_id, str):
            raise QedmaServerError("Invalid task ID in response", details=resp_json)

        return task_id

    def _get_decompose_task_result(self, task_id: str) -> DecomposeResponse:
        response = requests.get(
            url=f"{self.uri}/hpc/decompose/{task_id}",
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=60 * 5,
        )

        _raise_for_status(response)
        if response.status_code == 202:
            raise ResultNotReadyError()

        return DecomposeResponse.model_validate_json(response.content)

    def decompose(
        self,
        mpo_file: str,
        *,
        max_bases: int,
        l2_truncation_err: float = 1e-12,
        observable: models.Observable,
        k: int = 1000,
        pauli_coeff_th: float = 1e-8,
        timeout: datetime.timedelta = datetime.timedelta(minutes=60),
    ) -> DecomposeResponse:
        """
        Decompose an MPO into circuits and observables to measure
        """

        op_l2_norm = math.sqrt(sum(coeff**2 for p, coeff in observable.root.items()))

        task_id = self._create_decompose_task(
            mpo_file,
            max_bases=max_bases,
            l2_truncation_err=l2_truncation_err,
            op_l2_norm=op_l2_norm,
            k=k,
            pauli_coeff_th=pauli_coeff_th,
        )
        logger.info("Decomposition task created. task_id: {task_id}", task_id=task_id)

        start = datetime.datetime.now()
        while datetime.datetime.now() - start < timeout:
            time.sleep(0.5)
            try:
                return self._get_decompose_task_result(task_id)
            except ResultNotReadyError:
                pass

        raise TimeoutError("Decomposition task timed out")

    def cancel_job(self, job_id: str) -> None:
        """Cancel a job."""
        logger.info("Canceling job. job_id: {job_id}", job_id=job_id)
        response = requests.post(
            url=f"{self.uri}/job/{job_id}/cancel",
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=self.timeout,
        )

        _raise_for_status(response)

    def get_job(
        self, job_id: str, include_circuits: bool = False, include_results: bool = False
    ) -> models.JobDetails:
        """
        Get a job's details.
        :param job_id: The ID of the job.
        :param include_circuits: Whether to include the input circuit. Defaults to False.
        :param include_results: Whether to include the result of the job (if it is ready). Defaults
         to False.
        :return: Details about the job, with the data from the flags.
        """
        job_details = self.get_jobs([job_id], include_circuits, include_results)[0]

        _print_warnings_and_errors(job_details)

        return job_details

    def get_jobs(
        self, jobs_ids: list[str], include_circuits: bool = False, include_results: bool = False
    ) -> list[models.JobDetails]:
        """
        Get multiple jobs' details.
        :param jobs_ids: The IDs of the jobs.
        :param include_circuits: Whether to include the input circuits. Defaults to False.
        :param include_results: Whether to include the results of the jobs (if they are ready).
         Defaults to False.
        :return: Details about the jobs, with the data from the flags.
        """
        logger.info("Querying jobs details. jobs_ids: {jobs_ids}", jobs_ids=jobs_ids)

        response = requests.get(
            url=f"{self.uri}/jobs",
            params=[
                ("ids", ",".join(jobs_ids)),
                ("include_circuits", include_circuits),
                ("include_results", include_results),
            ],
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=self.timeout,
        )

        _raise_for_status(response)

        return GetJobsDetailsResponse.model_validate_json(response.content).jobs

    def list_jobs(self, skip: int = 0, limit: int = 50) -> list[models.JobDetails]:
        """
        Get all jobs' details.
        :param skip: How many jobs to skip.
        :param limit: Maximum amount of jobs to return.
        :return: The list of requested jobs.
        """
        logger.info("Querying jobs details. skip: {skip}, limit: {limit}", skip=skip, limit=limit)

        response = requests.get(
            url=f"{self.uri}/jobs/list",
            params=[("skip", skip), ("limit", limit)],
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=self.timeout,
        )

        _raise_for_status(response)

        return GetJobsDetailsResponse.model_validate_json(response.content).jobs

    def register_qpu_token(self, token: str) -> str:
        """Stores a vendor token for an account."""

        response = requests.post(
            url=f"{self.uri}/qpu-token",
            data=RegisterQpuTokenRequest(qpu_token=token).model_dump_json(),
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=30,
        )

        _raise_for_status(response)

        return RegisterQpuTokenResponse.model_validate_json(response.content).qpu_token_ref

    def unregister_qpu_token(self, token_ref: str) -> None:
        """Unregisters a vendor token for an account."""

        response = requests.delete(
            url=f"{self.uri}/qpu-token/{token_ref}",
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=30,
        )

        _raise_for_status(response)

    def _wait_for_status(  # pylint: disable=too-many-arguments
        self,
        job_id: str,
        statuses: set[models.JobStatus],
        interval: datetime.timedelta,
        timeout: datetime.timedelta | None,
        *,
        include_circuits: bool = False,
        include_results: bool = False,
        log_intermediate_results: bool = False,
    ) -> models.JobDetails:
        job = self.get_job(job_id)
        start = datetime.datetime.now()
        intermediate_results = None
        while job.status not in statuses:
            if timeout is not None and datetime.datetime.now() - start < timeout:
                raise TimeoutError("The given time out passed!")

            time.sleep(interval.total_seconds())
            job = self.get_job(job_id, include_circuits, include_results)

            if log_intermediate_results and job.intermediate_results:
                if job.intermediate_results != intermediate_results:
                    intermediate_results = job.intermediate_results
                    logger.info(
                        "Intermediate results for job {job_id}: {results}",
                        job_id=job_id,
                        results=job.intermediate_results,
                    )

        return job

    def wait_for_time_estimation(
        self,
        job_id: str,
        *,
        interval: datetime.timedelta = POLLING_INTERVAL,
        max_poll_time: datetime.timedelta | None = None,
    ) -> datetime.timedelta | None:
        """
        Wait until a job reaches the time-estimation part, and get the estimation.

        :param job_id: The ID of the job.
        :param interval: The interval between two polls. Defaults to 10 seconds.
        :param max_poll_time: Max time until a timeout. Defaults to None.
        :return: The time estimation of the job.
        :raises: `TimeoutError` if max_poll_time passed.
        """
        job = self._wait_for_status(
            job_id,
            {
                models.JobStatus.ESTIMATED,
                models.JobStatus.RUNNING,
                models.JobStatus.SUCCEEDED,
                models.JobStatus.FAILED,
                models.JobStatus.CANCELLED,
            },
            interval,
            max_poll_time,
        )

        _print_warnings_and_errors(job)

        time_est = job.empirical_qpu_time_estimation
        if time_est is None:
            time_est = job.analytical_qpu_time_estimation

        return time_est

    def wait_for_job_complete(
        self,
        job_id: str,
        *,
        interval: datetime.timedelta = POLLING_INTERVAL,
        max_poll_time: datetime.timedelta | None = None,
    ) -> models.JobDetails:
        """
        Wait until the job finishes, and get the results.

        :param job_id: The ID of the job.
        :param interval: The interval between two polls. Defaults to 10 seconds.
        :param max_poll_time: Max time until a timeout. Defaults to None.
        :return: The details of the job, including its results.
        :raises: `TimeoutError` if max_poll_time passed.
        """
        job = self._wait_for_status(
            job_id,
            {
                models.JobStatus.SUCCEEDED,
                models.JobStatus.FAILED,
                models.JobStatus.CANCELLED,
            },
            interval,
            max_poll_time,
            include_results=True,
            log_intermediate_results=True,
        )

        return job


def _raise_for_status(response: requests.Response) -> None:
    http_error_msg = ""
    if isinstance(response.reason, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = response.reason.decode("utf-8")
        except UnicodeDecodeError:
            reason = response.reason.decode("iso-8859-1")
    else:
        reason = response.reason

    if 400 <= response.status_code < 500:
        http_error_msg = f"{response.status_code} Client Error: {reason} for url: {response.url}"

    elif 500 <= response.status_code < 600:
        http_error_msg = f"{response.status_code} Server Error: {reason} for url: {response.url}"

    if http_error_msg:
        if not response.content:
            raise QedmaServerError(http_error_msg)

        try:
            details = response.json().get("detail")
        except json.JSONDecodeError:
            raise QedmaServerError(http_error_msg)  # pylint: disable=raise-missing-from

        logger.error(
            "Qedma server error: {http_error_msg}. Details: {details}",
            http_error_msg=http_error_msg,
            details=details,
        )
        raise QedmaServerError(http_error_msg, details=details)


def _print_warnings_and_errors(job_details: models.JobDetails) -> None:
    if job_details.warnings:
        for w in job_details.warnings:
            logger.warning(w)

    if job_details.errors:
        if len(job_details.errors) == 1:
            logger.error("Job creation encountered an error: {err}.", err=job_details.errors[0])
        else:
            logger.error(
                "Job creation encountered multiple errors: {errs}.", errs=job_details.errors
            )
