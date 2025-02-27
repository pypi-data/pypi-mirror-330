import logging

from .base import AWG
from .enums import WaveformType, FrequencyUnit, AmplitudeUnit


class SiglentSDG1000X(AWG):
    def __init__(self, ip_address):
        super().__init__(ip_address)
        logging.debug("SiglentSDG1000X instance created.")

    def get_channel_wave_parameter(self, channel, parameter):
        """Gets the waveform parameters for the specified channel"""
        try:
            response = self.query(f"C{channel}BSWV?").split(' ')[1]
            params = dict(zip(response.strip("'").split(',')[::2], response.strip("'").split(',')[1::2]))

            result_dict = {
                'waveform_type': params.get('WVTP'),
                'frequency': params.get('FRQ'),
                'period': params.get('PERI'),
                'amplitude': params.get('AMP'),
                'offset': params.get('OFST'),
                'high_level': params.get('HLEV'),
                'low_level': params.get('LLEV'),
                'phase': params.get('PHSE')
            }
            return result_dict[parameter]
            
        except Exception as e:
            logging.error(f"Failed to retrieve parameter and/or its value: {e}")
            raise

    def set_amplitude(self, channel, amplitude: float, unit: AmplitudeUnit = AmplitudeUnit.VPP):
        """Sets the amplitude for the specified channel."""
        try:
            self.write(f"C{channel}:BSWV AMP,{amplitude}")
            logging.debug(f"Channel {channel} amplitude set to {amplitude}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} amplitude to {amplitude}{unit.value}: {e}")
            raise

    def set_burst_delay(self, channel, delay: float):
        try:
            self.write(f"C{channel}:BTWV DEL,{delay}")
            logging.debug(f"Channel {channel} burst delay has been set to {delay}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} burst delay to {delay}") 

    def set_burst_mode(self, channel, state: bool):
        state_str = "ON" if state else "OFF"
        try:
            self.write(f"C{channel}:BTWV STATE,{state_str}")
            logging.debug(f"Channel {channel} burst mode has been set to {state_str}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} burst mode to {state_str}") 

    def set_burst_period(self, channel, period: float):
        try:
            self.write(f"C{channel}:BTWV PRD,{period}")
            logging.debug(f"Channel {channel} burst period has been set to {period}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} burst period to {period}") 

    def set_frequency(self, channel, frequency: float, unit: FrequencyUnit = FrequencyUnit.HZ):
        """Sets the frequency for the specified channel."""
        try:
            converted_frequency = frequency
            if unit == FrequencyUnit.KHZ:
                converted_frequency = frequency * 1000
            elif unit == FrequencyUnit.MHZ:
                converted_frequency = frequency * 1000000

            self.write(f"C{channel}:BSWV FRQ,{converted_frequency}")
            logging.debug(f"Channel {channel} frequency set to {frequency}{unit.value} (converted to {converted_frequency} Hz)")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} frequency to {frequency}{unit.value}: {e}")
            raise

    def set_offset(self, channel, offset_voltage: float):
        """Sets the offset voltage for the specified channel."""
        try:
            self.write(f"C{channel}:BSWV OFST,{offset_voltage}")
            logging.debug(f"Channel {channel} offset voltage set to {offset_voltage} Vdc")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} offset voltage to {offset_voltage} Vdc: {e}")
            raise

    def set_output(self, channel, state: bool):
        state_str = "ON" if state else "OFF"
        try:
            self.write(f"C{channel}:OUTP {state_str}")
            logging.debug(f"Channel {channel} output has been set to {state_str}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} output to {state_str}")

    def set_output_load(self, channel, load: str | int):
        if load == 'HZ' or load == 'INF':
            load = 'HZ'
        try:
            self.write(f"C{channel}:OUTP LOAD,{load}")
            logging.debug(f"Channel {channel} output load has been set to {load}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} output load to {load}")

    def set_phase(self, channel, phase: float):
        """Sets the phase for the specified channel."""
        try:
            self.write(f"C{channel}:BSWV PHSE,{phase}")
            logging.debug(f"Channel {channel} phase set to {phase}°")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} phase to {phase}°: {e}")
            raise

    def set_waveform(self, channel, waveform_type: WaveformType):
        """Sets the waveform type for the specified channel."""
        try:
            self.write(f"C{channel}:BSWV WVTP,{waveform_type.value}")
            logging.debug(f"Channel {channel} waveform set to {waveform_type.value}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} waveform to {waveform_type.value}: {e}")
            raise

    def sync_phase(self):
        """Sets the phase synchronization of the two channels."""
        try:
            self.write(f"EQPHASE")
            logging.debug(f"Phases of both the channels have been synchronized")
        except Exception as e:
            logging.error(f"Failed to synchronize phase: {e}")
            raise
