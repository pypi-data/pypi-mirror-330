"""
    QApp Platform Project
    pennylane_device_factory.py
    Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qapp_common.config.logging_config import logger
from qapp_common.enum.provider_tag import ProviderTag
from qapp_common.enum.sdk import Sdk
from qapp_common.factory.device_factory import DeviceFactory
from qapp_common.model.provider.provider import Provider
from ..model.device.qapp_pyquil_device import QAppPyquilDevice


class PyquilDeviceFactory(DeviceFactory):

    @staticmethod
    def create_device(provider: Provider, device_specification: str, authentication: dict, sdk: Sdk,
                      **kwargs):
        logger.info("[PyquilDeviceFactory] create_device()")

        provider_type = ProviderTag.resolve(provider.get_provider_type().value)

        match provider_type:
            case ProviderTag.QUAO_QUANTUM_SIMULATOR:
                if Sdk.PYQUIL == sdk:
                    logger.debug('[PyquilDeviceFactory] Creating QAppPennylaneDevice')
                    return QAppPyquilDevice(provider, device_specification)
            case _:
                raise ValueError(f"Unsupported provider type: {provider_type}")