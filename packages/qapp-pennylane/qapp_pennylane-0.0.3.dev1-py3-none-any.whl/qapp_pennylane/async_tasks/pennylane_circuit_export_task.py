"""
    QApp Platform Project pennylane_circuit_export_task.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qapp_common.async_tasks.export_circuit_task import CircuitExportTask
from qapp_common.config.logging_config import logger
import pennylane as qml
from io import BytesIO


class PennylaneCircuitExportTask(CircuitExportTask):
        
    def _convert(self):
        
        logger.debug("[Circuit export] Preparing circuit figure...")
        circuit = self.circuit_data_holder.circuit
        circuit_figure, _ = qml.draw_mpl(circuit)()
        logger.debug("[Circuit export] Converting circuit figure to svg file...")
        figure_buffer = BytesIO()
        circuit_figure.savefig(figure_buffer, format="svg")
        
        return figure_buffer