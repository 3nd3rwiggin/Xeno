#include <Arduino.h>
#include <ArduinoWebsockets.h>
#include <ESP8266WiFi.h>

using namespace websockets;

class MyWebSocket {
public:
    MyWebSocket(const char* host, int port, const char* path)
        : host(host), port(port), path(path) {}

    void connect() {
        if (!webSocket.connected()) {
            webSocket.begin(host, port, path);
        }
    }

    void sendData(const char* name, const char* state) {
        String data = String("{\"type\":\"mcuinsert\",\"name\":\"") + name + "\",\"state\":\"" + state + "\"}";
        webSocket.send(data);
    }

    bool receiveData(String& msg) {
        webSocket.poll();
        if (webSocket.available()) {
            msg = webSocket.readMessage();
            return true;
        }
        return false;
    }

private:
    const char* host;
    int port;
    const char* path;
};

MyWebSocket myWebSocket("localhost", 8763, "/node");

void setup() {
    Serial.begin(115200);
    WiFi.begin("MyWifi", "secret");

    Serial.print("Connecting");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
}

void loop() {
    myWebSocket.connect();

    // Your data - adjust accordingly
    const char* name = "node6";
    const char* state = "1";

    myWebSocket.sendData(name, state);

    String msg;
    if (myWebSocket.receiveData(msg)) {
        Serial.println(msg);
    }

    delay(500);
}
