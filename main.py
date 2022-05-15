from webhook_form import WebhookForm
from flood_sensor.decode.sensor_data import FloodSensorData


def load_webhook(webhook_path) -> WebhookForm:
    try:
        with open(webhook_path, 'r') as webhook_file:
            return WebhookForm.from_json(webhook_file.read())
    except Exception as error:
        raise error


def decode_flood_sensor_data():
    try:
        webhook_form = load_webhook('./flood_sensor/webhook/sensor_data.json')
        sensor_id = webhook_form.device.sensor_id
        sensordata_base64 = webhook_form.device.data['data']

        if sensor_id == '00ff':
            print(FloodSensorData(sensordata_base64))
        else:
            print("it is not sensor data!")

    except ValueError as error:
        print(error)


def decode_flood_sensor_setting():
    """underconstruction"""


if __name__ == '__main__':
    decode_flood_sensor_data()
