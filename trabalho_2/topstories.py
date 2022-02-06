import time
import paho.mqtt.client as paho
from util import get_top_stories
import random

broker="mqtt.eclipseprojects.io"

def on_message(client, userdata, message):
    time.sleep(2)
    print("Mensagem  ==> ", str(message.payload.decode()))

def main():

    # try:
    client= paho.Client("client_1_on_hn")

    client.on_message=on_message


    print("Conectando ao broker",broker)
    client.connect(broker)
    client.loop_start()

    print("Subscrevendo no tópico de job stories do Hacker New(HN-JOB-STORIES) ")
    client.subscribe("HN-JOB-STORIES")
    time.sleep(1)

    print("Publicando os top stories no tópico HN-TOP-STORIES ")
    
    client.publish("HN-TOP-STORIES", str(get_top_stories(2)))
    time.sleep(6)

    client.disconnect()
    client.loop_stop()

    # except Exception as e:
    #     print('Exception on topstories mqtt client.')

if __name__ == '__main__':
    main()