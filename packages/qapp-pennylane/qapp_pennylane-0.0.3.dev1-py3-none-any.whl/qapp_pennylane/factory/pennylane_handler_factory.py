"""
    QApp Platform Project pennylane_handler_factory.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from qapp_common.config.logging_config import logger
from qapp_common.factory.handler_factory import HandlerFactory
from qapp_common.handler.handler import Handler

from ..handler.invocation_handler import InvocationHandler


class PennylaneHandlerFactory(HandlerFactory):

    @staticmethod
    def create_handler(event, circuit_preparation_fn, post_processing_fn) -> Handler:
        logger.info("[PennylaneHandlerFactory] create_handler()")

        request_data = event.json()

        logger.debug("[PennylaneHandlerFactory] Create InvocationHandler")
        return InvocationHandler(
            request_data=request_data,
            circuit_preparation_fn=circuit_preparation_fn,
            post_processing_fn=post_processing_fn,
        )