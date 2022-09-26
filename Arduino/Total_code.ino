#include <Wire.h>
#include <BH1750.h>
#include "DHT.h"
#include "Adafruit_CCS811.h"
#include <WiFi.h>
#include "ThingSpeak.h"
#include "PubSubClient.h" 
#include "HTTPClient.h"

#include "Cipher.h"
  
Cipher * cipher = new Cipher();
  
Adafruit_CCS811 ccs;
BH1750 lightMeter(0x23);
char ssid[] = "esw-m19@iiith";
char pass[] = "e5W-eMai@3!20hOct";

//char ssid[] = "Yes2";
//char pass[] = "123456789";

unsigned long lastTime = 0;
unsigned long timerDelay = 30000;

WiFiClient  client;
void getLatestCI(String cnt)
{
  HTTPClient http;
  bool isBegin = http.begin("http://esw-onem2m.iiit.ac.in:443/~/in-cse/in-name/Team-9/" + cnt + "/Data/la");
  if(isBegin){
  http.addHeader("X-M2M-Origin", "X0yg4!:CpsfPb");
  http.addHeader("Content-Type", "application/json");
  int code = http.GET();
  String response = http.getString();
  Serial.println(code);
  Serial.println(response);
  if (code == -1) {
    Serial.println("UNABLE TO CONNECT TO THE SERVER");
  }
  http.end();
  }
  else
    Serial.println("Couldn't begin server!!");
}

void createCI(String& val, String cnt){
  HTTPClient http;
  bool isBegin = http.begin("http://esw-onem2m.iiit.ac.in:443/~/in-cse/in-name/Team-9/" + cnt + "/Data");
  if(isBegin){
  http.addHeader("X-M2M-Origin", "X0yg4!:CpsfPb");
  http.addHeader("Content-Type", "application/json;ty=4");
  String PostReq = "{\"m2m:cin\": {\"con\": \"" + String(val) + "\"}}";
  Serial.println(PostReq);
  int code = http.POST(PostReq);
  Serial.println(code);
  if (code == -1) {
    Serial.println("UNABLE TO CONNECT TO THE SERVER");
  }
  http.end();
  }
  else
    Serial.println("Couldn't begin server!!");
}

unsigned long myChannelField = 1837535; // Channel ID
const int ChannelLight = 1; // Which channel to write data
const int ChannelSoil = 2;
const int ChannelTemp = 3;
const int ChannelHum = 4;
const char * myWriteAPIKey = "XKRJFSYVSSB20Z7M";
#define DHTPIN 23
//BH1750 lightMeter;
#define DHTTYPE DHT22


#define AOUT_PIN 34
DHT dht(DHTPIN, DHTTYPE);

void setup(){

  
  Serial.begin(115200);
  char * key = "abcdefghijklmnop";
    cipher->setKey(key);
  
  // Initialize the I2C bus (BH1750 library doesn't do this automatically)
//  Wire.begin();
  WiFi.mode(WIFI_STA);
  
  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    while (WiFi.status() != WL_CONNECTED)
    {
      WiFi.begin(ssid, pass);
      Serial.print(".");
      delay(5000);
    }
    Serial.println("\nConnected.");
  }
  ThingSpeak.begin(client);
  dht.begin();
  Wire.begin();
  lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE, 0x23, &Wire);

  if(!ccs.begin(0x5A)){
    Serial.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }

  while(!ccs.available());
}

void loop() {

  // LIGHT SENSOR
  
  float lux = lightMeter.readLightLevel();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");
  delay(2000);
  
 //  TEMPERATURE AND HUMIDITY SENSOR

  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  delay(2000);
  
  // CAPACITIVE SOIL MOISTURE SENSOR

  int value = analogRead(AOUT_PIN); // read the analog value from sensor

  Serial.print("Moisture value: ");
  Serial.println(value);
  
  delay(2000);
  float co2, tvoc;

  //VOC
     if(ccs.available()){
    if(!ccs.readData()){
      float temp = ccs.calculateTemperature();
      ccs.setTempOffset(temp - 25.0);
      co2 = ccs.geteCO2();
      tvoc = ccs.getTVOC();
      Serial.print("CO2: ");
      Serial.print(co2);
      Serial.print("ppm, TVOC: ");
      Serial.println(tvoc);
    }
    else{
      Serial.println("ERROR!");
    }
  }
Serial.println("CCS811 test");

  delay(500);
  ThingSpeak.setField(1, lux);
  ThingSpeak.setField(ChannelSoil, value);
  ThingSpeak.setField(ChannelTemp, t);
  ThingSpeak.setField( ChannelHum, h);
  ThingSpeak.setField(5, co2);
  ThingSpeak.setField(6, tvoc);
  ThingSpeak.writeFields(myChannelField, myWriteAPIKey);
   ThingSpeak.writeField(myChannelField, ChannelSoil, value, myWriteAPIKey);
    ThingSpeak.writeField(myChannelField, ChannelTemp, t, myWriteAPIKey);
     ThingSpeak.writeField(myChannelField, ChannelHum, h, myWriteAPIKey);
     ThingSpeak.writeField(myChannelField, 5, co2, myWriteAPIKey);
     ThingSpeak.writeField(myChannelField, 6, tvoc, myWriteAPIKey);
  delay(1000);

  if(millis() - lastTime > timerDelay)
  {
    String SoilVal = cipher->encryptString(String(value));
    createCI(SoilVal, "Node-2");
    String temp = cipher->encryptString(String(t));
    createCI(temp, "Node-3");
    String hum = cipher->encryptString(String(h));
    createCI(hum, "Node-4");
    String light = cipher->encryptString(String(lux));
    createCI(light, "Node-5");
    String tvc = cipher->encryptString(String(tvoc));
    createCI(tvc, "Node-6");
    String co = cipher->encryptString(String(co2));
    createCI(co, "Node-7");

    getLatestCI("Node-2");
    getLatestCI("Node-3");
    getLatestCI("Node-4");
    getLatestCI("Node-5");
    getLatestCI("Node-6");
    getLatestCI("Node-7");
    lastTime = millis();  
  }

}
