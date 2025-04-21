#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include "time.h"  // Include time library for timestamp

// Firebase Configuration
#define FIREBASE_HOST "https://esp32-fire-alarm-a8fc5-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define FIREBASE_AUTH "wMgwwBjo65VqlBb7AaNVKJHVlo0cvGFd4kxCPNhi"

// WiFi Credentials
#define WIFI_SSID "House"
#define WIFI_PASSWORD "1234512345"

// Firebase Objects
FirebaseData fbData;
FirebaseAuth auth;
FirebaseConfig config;



#define SMOKE_SENSOR_PIN1 33  
#define SMOKE_SENSOR_PIN2 32
#define SMOKE_SENSOR_PIN3 35  
#define SMOKE_SENSOR_PIN4 34

#define SMOKE_THRESHOLD 400  // Adjust based on sensitivity

// NTP Time Settings (for timestamp)
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 7 * 3600;  
const int daylightOffset_sec = 0;

void setup() {
  Serial.begin(115200);

  pinMode(SMOKE_SENSOR_PIN1, INPUT);
  pinMode(SMOKE_SENSOR_PIN2, INPUT);
  pinMode(SMOKE_SENSOR_PIN3, INPUT);
  pinMode(SMOKE_SENSOR_PIN4, INPUT);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nConnected to WiFi!");
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());

  // Initialize Firebase
  config.database_url = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  // Initialize NTP Time Sync
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

String getTimestamp() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return "Unknown Time";
  }
  char buffer[30];
  strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &timeinfo);
  return String(buffer);
}

void sendEventToFirebase(String eventType, String room) {
  String timestamp = getTimestamp();
  String globalPath = "/event_logs";

  FirebaseJson json;
  json.set("timestamp", timestamp);
  json.set("room", room);
  json.set("event", eventType);

  if (Firebase.RTDB.pushJSON(&fbData, globalPath, &json)) {
    //Serial.println("✅ Event logged in global logs: " + eventType + " in " + room);
  } else {
    Serial.print("❌ Firebase Error: ");
    Serial.println(fbData.errorReason());
  }

  String roomPath = "/room_logs/" + room;
  if (Firebase.RTDB.pushJSON(&fbData, roomPath, &json)) {
    //Serial.println("✅ Event logged in " + room + " logs.");
  } else {
    Serial.print("❌ Firebase Error: ");
    Serial.println(fbData.errorReason());
  }
}

void loop() {

  // Read Smoke Sensors
  int smokeStatus1 = analogRead(SMOKE_SENSOR_PIN1);
  int smokeStatus2 = analogRead(SMOKE_SENSOR_PIN2);
  int smokeStatus3 = analogRead(SMOKE_SENSOR_PIN3);
  int smokeStatus4 = analogRead(SMOKE_SENSOR_PIN4);
  Serial.print("r1: ");
  Serial.println(smokeStatus1);
  Serial.print("r2: ");
  Serial.println(smokeStatus2);
  Serial.print("r3: ");
  Serial.println(smokeStatus3);
  Serial.print("r4: ");
  Serial.println(smokeStatus4);

  static int previousSmoke1 = LOW;
  static int previousSmoke2 = LOW;
  static int previousSmoke3 = LOW;
  static int previousSmoke4 = LOW;

  if (smokeStatus1 > 1000 && previousSmoke1 == LOW) {

    Firebase.RTDB.setInt(&fbData, "/b1/r1/smoke1", 1);

  }
  if (smokeStatus1 <= 1000) {
    Firebase.RTDB.setInt(&fbData, "/b1/r1/smoke1", 0);
  }
  previousSmoke1 = (smokeStatus1 > 1000) ? HIGH : LOW;


  if (smokeStatus2 > 1000 && previousSmoke2 == LOW) {
   
    Firebase.RTDB.setInt(&fbData, "/b1/r2/smoke2", 1);

  }
  if (smokeStatus2 <= 1000) {
    Firebase.RTDB.setInt(&fbData, "/b1/r2/smoke2", 0);
  }
  previousSmoke2 = (smokeStatus2 > 1000) ? HIGH : LOW;


  if (smokeStatus3 > 1000 && previousSmoke3 == LOW) {
   
    Firebase.RTDB.setInt(&fbData, "/b2/r3/smoke3", 1);

  }
  if (smokeStatus3 <= 1000) {
    Firebase.RTDB.setInt(&fbData, "/b2/r3/smoke3", 0);
  }
  previousSmoke3 = (smokeStatus3 > 1000) ? HIGH : LOW;


  if (smokeStatus4 > 1000 && previousSmoke4 == LOW) {
  
    Firebase.RTDB.setInt(&fbData, "/b2/r4/smoke4", 1);

  }
  if (smokeStatus4 <= 1000) {
    Firebase.RTDB.setInt(&fbData, "/b2/r4/smoke4", 0);
  }
  previousSmoke4 = (smokeStatus4 > 1000) ? HIGH : LOW;

delay(1000);
}
