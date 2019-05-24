# relais-button-docker-arm
Docker to provide a relais-switch-actor listening on a mqtt topic
Send "ON" to switch on
Send "OFF" to switch off

# build it 
docker build --rm -t jumajumo/relais_switch_on_off .

# run it
docker run -d --network="host" --privileged -e brokeraddr=192.168.0.150 -e thingid=swGaragedoor -e pin=17 --name "jumajumo_relais_switch_on_off" jumajumo/relais_switch_on_off

- --privileged: privileged is necessary in order to allow access to gpio
- -e brokeraddr: ip address of the mqtt broker (default port 1883 is used) (default "openhabian")
- -e thingid: thing id of the sensor (used for mqtt-topic) (default "actor")
- -e pin: the gpio pin used for the sensor (default 17)
- --name: give it a name
