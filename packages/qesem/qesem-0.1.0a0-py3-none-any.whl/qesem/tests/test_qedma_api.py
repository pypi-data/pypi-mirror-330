"""Qedma API tests"""
import concurrent.futures

# pylint: disable=missing-function-docstring,missing-class-docstring
import datetime
import importlib.resources
import json
import pathlib
import time
import urllib.parse

import pytest
import qiskit
import qiskit.qasm3
import responses
import responses.matchers

import qedma_api
import qedma_api.client


TEST_QASM = """
OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
x q[0];
cx q[0], q[1];
"""

test_job = qedma_api.JobDetails(
    account_id="test_account_id",
    job_id="job_1",
    description="test",
    created_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
    updated_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
    status=qedma_api.JobStatus.SUCCEEDED,
    analytical_qpu_time_estimation=datetime.timedelta(minutes=30),
    empirical_qpu_time_estimation=datetime.timedelta(minutes=40),
    total_execution_time=datetime.timedelta(minutes=29),
    qpu_name="kolkata",
    masked_qpu_token="***test",
    masked_account_token="***test",
    qpu_time={
        "execution": datetime.timedelta(minutes=21),
        "estimation": datetime.timedelta(minutes=2),
    },
)


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
            qedma_api.Observable(root=invalid_observable)

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
        qedma_api.Observable(root=valid_observable)


@pytest.fixture(name="provider")
def provider_fixture() -> qedma_api.IBMQProvider:
    return qedma_api.IBMQProvider(instance="test", token_ref="test")


@pytest.fixture(name="client")
def client_fixture(provider: qedma_api.IBMQProvider) -> qedma_api.Client:
    return qedma_api.Client(api_token="test", provider=provider, uri="http://test-endpoint")


