"""
    QApp Platform Project
    pennylane_provider_factory.py
    Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qapp_common.config.logging_config import logger
from qapp_common.enum.provider_tag import ProviderTag
from qapp_common.enum.sdk import Sdk
from qapp_common.factory.provider_factory import ProviderFactory

from ..model.provider.qapp_pyquil_provider import QAppPyquilProvider

class PyquilProviderFactory(ProviderFactory):

    @staticmethod
    def create_provider(provider_type: ProviderTag, sdk: Sdk, authentication: dict):
        logger.info("[PyquilProviderFactory] create_provider()")
        logger.debug(f"provider_type: {provider_type}, sdk: {sdk}, authentication: {authentication}")

        match provider_type:
            case ProviderTag.QUAO_QUANTUM_SIMULATOR:
                if Sdk.PYQUIL.__eq__(sdk):
                    return QAppPyquilProvider()
                raise ValueError(f'Unsupported SDK for provider type: {provider_type}')
            # case ProviderTag.AWS_BRAKET:
            #     return AwsBraketProvider(authentication.get('access_key_id'),
            #                              authentication.get('secret_access_key'),
            #                              authentication.get('region_name'))
            case _:
                raise ValueError(f'Unsupported provider type: {provider_type}')