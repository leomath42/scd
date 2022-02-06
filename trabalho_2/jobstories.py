import time
import paho.mqtt.client as paho
from util import get_job_stories
import random

broker="mqtt.eclipseprojects.io"

def on_message(client, userdata, message):
    time.sleep(2)
    print("Mensagem ==> ", str(message.payload.decode()))

def main():

    # try:
    client= paho.Client("client_2_on_hn")

    client.on_message=on_message


    print("Conectando ao broker ",broker)
    client.connect(broker)
    client.loop_start()


    print("Subscrevendo no tópico de top stories do Hacker News(HN-TOP-STORIES) ")
    client.subscribe("HN-TOP-STORIES")
    time.sleep(1)

    print("Publicando os job stories no tópico HN-JOB-STORIES ")
    client.publish("HN-JOB-STORIES", str(get_job_stories(4)))
    time.sleep(6)

    client.disconnect()
    client.loop_stop()

    # except Exception as e:
    #     print('Exception on jobstories mqtt client.')

if __name__ == '__main__':
    main()