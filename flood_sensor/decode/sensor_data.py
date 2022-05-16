import base64
import struct


class FloodSensorData:
    fw_version: str
    water_pressure: float
    water_temperature: float
    air_pressure: float
    air_temperature: float
    battery: int

    def __init__(self, sensor_data_base64):
        sensor_data_bytes = base64.b64decode(sensor_data_base64, validate=True)
        if len(sensor_data_bytes) != 20:
            raise ValueError('invalid sensor data!')
        major = sensor_data_bytes[0]
        minor = sensor_data_bytes[1]
        build = sensor_data_bytes[2]
        self.fw_version = f"{major}.{minor}.{build}"
        self.water_pressure = self._to_folat(sensor_data_bytes[3:7])
        self.water_temperature = self._to_folat(sensor_data_bytes[7:11])
        self.air_pressure = self._to_folat(sensor_data_bytes[11:15])
        self.air_temperature = self._to_folat(sensor_data_bytes[15:19])
        self.battery = sensor_data_bytes[19]

    def _to_folat(self, bytes: bytes) -> float:
        return struct.unpack('<f', bytes)[0]

    def __str__(self) -> str:
        return f"FwVersion: {self.fw_version}\n" +\
            f"WaterPressure: {self.water_pressure}\n" +\
            f"WaterTemperature: {self.water_temperature}\n" +\
            f"AirPressure: {self.air_pressure}\n" +\
            f"AirTempreture: {self.air_temperature}\n" +\
            f"Battery: {self.battery}\n"
