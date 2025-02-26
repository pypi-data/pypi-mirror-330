"""
    QApp Platform Project pennylane_invocation.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from qapp_common.component.backend.invocation import Invocation
from qapp_common.config.logging_config import logger
from qapp_common.config.thread_config import circuit_exporting_pool
from qapp_common.data.async_task.circuit_export.backend_holder import BackendDataHolder
from qapp_common.data.async_task.circuit_export.circuit_holder import CircuitDataHolder
from qapp_common.data.request.invocation_request import InvocationRequest
from qapp_common.model.provider.provider import Provider

from ...async_tasks.pyquil_circuit_export_task import PyquilCircuitExportTask
from ...factory.pyquil_device_factory import PyquilDeviceFactory
from ...factory.pyquil_provider_factory import PyquilProviderFactory

class PyquilInvocation(Invocation):

    def __init__(self, request_data: InvocationRequest, **kwargs):
        super().__init__(request_data)
        self.num_qubits = kwargs.get('num_qubits')

    def _export_circuit(self, circuit):
        logger.info("[PennylaneInvocation] _export_circuit()")

        circuit_export_task = PyquilCircuitExportTask(
            circuit_data_holder=CircuitDataHolder(circuit, self.circuit_export_url),
            backend_data_holder=BackendDataHolder(
                self.backend_information, self.authentication.user_token
            ),
        )
        circuit_exporting_pool.submit(circuit_export_task.do)

    def _create_provider(self):
        logger.info('[PennylaneInvocation] _create_provider()')

        return PyquilProviderFactory.create_provider(
            provider_type=self.backend_information.provider_tag, sdk=self.sdk,
            authentication=self.backend_information.authentication)

    def _create_device(self, provider: Provider):
        logger.info('[PennylaneInvocation] Creating device')
        return PyquilDeviceFactory.create_device(provider=provider,
                                                    device_specification=self.backend_information.device_name,
                                                    authentication=self.backend_information.authentication,
                                                    sdk=self.sdk, num_qubits=self.num_qubits,
                                                    input=self.input)

    def _get_qubit_amount(self, circuit):
        return len(circuit.get_qubit_indices())