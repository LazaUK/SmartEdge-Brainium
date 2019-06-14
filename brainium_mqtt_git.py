import uuid
import json

# MQTT client libraries
import paho.mqtt.client as mqtt

# Azure IoT SDK libraries
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# Azure connection parameters
CONNECTION_STRING = '<<--STUB-->>'  # copy and paste here your Azure IoT Hub connection string
PROTOCOL = IoTHubTransportProvider.MQTT
azureclient = IoTHubClient(CONNECTION_STRING, PROTOCOL)
azureclient.set_option("auto_url_encode_decode", True)

# Brainium connection parameters
mqtt_user_name = 'oauth2-user'
mqtt_password = '<<--STUB-->>'  # copy and paste here external client id from your account
user_id = '<<--STUB-->>'  # copy and paste here your user id
device_id = '<<--STUB-->>'  # copy and paste here your device id

motion_datasource_topic = '/v1/users/{user_id}/in/devices/{device_id}/datasources/MOTION'.format(
    user_id=user_id,
    device_id=device_id)

ca_cert_path = 'cacert.crt'

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected to SmartEdge device. Returned code={r_code}".format(r_code=rc))
    else:
        print("Bad connection to SmartEdge. Returned code={r_code}".format(r_code=rc))

def on_message(client, userdata, msg):
    my_payload = json.loads(msg.payload.decode("utf-8")[1:-1])
    print('Msg received from topic={topic}\n{content}'.format(topic=msg.topic, content=my_payload))
    
    if my_payload["name"] == "Tick":
        print("\n---- Tick motion detected. Transferring data to Azure IoT backend ----")  
        msg_txt = "{\"deviceId\": \"%s\", \"probability\": %.2f}" % (my_payload["deviceId"], my_payload["selfProbability"])
        # print( "Compiled message: %s" % msg_txt )

        try:                       
            # Send the message to Azure IoT Hub.            
            message = IoTHubMessage(msg_txt)
            message.set_content_type_system_property("application/json")    
            # print(message.get_content_type_system_property())         
            print( "Sending message: %s" % message.get_string() )                   
            azureclient.send_event_async(message, send_confirmation_callback, None)
        except IoTHubError as iothub_error:
            print ( "Unexpected error %s from IoTHub" % iothub_error )
            return

def main():
    client = mqtt.Client(client_id=str(uuid.uuid4()), transport='websockets')
    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_set(ca_certs=ca_cert_path)
    client.username_pw_set(mqtt_user_name, mqtt_password)
    client.connect('ns01-wss.brainium.com', 443)

    client.subscribe(motion_datasource_topic)
    client.loop_forever()

if __name__ == "__main__":
    main()
