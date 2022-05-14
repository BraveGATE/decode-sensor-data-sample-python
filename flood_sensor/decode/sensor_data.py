import base64
import struct


class FloodSensorData:
    fw_version: str
    water_pressure: float
    water_temperature: float
    air_pressure: float
    air_temperature: float
    battery: int

    def __init__(self, sensor_data_base64) -> None:
        sensordata_bytes = base64.b64decode(sensor_data_base64, validate=True)
        if len(sensordata_bytes) != 20: raise ValueError('Invalid sensor data!')
        major = sensordata_bytes[0]
        minor = sensordata_bytes[1]
        build = sensordata_bytes[2]
        self.fw_version = f"{major}.{minor}.{build}"
        self.water_pressure = self._to_folat(sensordata_bytes[3:7])
        self.water_temperature = self._to_folat(sensordata_bytes[7:11])
        self.air_pressure = self._to_folat(sensordata_bytes[11:15])
        self.air_temperature = self._to_folat(sensordata_bytes[15:19])
        self.battery = sensordata_bytes[19]

    def _to_folat(self, bytes: bytes) -> float:
        return struct.unpack('<f', bytes)[0]

    def print(self):
        print(f"FwVersion:{self.fw_version}")
        print(f"WaterPressure:{self.water_pressure}")
        print(f"WaterTemperature:{self.water_temperature}")
        print(f"AirPressure:{self.air_pressure}")
        print(f"AirTempreture:{self.air_temperature}")
        print(f"Battery:{self.battery}")
