from webhook_form import WebhookForm
from flood_sensor.decode.sensor_data import FloodSensorData
import json


def decode_flood_sensor_data():
    try:
        with open('./flood_sensor/webhook/sensor_data.json', 'r') as webhook_file:
            webhookform = WebhookForm.from_json(webhook_file.read())
            sensor_id = webhookform.device.sensor_id
            sensordata_base64 = webhookform.device.data['data']

            if sensor_id == '00ff':
                FloodSensorData(sensordata_base64).print()
            else:
                print("it is not sensor data!")
    except ValueError as error:
        print(error)


def decode_flood_sensor_setting():
    """underconstruction"""


if __name__ == '__main__':
    decode_flood_sensor_data()
