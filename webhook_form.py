from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from xmlrpc.client import DateTime


@dataclass_json
@dataclass
class Application:
    application_id: str
    name: str


@dataclass_json
@dataclass
class Router:
    router_id: str
    imsi: str
    fw_version: str
    rssi: int = 0
    battery: int = 0


@dataclass_json
@dataclass
class Device:
    device_id: str
    sensor_id: str
    sensor_name: str
    rssi: int = 0
    data: dict = field(default_factory=None)


@dataclass_json
@dataclass
class WebhookForm:
    application: Application = None
    router: Router = None
    device: Device = None
    date: DateTime = None
    uplink_id: str = ''
