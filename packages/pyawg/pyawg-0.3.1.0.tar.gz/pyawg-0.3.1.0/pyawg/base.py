from __future__ import annotations

import json
import logging

import vxi11

from .enums import WaveformType, AmplitudeUnit, FrequencyUnit


class AWG:
    ip_addr: str
    device: vxi11.Instrument | None
    manufacturer: str
    model: str
    serial_number: str
    fw_version: str

    def __init__(self: AWG, ip_addr: str):
        self.ip_addr = ip_addr
        self.device = None
        try:
            self.device = vxi11.Instrument(ip_addr)
            self.device.clear()
            logging.debug(f"Connected to AWG at {ip_addr}")
            
            self.manufacturer, self.model, self.serial_number, self.fw_version = self.get_id().strip().split(',')
        except Exception as e:
            logging.error(f"Failed to connect to AWG at {ip_addr}: {e}")
            raise
    
    def __str__(self):
        return json.dumps(
            dict(
                manufacturer=self.manufacturer,
                model=self.model,
                serial_number=self.serial_number,
                fw_version=self.fw_version
            ),
            indent=2
        )
        
    def close(self):
        try:
            self.device.close()
            logging.debug("Disconnected from AWG")
        except Exception as e:
            logging.error(f"Failed to disconnect from AWG: {e}")

    def get_id(self) -> str:
        return self.query("*IDN?")

    def query(self, command):
        try:
            response = self.device.ask(command)
            logging.debug(f"Sent query: {command}, Received: {response}")
            return response
        except Exception as e:
            logging.error(f"Failed to query command: {e}")
            raise

    def write(self, command):
        try:
            self.device.write(command)
            logging.debug(f"Sent command: {command}")
        except Exception as e:
            logging.error(f"Failed to write command: {e}")
            raise
