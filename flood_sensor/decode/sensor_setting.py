import base64
from datetime import datetime, time
from enum import Enum
import struct


class AliveType(Enum):
    Monthry = (b'\x00', "日時スケジュール")
    Interval = (b'\x01', "インターバル")
    Daily = (b'\x02', "毎日スケジュール")
    Off = (b'\x03', "OFF")
    Unknown = (b'\xff', "不明")


class AliveSetting:
    name: str
    value: bytes
    description: str

    def __init__(self, value: bytes):
        e = next(filter(lambda e: e.value[0] == value, AliveType), AliveType.Unknown)
        self.name = e.name
        self.value = e.value[0]
        self.description = e.value[1]

    def __str__(self):
        return f'name: {self.name}, value: {self.value}, description: {self.description}'


class ScheduleSetting:
    _bytes_data_map = {
        'Monthly': 3,
        'Daily': 2
    }

    _size: int = 60

    daily_schedule: list = []
    monthly_schedule: list = []

    def __init__(self, schedule_setting_bytes: bytes, schedule_type: str):
        if len(schedule_setting_bytes) != self._size:
            raise ValueError('invalid schedule setting!')
        if schedule_type not in self._bytes_data_map:
            raise ValueError('invalid parameter!')
        max_n_schedules = int(self._size/self._bytes_data_map[schedule_type])
        interval_bytes = self._bytes_data_map[schedule_type]
        for i in range(0, self._size, interval_bytes):
            schedule_bytes = schedule_setting_bytes[i:i+interval_bytes]
            if schedule_bytes == b'\xff\xff':
                continue
            if schedule_type == 'Monthly':
                day = schedule_bytes[0]
                hour = int.from_bytes(schedule_bytes[1:3]) // 60
                min = int.from_bytes(schedule_bytes[1:3]) % 60
                self.monthly_schedule.append(datetime(2022, 1, day, hour, min))
            elif schedule_type == 'Daily':
                hour = int.from_bytes(
                    schedule_bytes[0:2], byteorder='little') // 60
                min = int.from_bytes(
                    schedule_bytes[0:2], byteorder='little') % 60
                self.daily_schedule.append(time(hour, min))

    def __str__(self):
        ret = ''
        for i, ms in enumerate(self.monthly_schedule):
            ts = ms.strftime('%d %H:%M')
            ret += f'MonthlySchedule{i}: {ts}\n'
        for i, ds in enumerate(self.daily_schedule):
            ts = ds.strftime('%H:%M')
            ret += f'DailySchedule{i}: {ts}\n'
        return ret


class FloodSensorSetting:
    cable_length: int
    send_start_waterlevel: float
    send_interval: int
    alive_setting: AliveSetting
    interval: int
    schedule_setting: ScheduleSetting
    fw_version: str
    hw_version: str
    battery: int
    sys_status: str

    def _to_folat(self, bytes: bytes) -> float:
        return struct.unpack('<f', bytes)[0]

    def __init__(self, sensor_setting_base64):
        sensor_setting_bytes = base64.b64decode(
            sensor_setting_base64, validate=True)
        if len(sensor_setting_bytes) != 166:
            raise ValueError('invalid sensor setting!')
        self.cable_length = int.from_bytes(sensor_setting_bytes[0:2], 'little')
        self.send_start_waterlevel = self._to_folat(sensor_setting_bytes[2:6])
        self.send_interval = int.from_bytes(
            sensor_setting_bytes[6:10], 'little')
        self.alive_setting = AliveSetting(
            sensor_setting_bytes[10].to_bytes(1, byteorder='little'))
        if self.alive_setting.name == AliveType.Unknown:
            raise ValueError('invalid alive setting!')
        self.schedule_setting = ScheduleSetting(
            sensor_setting_bytes[15:75], self.alive_setting.name)
        reserve = sensor_setting_bytes[75:158]
        fw_major = sensor_setting_bytes[158]
        fw_minor = sensor_setting_bytes[159]
        fw_build = sensor_setting_bytes[160]
        self.fw_version = f'{fw_major}.{fw_minor}.{fw_build}'
        hw_major = sensor_setting_bytes[161]
        hw_minor = sensor_setting_bytes[162]
        hw_build = sensor_setting_bytes[163]
        self.hw_version = f'{hw_major}.{hw_minor}.{hw_build}'
        self.battery = sensor_setting_bytes[164]
        self.sys_status = hex(sensor_setting_bytes[165])

    def __str__(self):
        return f'CableLength: {self.cable_length}\n' + \
            f'SendStartWaterlevel: {self.send_start_waterlevel}\n' + \
            f'SendInterval: {self.send_interval}\n' + \
            f'AliveSetting: {self.alive_setting.name}\n' + \
            f'{self.schedule_setting}' + \
            f"FwVersion: {self.fw_version}\n" +\
            f"HwVersion: {self.hw_version}\n" +\
            f"Battery: {self.battery}\n" +\
            f"SysStatus: {self.sys_status}\n"