class TestClient:
    @responses.activate
    def test_create_new_job_with_invalid_input(self, client: qedma_api.Client) -> None:
        responses.add(
            responses.POST,
            f"{client.uri}/job",
            body=json.dumps({"detail": "invalid input"}),
            status=422,
        )

        circ = qiskit.QuantumCircuit(5)
        circ.x(3)
        circ.measure_all()

        with pytest.raises(qedma_api.client.QedmaServerError, match="invalid input"):
            client.create_job(
                circuit=circ,
                observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
                precision=1.3,
                backend="test",
            )

    @responses.activate
    def test_create_new_job_with_default_options(
        self, client: qedma_api.Client, provider: qedma_api.IBMQProvider
    ) -> None:
        circ = qiskit.QuantumCircuit(5)
        circ.x(3)
        circ.measure_all()

        responses.add(
            responses.POST,
            f"{client.uri}/job",
            body=qedma_api.JobDetails(
                account_id="test_account_id",
                job_id="job_1",
                created_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
                updated_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
                status=qedma_api.JobStatus.SUCCEEDED,
                analytical_qpu_time_estimation=datetime.timedelta(minutes=30),
                empirical_qpu_time_estimation=datetime.timedelta(minutes=40),
                total_execution_time=datetime.timedelta(minutes=29),
                qpu_name="kolkata",
                masked_qpu_token="***test",
                masked_account_token="***test",
                qpu_time={
                    "execution": datetime.timedelta(),
                },
            ).model_dump_json(),
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
                responses.matchers.json_params_matcher(
                    json.loads(
                        qedma_api.client.JobRequest(
                            circuit=qedma_api.Circuit(
                                circuit=qiskit.qasm3.dumps(circ),
                                observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
                                precision=1.3,
                                options=qedma_api.CircuitOptions(),
                            ),
                            provider=provider,
                            empirical_time_estimation=False,
                            backend="test",
                        ).model_dump_json()
                    )
                ),
            ],
        )

        client.create_job(
            circuit=circ,
            observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
            precision=1.3,
            backend="test",
        )

    @responses.activate
    def test_create_new_job_with_default_options_and_a_single_observable(
        self, client: qedma_api.Client, provider: qedma_api.IBMQProvider
    ) -> None:
        circ = qiskit.QuantumCircuit(5)
        circ.x(3)
        circ.measure_all()

        responses.add(
            responses.POST,
            f"{client.uri}/job",
            body=qedma_api.JobDetails(
                account_id="test_account_id",
                job_id="job_1",
                created_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
                updated_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
                status=qedma_api.JobStatus.SUCCEEDED,
                analytical_qpu_time_estimation=datetime.timedelta(minutes=30),
                empirical_qpu_time_estimation=datetime.timedelta(minutes=40),
                total_execution_time=datetime.timedelta(minutes=29),
                qpu_name="kolkata",
                masked_qpu_token="***test",
                masked_account_token="***test",
                qpu_time={
                    "execution": datetime.timedelta(),
                },
            ).model_dump_json(),
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
                responses.matchers.json_params_matcher(
                    json.loads(
                        qedma_api.client.JobRequest(
                            circuit=qedma_api.Circuit(
                                circuit=qiskit.qasm3.dumps(circ),
                                observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
                                precision=1.3,
                                options=qedma_api.CircuitOptions(),
                            ),
                            provider=provider,
                            empirical_time_estimation=False,
                            backend="test",
                        ).model_dump_json()
                    )
                ),
            ],
        )

        client.create_job(
            circuit=circ,
            observables=qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),
            precision=1.3,
            backend="test",
        )

    @responses.activate
    def test_create_new_job_with_transpilation_level_0(
        self, client: qedma_api.Client, provider: qedma_api.IBMQProvider
    ) -> None:
        circ = qiskit.QuantumCircuit(5)
        circ.x(3)
        circ.measure_all()

        responses.add(
            responses.POST,
            f"{client.uri}/job",
            body=qedma_api.JobDetails(
                account_id="test_account_id",
                job_id="mock_job_id",
                created_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
                updated_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
                status=qedma_api.JobStatus.SUCCEEDED,
                analytical_qpu_time_estimation=datetime.timedelta(minutes=30),
                empirical_qpu_time_estimation=datetime.timedelta(minutes=40),
                total_execution_time=datetime.timedelta(minutes=29),
                qpu_name="kolkata",
                masked_qpu_token="***test",
                masked_account_token="***test",
                qpu_time={
                    "execution": datetime.timedelta(),
                },
            ).model_dump_json(),
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
                responses.matchers.json_params_matcher(
                    json.loads(
                        qedma_api.client.JobRequest(
                            circuit=qedma_api.Circuit(
                                circuit=qiskit.qasm3.dumps(circ),
                                observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
                                precision=1.3,
                                options=qedma_api.CircuitOptions(
                                    transpilation_level=qedma_api.TranspilationLevel.LEVEL_0,
                                ),
                            ),
                            provider=provider,
                            empirical_time_estimation=False,
                            backend="test",
                        ).model_dump_json()
                    )
                ),
            ],
        )

        job = client.create_job(
            circuit=circ,
            observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
            precision=1.3,
            circuit_options=qedma_api.CircuitOptions(
                transpilation_level=qedma_api.TranspilationLevel.LEVEL_0,
            ),
            backend="test",
        )
        assert job.job_id == "mock_job_id"

    @responses.activate
    def test_create_new_job_with_transpilation_level_1(
        self, client: qedma_api.Client, provider: qedma_api.IBMQProvider
    ) -> None:
        circ = qiskit.QuantumCircuit(5)
        circ.x(3)
        circ.measure_all()

        responses.add(
            responses.POST,
            f"{client.uri}/job",
            body=qedma_api.JobDetails(
                account_id="test_account_id",
                job_id="mock_job_id",
                created_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
                updated_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
                status=qedma_api.JobStatus.SUCCEEDED,
                analytical_qpu_time_estimation=datetime.timedelta(minutes=30),
                empirical_qpu_time_estimation=datetime.timedelta(minutes=40),
                total_execution_time=datetime.timedelta(minutes=29),
                qpu_name="kolkata",
                masked_qpu_token="***test",
                masked_account_token="***test",
                qpu_time={
                    "execution": datetime.timedelta(),
                },
            ).model_dump_json(),
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
                responses.matchers.json_params_matcher(
                    json.loads(
                        qedma_api.client.JobRequest(
                            description="test",
                            circuit=qedma_api.Circuit(
                                circuit=qiskit.qasm3.dumps(circ),
                                observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
                                precision=1.3,
                                options=qedma_api.CircuitOptions(
                                    transpilation_level=qedma_api.TranspilationLevel.LEVEL_1,
                                ),
                            ),
                            provider=provider,
                            empirical_time_estimation=False,
                            backend="test",
                        ).model_dump_json()
                    )
                ),
            ],
        )

        job = client.create_job(
            description="test",
            circuit=circ,
            observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
            precision=1.3,
            backend="test",
            circuit_options=qedma_api.CircuitOptions(
                transpilation_level=qedma_api.TranspilationLevel.LEVEL_1,
            ),
        )
        assert job.job_id == "mock_job_id"

    @responses.activate
    def test_get_jobs_details_without_circuits(self, client: qedma_api.Client) -> None:
        test_job_1: qedma_api.JobDetails = test_job.model_copy()
        test_job_1.job_id = "job_1"
        test_job_2: qedma_api.JobDetails = test_job.model_copy()
        test_job_2.job_id = "job_2"

        responses.add(
            responses.GET,
            f"{client.uri}/jobs",
            body=qedma_api.client.GetJobsDetailsResponse(
                jobs=[test_job_1, test_job_2]
            ).model_dump_json(),
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
                responses.matchers.query_param_matcher(
                    params={
                        "ids": "job_1,job_2",
                        "include_circuits": False,
                        "include_results": False,
                    }
                ),
            ],
        )

        jobs = client.get_jobs(jobs_ids=["job_1", "job_2"])

        assert len(jobs) == 2
        assert jobs == [test_job_1, test_job_2]

    @responses.activate
    def test_get_single_job_with_circuits_and_results(self, client: qedma_api.Client) -> None:
        expected_job = qedma_api.JobDetails(
            account_id="test_account_id",
            job_id="job_1",
            created_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
            updated_at=datetime.datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
            status=qedma_api.JobStatus.SUCCEEDED,
            analytical_qpu_time_estimation=datetime.timedelta(minutes=30),
            empirical_qpu_time_estimation=datetime.timedelta(minutes=40),
            total_execution_time=datetime.timedelta(minutes=29),
            qpu_name="kolkata",
            masked_qpu_token="***test",
            masked_account_token="***test",
            qpu_time={
                "execution": datetime.timedelta(minutes=2),
                "estimation": datetime.timedelta(minutes=1),
            },
            circuit=qedma_api.Circuit(
                options=qedma_api.CircuitOptions(
                    transpilation_level=qedma_api.TranspilationLevel.LEVEL_1
                ),
                circuit=TEST_QASM,
                observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
                precision=1.3,
            ),
            results=qedma_api.ExpectationValues(
                root=[
                    (
                        qedma_api.Observable({"X1": 1, "Z0,Z3": 0.3}),
                        qedma_api.ExpectationValue(value=1.0, error_bar=0.09),
                    )
                ]
            ),
        )

        responses.add(
            responses.GET,
            f"{client.uri}/jobs",
            body=qedma_api.client.GetJobsDetailsResponse(jobs=[expected_job]).model_dump_json(),
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
                responses.matchers.query_param_matcher(
                    params={
                        "ids": "job_1",
                        "include_circuits": True,
                        "include_results": True,
                    }
                ),
            ],
        )

        job = client.get_job(job_id="job_1", include_circuits=True, include_results=True)

        assert job == expected_job
        assert str(job.results) == "[{'X1': 1.0, 'Z0,Z3': 0.3}: (1.0 ± 0.09)]"
        assert (
            repr(job.results)
            == "ExpectationValues([Observable({'X1': 1.0, 'Z0,Z3': 0.3}): ExpectationValue(value=1.0, error_bar=0.09)])"  # pylint: disable=line-too-long
        )

    @responses.activate
    def test_get_jobs_details_with_circuits(self, client: qedma_api.Client) -> None:
        test_circuit = qedma_api.Circuit(
            options=qedma_api.CircuitOptions(
                transpilation_level=qedma_api.TranspilationLevel.LEVEL_1
            ),
            circuit=TEST_QASM,
            observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),),
            precision=1.3,
        )
        test_job_1: qedma_api.JobDetails = test_job.model_copy()
        test_job_1.job_id = "job_1"
        test_job_1.circuit = test_circuit
        test_job_2: qedma_api.JobDetails = test_job.model_copy()
        test_job_2.job_id = "job_2"
        test_job_2.circuit = test_circuit

        responses.add(
            responses.GET,
            f"{client.uri}/jobs",
            body=qedma_api.client.GetJobsDetailsResponse(
                jobs=[test_job_1, test_job_2]
            ).model_dump_json(),
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
                responses.matchers.query_param_matcher(
                    params={
                        "ids": "job_1,job_2",
                        "include_circuits": True,
                        "include_results": False,
                    }
                ),
            ],
        )

        jobs = client.get_jobs(jobs_ids=["job_1", "job_2"], include_circuits=True)

        assert jobs == [test_job_1, test_job_2]

    @responses.activate
    @pytest.mark.parametrize("max_qpu_time", [datetime.timedelta(minutes=30)])
    def test_start_job(self, max_qpu_time: datetime.timedelta, client: qedma_api.Client) -> None:
        responses.add(
            responses.POST,
            f"{client.uri}/job/123/start",
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
            ],
        )

        client.start_job(
            job_id="123",
            max_qpu_time=max_qpu_time,
            options=qedma_api.JobOptions(execution_mode=qedma_api.ExecutionMode.SESSION),
        )

        responses.assert_call_count(f"{client.uri}/job/123/start", 1)

    @responses.activate
    @pytest.mark.parametrize("max_qpu_time", ["30", "ABC"], ids=lambda x: f"{type(x)}({x})")
    def test_start_job_invalid_input(
        self, max_qpu_time: datetime.timedelta, client: qedma_api.Client
    ) -> None:
        responses.add(
            responses.POST,
            f"{client.uri}/job/123/start",
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
            ],
        )

        with pytest.raises(ValueError):
            client.start_job(job_id="123", max_qpu_time=max_qpu_time)

    @responses.activate
    @pytest.mark.parametrize("max_qpu_time", [datetime.timedelta(minutes=30)])
    def test_start_job_while_estimating(
        self, max_qpu_time: datetime.timedelta, client: qedma_api.Client
    ) -> None:
        error_msg = "Job is still estimating"
        responses.add(
            responses.POST,
            f"{client.uri}/job/123/start",
            status=400,
            body=json.dumps({"detail": error_msg}),
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
            ],
        )

        with pytest.raises(qedma_api.client.QedmaServerError) as e:
            client.start_job(job_id="123", max_qpu_time=max_qpu_time)
            assert str(e) == error_msg

        responses.assert_call_count(f"{client.uri}/job/123/start", 1)

    @responses.activate
    def test_cancel_job(self, client: qedma_api.Client) -> None:
        responses.add(
            responses.POST,
            f"{client.uri}/job/123/cancel",
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
            ],
        )

        client.cancel_job(job_id="123")

        responses.assert_call_count(f"{client.uri}/job/123/cancel", 1)

    @responses.activate
    def test_get_listing_jobs_without_circuits(self, client: qedma_api.Client) -> None:
        test_job_1: qedma_api.JobDetails = test_job.model_copy()
        test_job_1.job_id = "job_1"
        test_job_2: qedma_api.JobDetails = test_job.model_copy()
        test_job_2.job_id = "job_2"

        responses.add(
            responses.GET,
            f"{client.uri}/jobs/list",
            body=qedma_api.client.GetJobsDetailsResponse(
                jobs=[test_job_1, test_job_2]
            ).model_dump_json(),
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
                responses.matchers.query_param_matcher(
                    params={
                        "skip": 0,
                        "limit": 50,
                    }
                ),
            ],
        )

        jobs = client.list_jobs(skip=0, limit=50)

        assert jobs == [test_job_1, test_job_2]

    @responses.activate
    def test_register_qpu_token(self) -> None:
        """Test storing a vendor token."""
        default_uri = "http://test-endpoint"
        qedma_client = qedma_api.Client(api_token="test", uri=default_uri)

        responses.post(
            f"{default_uri}/qpu-token",
            body=qedma_api.client.RegisterQpuTokenResponse(qpu_token_ref="123").model_dump_json(),
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
            ],
        )

        token_ref = qedma_client.register_qpu_token(token="secret_token")

        assert token_ref == "123"

    @responses.activate
    def test_unregister_token(self) -> None:
        """Test unregistering a vendor token."""
        default_uri = "http://test-endpoint"
        qedma_client = qedma_api.Client(api_token="test", uri=default_uri)

        responses.delete(
            f"{default_uri}/qpu-token/456",
            status=200,
            match=[
                responses.matchers.header_matcher({"Authorization": "Bearer test"}),
            ],
        )

        qedma_client.unregister_qpu_token(token_ref="456")

        responses.assert_call_count(f"{default_uri}/qpu-token/456", 1)

    @responses.activate
    @pytest.mark.parametrize("with_empirical_time_estimation", [True, False])
    def test_wait_for_status(
        self,
        caplog: pytest.LogCaptureFixture,
        with_empirical_time_estimation: bool,
        client: qedma_api.Client,
    ) -> None:
        """Test the wait function"""
        job: qedma_api.JobDetails = test_job.model_copy()
        job.job_id = "tst"
        job.status = qedma_api.JobStatus.ESTIMATING
        job.intermediate_results = qedma_api.ExpectationValues(
            [
                (
                    qedma_api.Observable({"X1": 1.0}),
                    qedma_api.ExpectationValue(value=1.0, error_bar=0.1),
                )
            ]
        )
        if not with_empirical_time_estimation:
            job.empirical_qpu_time_estimation = None
            job.qpu_time.pop("estimation", None)
        else:
            job.analytical_qpu_time_estimation = datetime.timedelta(minutes=30)
            job.empirical_qpu_time_estimation = datetime.timedelta(minutes=3)
            job.qpu_time["estimation"] = datetime.timedelta(minutes=3)

        responses.add(
            responses.GET,
            f"{client.uri}/jobs",
            body=qedma_api.client.GetJobsDetailsResponse(jobs=[job]).model_dump_json(),
            status=200,
            match=[responses.matchers.header_matcher({"Authorization": "Bearer test"})],
        )

        with concurrent.futures.ThreadPoolExecutor() as ex:
            est_future = ex.submit(
                client.wait_for_time_estimation,
                "tst",
                interval=datetime.timedelta(seconds=0.1),
            )

            job.status = qedma_api.JobStatus.ESTIMATED
            responses.add(
                responses.GET,
                f"{client.uri}/jobs",
                body=qedma_api.client.GetJobsDetailsResponse(jobs=[job]).model_dump_json(),
                status=200,
                match=[responses.matchers.header_matcher({"Authorization": "Bearer test"})],
            )

            assert not est_future.done()

            time.sleep(0.2)

            assert est_future.done()
            if with_empirical_time_estimation:
                assert est_future.result() == job.empirical_qpu_time_estimation
            else:
                assert est_future.result() == job.analytical_qpu_time_estimation

            job_future = ex.submit(
                client.wait_for_job_complete, "tst", interval=datetime.timedelta(seconds=0.1)
            )
            assert not job_future.done()

            time.sleep(0.2)  # wait for interval to pass

            assert f"Intermediate results for job {job.job_id}:" in caplog.text

            job.status = qedma_api.JobStatus.SUCCEEDED
            responses.add(
                responses.GET,
                f"{client.uri}/jobs",
                body=qedma_api.client.GetJobsDetailsResponse(jobs=[job]).model_dump_json(),
                status=200,
                match=[responses.matchers.header_matcher({"Authorization": "Bearer test"})],
            )

            time.sleep(0.2)  # wait for interval to pass

            assert job_future.done()
            job_res = job_future.result()
            assert job_res == job
            if with_empirical_time_estimation:
                assert job_res.qpu_time["estimation"]
            else:
                assert "estimation" not in job_res.qpu_time

    @pytest.mark.parametrize(
        ["num_observables", "num_params", "parameters", "error"],
        [
            (
                2,
                1,
                {"param0": (1.0, 2.0, 3.0)},
                "Number of observables must be equal to the number of parameter values",
            ),
            (
                3,
                1,
                {"param0": (1.0, 2.0)},
                "Number of observables must be equal to the number of parameter values",
            ),
            (
                2,
                2,
                {"param0": (1.0, 2.0), "param1": (3.0,)},
                "All parameter values must have the same length",
            ),
            (
                2,
                3,
                {"param0": (1.0, 2.0), "param2": (3.0,), "param1": (4.0, 5.0)},
                "All parameter values must have the same length",
            ),
            (
                2,
                2,
                {"param0": (1.0, 2.0), "param1": (4.0, 5.0, 6.0)},
                "All parameter values must have the same length",
            ),
            (
                2,
                2,
                {"param0": (1.0, 2.0), qiskit.circuit.Parameter("param1"): (4.0, 5.0, 6.0)},
                "All parameter values must have the same length",
            ),
            (
                2,
                2,
                {"param0": (1.0, 2.0), "notparam1": (4.0, 5.0)},
                "Parameters must match the circuit parameters",
            ),
            (
                2,
                2,
                {"param0": (1.0, 2.0), qiskit.circuit.Parameter("notparam1"): (4.0, 5.0)},
                "Parameters must match the circuit parameters",
            ),
            (
                2,
                3,
                {"param0": (1.0, 2.0), "param1": (3.0,)},
                "Parameters must match the circuit parameters",
            ),
            (
                2,
                3,
                {
                    "param0": (1.0, 2.0),
                    "param1": (3.0, 0.0),
                    "param2": (4.0, 5.0),
                    "param3": (6.0, 7.0),
                },
                "Parameters must match the circuit parameters",
            ),
            (
                2,
                3,
                None,
                "Parameters must match the circuit parameters",
            ),
            (
                2,
                0,
                {"param0": (1, 2, 3)},
                "Parameters must match the circuit parameters",
            ),
        ],
        ids=[
            "too_many_values",
            "too_few_values",
            "parameters_have_different_lengths",
            "parameters_have_different_lengths_2",
            "parameters_have_different_lengths_3",
            "parameters_have_different_lengths_qiskit_param",
            "wrong_name",
            "wrong_name_qiskit_param",
            "missing_parameters",
            "too_many_parameters",
            "no_parameters",
            "no_circuit_parameters",
        ],
    )
    @responses.activate
    def test_invalid_call_parameters(  # pylint: disable=too-many-positional-arguments
        self,
        num_observables: int,
        num_params: int,
        parameters: dict[str, tuple[float, ...]] | None,
        error: str,
        client: qedma_api.Client,
    ) -> None:
        responses.add(
            responses.POST,
            f"{client.uri}/job",
            body=json.dumps({"detail": "invalid input"}),
            status=422,
        )

        circ = qiskit.QuantumCircuit(5)
        circ.x(3)
        for i in range(num_params):
            circ.rx(qiskit.circuit.Parameter(f"param{i}"), 0)
        circ.measure_all()

        with pytest.raises(ValueError, match=error):
            if parameters is None:
                client.create_job(
                    circuit=circ,
                    observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),)
                    * num_observables,
                    parameters=None,
                    precision=1.3,
                    backend="test",
                    precision_mode=None,
                )
            else:
                client.create_job(
                    circuit=circ,
                    observables=(qedma_api.Observable({"X1": 1.0, "Z0,Z3": 0.3}),)
                    * num_observables,
                    parameters=parameters,
                    precision=1.3,
                    backend="test",
                    precision_mode=qedma_api.PrecisionMode("JOB"),
                )

    @responses.activate(  # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
        registry=responses.registries.OrderedRegistry, assert_all_requests_are_fired=True
    )
    def test_decompose_args(self, tmp_path: pathlib.Path, client: qedma_api.Client) -> None:
        with (
            importlib.resources.files(__package__)
            .joinpath("resources/decompose_response.json")
            .open("r") as f
        ):
            responses.add(
                responses.POST,
                f"{client.uri}/hpc/decompose",
                body=b'{"task_id": "task_1"}',
                status=200,
            )
            responses.add(
                responses.GET,
                f"{client.uri}/hpc/decompose/task_1",
                status=202,
            )
            responses.add(
                responses.GET,
                f"{client.uri}/hpc/decompose/task_1",
                status=202,
            )
            responses.add(
                responses.GET,
                f"{client.uri}/hpc/decompose/task_1",
                body=f.read(),
                status=200,
            )

        with tmp_path.joinpath("mpo_file").open("w") as f:
            f.write("test")

        n = 20

        client.decompose(
            mpo_file=str(tmp_path.joinpath("mpo_file")),
            max_bases=2,
            l2_truncation_err=1e-3,
            observable=qedma_api.Observable({f"Z{i}": 1 / n for i in range(n)}),
        )
        parsed_url = urllib.parse.urlparse(responses.calls[0].request.url)
        qparams = urllib.parse.parse_qs(parsed_url.query)  # type: ignore[type-var]

        assert set(qparams) == {
            "max_bases",
            "l2_truncation_err",
            "op_l2_norm",
            "k",
            "pauli_coeff_th",
        }
        op_l2_norm = float(qparams["op_l2_norm"][0])  # type: ignore[arg-type]
        assert op_l2_norm == pytest.approx(1 / n**0.5)

    @responses.activate(  # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
        registry=responses.registries.OrderedRegistry, assert_all_requests_are_fired=True
    )
    def test_decompose_args_expire(self, tmp_path: pathlib.Path, client: qedma_api.Client) -> None:
        responses.add(
            responses.POST,
            f"{client.uri}/hpc/decompose",
            body=b'{"task_id": "task_1"}',
            status=200,
        )
        responses.add(
            responses.GET,
            f"{client.uri}/hpc/decompose/task_1",
            status=202,
        )
        responses.add(
            responses.GET,
            f"{client.uri}/hpc/decompose/task_1",
            status=202,
        )
        responses.add(
            responses.GET,
            f"{client.uri}/hpc/decompose/task_1",
            status=404,
        )

        with tmp_path.joinpath("mpo_file").open("w") as f:
            f.write("test")

        n = 20
        with pytest.raises(qedma_api.client.QedmaServerError) as e:
            client.decompose(
                mpo_file=str(tmp_path.joinpath("mpo_file")),
                max_bases=2,
                l2_truncation_err=1e-3,
                observable=qedma_api.Observable({f"Z{i}": 1 / n for i in range(n)}),
            )

        assert "404" in str(e.value)
