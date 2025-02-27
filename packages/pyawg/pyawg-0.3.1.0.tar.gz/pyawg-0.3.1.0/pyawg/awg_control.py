from .base import AWG
from .rigol import RigolDG1000Z
from .siglent import SiglentSDG1000X
import logging
import re

def awg_control(ip_address: str) -> AWG:
    """
    Factory function to create AWG instances based on device identification.
    """
    try:
        # Create a generic AWG instance to identify the device
        temp_awg = AWG(ip_address)
        model = temp_awg.model
        temp_awg.close()  # Close the temporary connection

        if re.match('^(DG10[3|6]2Z)$', model):
            return RigolDG1000Z(ip_address)
        elif re.match('^(SDG10[3|6]2X)$', model):
            return SiglentSDG1000X(ip_address)
        else:
            raise ValueError(f"Unsupported AWG device: {device_id}")
    except Exception as e:
        logging.error(f"Failed to identify AWG at {ip_address}: {e}")
        raise