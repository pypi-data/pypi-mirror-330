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

from ..model.device.qapp_pennylane_device import QAppPennylaneDevice


class PennylaneDeviceFactory(DeviceFactory):

    @staticmethod
    def create_device(provider: Provider, device_specification: str, authentication: dict, sdk: Sdk,
                      **kwargs):
        logger.info("[PennylaneDeviceFactory] create_device()")

        provider_type = ProviderTag.resolve(provider.get_provider_type().value)

        match provider_type:
            case ProviderTag.QUAPP:
                if Sdk.PENNYLANE == sdk:
                    logger.debug('[PennylaneDeviceFactory] Creating QAppPennylaneDevice')
                    return QAppPennylaneDevice(provider, device_specification)
            # case ProviderTag.AWS_BRAKET:
            #     logger.debug('[PennylaneDeviceFactory] Creating AwsBraketDevice')
            #     return AwsBraketDevice(provider, device_specification, kwargs['backend_name'],
            #                            kwargs['num_qubits'], kwargs['s3_bucket_name'],
            #                            kwargs['s3_prefix'], kwargs['inputs'])
            # case ProviderTag.IBM_QUANTUM:
            #     return IbmQuantumDevice(provider, device_specification,
            #                             api_token=authentication.get('api_token'),
            #                             instance=authentication.get('instance'))
            case _:
                raise ValueError(f"Unsupported provider type: {provider_type}")