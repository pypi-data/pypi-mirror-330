"""
    QApp Platform Project
    qapp_pennylane_provider.py
    Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qapp_common.config.logging_config import logger
from qapp_common.enum.provider_tag import ProviderTag
from qapp_common.model.provider.provider import Provider


class QAppPennyLaneProvider(Provider):
    def __init__(self, ):
        logger.debug('[QAppPennyLaneProvider] get_backend()')
        super().__init__(ProviderTag.QUAO_QUANTUM_SIMULATOR)

    def get_backend(self, device_specification):
        logger.debug('[QAppPennyLaneProvider] get_backend()')

        try:
            # with pennylane, create backend later 
            return None
        except Exception:
            raise ValueError('[QAppPennyLaneProvider] Unsupported device')

    def collect_provider(self):
        logger.debug('[QAppPennyLaneProvider] collect_provider()')
        return None