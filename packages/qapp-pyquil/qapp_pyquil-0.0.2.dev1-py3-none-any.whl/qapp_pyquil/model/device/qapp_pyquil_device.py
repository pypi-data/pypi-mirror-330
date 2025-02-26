"""
    QApp Platform Project
    qapp_pyquil_device.py
    Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
import time
import math

from qapp_common.data.response.authentication import Authentication
from qapp_common.data.response.project_header import ProjectHeader
from qapp_common.model.device.device import Device
from qapp_common.config.logging_config import logger
from qapp_common.data.device.circuit_running_option import CircuitRunningOption
from qapp_common.model.provider.provider import Provider
from qapp_common.enum.invocation_step import InvocationStep


class QAppPyquilDevice(Device):
    def __init__(self, provider: Provider, device_specification: str):
        super().__init__(provider, device_specification)
        logger.debug('[QAppPyquilDevice] Initializing device specification')
        self.device_specification = device_specification

    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug(
            '[QAppPyquilDevice] Creating job with {0} shots'.format(
                options.shots))
        
        circuit.wrap_in_numshots_loop(options.shots)
      
        start_time = time.time()
        executable = self.device.compile(circuit)
        result = self.device.run(executable)
        end_time = time.time()

        # with QuantumTape() as tape:
        #     circuit()

        # parts = self.device_specification.split('/')

        # device_name = parts[0]
        # if device_name == "rigetti.qvm":
        #     device_type = parts[1]
        #     if parts[1] in ["9q-square-qvm", "9q-square-pyqvm"]:
        #         self.device = qml.device(device_name, device=device_type,
        #                                  shots=options.shots)
        #     else:
        #         self.device = qml.device(device_name, device=str(tape.num_wires) + device_type[1:],
        #                                  shots=options.shots)
        # else:
        #     self.device = qml.device(device_name, wires=tape.wires,
        #                              shots=options.shots)

        # start_time = time.time()
        # qnode = qml.QNode(circuit, self.device)
        # job_result = qnode()
        # end_time = time.time()

        # result_histogram = {}

        # # generate histogram
        # if qml.probs() in qnode.tape.observables:
        #     histogram_index = qnode.tape.observables.index(qml.probs())
        #     probs = job_result[histogram_index]
        #     num_bits = math.ceil(math.log2(len(probs)))
        #     for i, prob in enumerate(probs):
        #         bitstring = format(i, f'0{num_bits}b')
        #         result_histogram[bitstring] = int(prob * options.shots)
        # else:
        #     result_histogram = None

        data = {"result": result, "time_taken_execute": end_time - start_time}

        # logger.info(data)
        return data

    def _is_simulator(self) -> bool:
        logger.debug('[QAppPyquilDevice] Is simulator')
        return True

    def _produce_histogram_data(self, job_result) -> dict | None:
        logger.info('[PyquilDevice] Producing histogram data')

        histogram = job_result.get('histogram')

        if histogram is None:
            logger.debug("[PyquilDevice] Can't produce histogram")

        return job_result.get('histogram')

    def _get_provider_job_id(self, job) -> str:
        logger.debug('[PyquilDevice] Getting job id')

        # no job id in local simulator
        return ""

    def _get_job_status(self, job) -> str:
        logger.debug('[PyquilDevice] Getting job status')

        return "DONE"

    def _get_job_result(self, job) -> dict:
        logger.debug('[PyquilDevice] Getting job result')

        return job

    def _calculate_execution_time(self, job_result):
        logger.debug('[PyquilDevice] Calculating execution time')

        self.execution_time = job_result.get('time_taken_execute')

        logger.debug(
            '[PyquilDevice] Execution time calculation was: {0} seconds'.format(
                self.execution_time))

    def run_circuit(self,
                    circuit,
                    post_processing_fn,
                    options: CircuitRunningOption,
                    callback_dict: dict,
                    authentication: Authentication,
                    project_header: ProjectHeader):
        """
        @param project_header: project header
        @param callback_dict: callback url dictionary
        @param options: Options for run circuit
        @param authentication: Authentication for calling quao server
        @param post_processing_fn: Post-processing function
        @param circuit: Circuit was run
        """
        original_job_result, job_response = self._on_execution(
            authentication=authentication,
            project_header=project_header,
            execution_callback=callback_dict.get(InvocationStep.EXECUTION),
            circuit=circuit,
            options=options)

        if original_job_result is None:
            return

        job_response = self._on_analysis(
            job_response=job_response,
            original_job_result=original_job_result,
            analysis_callback=callback_dict.get(InvocationStep.ANALYSIS))

        if job_response is None:
            return

        self._on_finalization(job_result=original_job_result.get('result'),
                              authentication=authentication,
                              post_processing_fn=post_processing_fn,
                              finalization_callback=callback_dict.get(
                                  InvocationStep.FINALIZATION),
                              project_header=project_header)
