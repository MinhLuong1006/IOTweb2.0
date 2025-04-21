#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include "time.h"  // Include time library for timestamp
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>
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

#define FLAME_SENSOR_PIN1 23  
#define FLAME_SENSOR_PIN2 22
#define FLAME_SENSOR_PIN3 21  
#define FLAME_SENSOR_PIN4 19


// NTP Time Settings (for timestamp)
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 7 * 3600;  
const int daylightOffset_sec = 0;

// Cooldown settings (30 seconds)
unsigned long lastFireLogTime1 = 0;
unsigned long lastFireLogTime2 = 0;
unsigned long lastSmokeLogTime1 = 0;
unsigned long lastSmokeLogTime2 = 0;
const unsigned long logCooldown = 30000;  // 30 seconds

// DS18B20 Setup
#define ONE_WIRE_BUS1 32  // Change to the correct GPIO pin33
OneWire oneWire1(ONE_WIRE_BUS1);
DallasTemperature sensors1(&oneWire1);

#define ONE_WIRE_BUS2 33  // Change to the correct GPIO pin32
OneWire oneWire2(ONE_WIRE_BUS2);
DallasTemperature sensors2(&oneWire2);

#define ONE_WIRE_BUS3 26  // Change to the correct GPIO pin35
OneWire oneWire3(ONE_WIRE_BUS3);
DallasTemperature sensors3(&oneWire3);

#define ONE_WIRE_BUS4 27  // Change to the correct GPIO pin34
OneWire oneWire4(ONE_WIRE_BUS4);
DallasTemperature sensors4(&oneWire4);

  bool previousFireDetected1 = false;
  bool previousFireDetected2 = false;
  bool previousFireDetected3 = false;
  bool previousFireDetected4 = false;
  
int previousAlarm1 = 0;
int previousAlarm2 = 0;
int previousAlarm3 = 0;
int previousAlarm4 = 0;

void setup() {
  Serial.begin(115200);
  pinMode(FLAME_SENSOR_PIN1, INPUT);
  pinMode(FLAME_SENSOR_PIN2, INPUT);
  pinMode(FLAME_SENSOR_PIN3, INPUT);
  pinMode(FLAME_SENSOR_PIN4, INPUT);
  

//WIFI_SSID, WIFI_PASSWORD
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

  // Initialize DS18B20 Sensor
  sensors1.begin();
  sensors2.begin();
  sensors3.begin();
  sensors4.begin();

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

  // Log to global event logs
  String globalPath = "/event_logs";
  
  FirebaseJson json;
  json.set("timestamp", timestamp);
  json.set("room", room);
  json.set("event", eventType);

  if (Firebase.RTDB.pushJSON(&fbData, globalPath, &json)) {
    Serial.println("✅ Event logged in global logs: " + eventType + " in " + room);
  } else {
    Serial.print("❌ Firebase Error: ");
    Serial.println(fbData.errorReason());
  }

  // Log to specific room's event logs
  String roomPath = "/room_logs/" + room;  // Example: /room_logs/Room1
  if (Firebase.RTDB.pushJSON(&fbData, roomPath, &json)) {
    Serial.println("✅ Event logged in " + room + " logs.");
  } else {
    Serial.print("❌ Firebase Error: ");
    Serial.println(fbData.errorReason());
  }
    // Log to building logs
  if (room == "Room1" || room == "Room2") {
    String building1Path = "/building_logs/building1";
    if (Firebase.RTDB.pushJSON(&fbData, building1Path, &json)) {
      Serial.println("✅ Event logged in building1 logs.");
    } else {
      Serial.print("❌ Firebase Error: ");
      Serial.println(fbData.errorReason());
    }
  } else if (room == "Room3" || room == "Room4") {
    String building2Path = "/building_logs/building2";
    if (Firebase.RTDB.pushJSON(&fbData, building2Path, &json)) {
      Serial.println("✅ Event logged in building2 logs.");
    } else {
      Serial.print("❌ Firebase Error: ");
      Serial.println(fbData.errorReason());
    }
  }
}

void loop() {
  int flameStatus1 = digitalRead(FLAME_SENSOR_PIN1);
  int flameStatus2 = digitalRead(FLAME_SENSOR_PIN2);
  int flameStatus3 = digitalRead(FLAME_SENSOR_PIN3);
  int flameStatus4 = digitalRead(FLAME_SENSOR_PIN4);

  static int previousFire1 = HIGH;
  static int previousFire2 = HIGH;
  static int previousFire3 = HIGH;
  static int previousFire4 = HIGH;

  int smokeValue1 = 0;  // Declare here to be accessible later
  int smokeValue2 = 0;
  int smokeValue3 = 0;
  int smokeValue4 = 0; 



  sensors1.requestTemperatures(); 
    float temperature1 = sensors1.getTempCByIndex(0);

  sensors2.requestTemperatures(); 
    float temperature2 = sensors2.getTempCByIndex(0);

  sensors3.requestTemperatures(); 
    float temperature3 = sensors3.getTempCByIndex(0);

  sensors4.requestTemperatures(); 
    float temperature4 = sensors4.getTempCByIndex(0);
    
  if (flameStatus1 == LOW && previousFire1 == HIGH) {  
    Serial.println("🔥 Fire detected at Room 1!");
    Firebase.RTDB.setInt(&fbData, "/b1/r1/flame1", 1);

  }
  if (flameStatus1 == HIGH) {
    Firebase.RTDB.setInt(&fbData, "/b1/r1/flame1", 0);
  }
  previousFire1 = flameStatus1;

  if (flameStatus2 == LOW && previousFire2 == HIGH) {
    Serial.println("🔥 Fire detected at Room 2!");
    Firebase.RTDB.setInt(&fbData, "/b1/r2/flame2", 1);
   
  }
  if (flameStatus2 == HIGH) {
    Firebase.RTDB.setInt(&fbData, "/b1/r2/flame2", 0);
  }
  previousFire2 = flameStatus2;

  if (flameStatus3 == LOW && previousFire3 == HIGH) {  
    Serial.println("🔥 Fire detected at Room 3!");
    Firebase.RTDB.setInt(&fbData, "/b2/r3/flame3", 1);
   
  }
  if (flameStatus3 == HIGH) {
    Firebase.RTDB.setInt(&fbData, "/b2/r3/flame3", 0);
  }
  previousFire3 = flameStatus3;

  if (flameStatus4 == LOW && previousFire4 == HIGH) {
    Serial.println("🔥 Fire detected at Room 4!");
    Firebase.RTDB.setInt(&fbData, "/b2/r4/flame4", 1);
    
  }
  if (flameStatus4 == HIGH) {
    Firebase.RTDB.setInt(&fbData, "/b2/r4/flame4", 0);
  }
  previousFire4 = flameStatus4;

  static unsigned long lastTempUpload = 0;
  if (millis() - lastTempUpload > 1000) {
    
    
    // Upload to Firebase
    if (Firebase.RTDB.setFloat(&fbData, "/b1/r1/temp1", temperature1)) {
        Serial.println("✅ Temperature uploaded to Firebase!");
    } else {
        Serial.print("❌ Firebase Error: ");
        Serial.println(fbData.errorReason());
    }

    
    // Upload to Firebase
    if (Firebase.RTDB.setFloat(&fbData, "/b1/r2/temp2", temperature2)) {
        Serial.println("✅ Temperature uploaded to Firebase!");
    } else {
        Serial.print("❌ Firebase Error: ");
        Serial.println(fbData.errorReason());
    }

    if (Firebase.RTDB.setFloat(&fbData, "/b2/r3/temp3", temperature3)) {
        Serial.println("✅ Temperature uploaded to Firebase!");
    } else {
        Serial.print("❌ Firebase Error: ");
        Serial.println(fbData.errorReason());
    }

    
    // Upload to Firebase
    if (Firebase.RTDB.setFloat(&fbData, "/b2/r4/temp4", temperature4)) {
        Serial.println("✅ Temperature uploaded to Firebase!");
    } else {
        Serial.print("❌ Firebase Error: ");
        Serial.println(fbData.errorReason());
    }

    lastTempUpload = millis();
}

////////////////////////
if (Firebase.RTDB.getInt(&fbData, "/b1/r1/smoke1")) {
    smokeValue1 = fbData.intData();  // Store the value
    Serial.print("Smoke Value1: ");
    Serial.println(smokeValue1);
} else {
    Serial.print("Failed to read from Firebase: ");
    Serial.println(fbData.errorReason());  // Print error message
}

if (Firebase.RTDB.getInt(&fbData, "/b1/r2/smoke2")) {
    smokeValue2 = fbData.intData();  // Store the value
    Serial.print("Smoke Value2: ");
    Serial.println(smokeValue2);
} else {
    Serial.print("Failed to read from Firebase: ");
    Serial.println(fbData.errorReason());  // Print error message
}

if (Firebase.RTDB.getInt(&fbData, "/b2/r3/smoke3")) {
    smokeValue3 = fbData.intData();  // Store the value
    Serial.print("Smoke Value3: ");
    Serial.println(smokeValue3);
} else {
    Serial.print("Failed to read from Firebase: ");
    Serial.println(fbData.errorReason());  // Print error message
}

if (Firebase.RTDB.getInt(&fbData, "/b2/r4/smoke4")) {
    smokeValue4 = fbData.intData();  // Store the value
    Serial.print("Smoke Value4: ");
    Serial.println(smokeValue4);
} else {
    Serial.print("Failed to read from Firebase: ");
    Serial.println(fbData.errorReason());  // Print error message
}
////////////////////////////////
//BED
bool fireDetected1 = (flameStatus1 == LOW || smokeValue1 == 1 || temperature1 >= 50);

if (fireDetected1 && !previousFireDetected1) {
  Serial.println("🔥 NEW fire detected in Room 1!");
  Firebase.RTDB.setInt(&fbData, "/alarm1", 1);
  Firebase.RTDB.setInt(&fbData, "/alarm1_sensor", 1);
  sendEventToFirebase("Fire Detected", "Room1");
  previousFireDetected1 = true;
}
else if (!fireDetected1 && previousFireDetected1) {

  Firebase.RTDB.setInt(&fbData, "/alarm1_sensor", 0);
  previousFireDetected1 = false;
}

//LIVING
//smokeValue2 == 1 && flameStatus2 == LOW && temperature2 >= 60
bool fireDetected2 = (flameStatus2 == LOW || smokeValue2 == 1 || temperature2 >= 50);

if (fireDetected2 && !previousFireDetected2) {
  Serial.println("🔥 NEW fire detected in Room 2!");
  Firebase.RTDB.setInt(&fbData, "/alarm2", 1);
  Firebase.RTDB.setInt(&fbData, "/alarm2_sensor", 1);
  sendEventToFirebase("Fire Detected", "Room2");
  previousFireDetected2 = true;
}
else if (!fireDetected2 && previousFireDetected2) {

  Firebase.RTDB.setInt(&fbData, "/alarm2_sensor", 0);
  previousFireDetected2 = false;
}

//STORAGE
//smokeValue3 == 1 || flameStatus3 == LOW || temperature3 >= 70
bool fireDetected3 = (flameStatus3 == LOW || smokeValue3 == 1 || temperature3 >= 50);

if (fireDetected3 && !previousFireDetected3) {
  Serial.println("🔥 NEW fire detected in Room 3!");
  Firebase.RTDB.setInt(&fbData, "/alarm3", 1);
  Firebase.RTDB.setInt(&fbData, "/alarm3_sensor", 1);
  sendEventToFirebase("Fire Detected", "Room3");
  previousFireDetected3 = true;
}
else if (!fireDetected3 && previousFireDetected3) {

  Firebase.RTDB.setInt(&fbData, "/alarm3_sensor", 0);
  previousFireDetected3 = false;
}


//KITCHEN
//smokeValue4 == 1 && flameStatus4 == LOW && temperature4 >= 50
bool fireDetected4 = (flameStatus4 == LOW || smokeValue4 == 1 || temperature4 >= 50);

if (fireDetected4 && !previousFireDetected4) {
  Serial.println("🔥 NEW fire detected in Room 4!");
  Firebase.RTDB.setInt(&fbData, "/alarm4", 1);
  Firebase.RTDB.setInt(&fbData, "/alarm4_sensor", 1);
  sendEventToFirebase("Fire Detected", "Room4");
  previousFireDetected4 = true;
}
else if (!fireDetected4 && previousFireDetected4) {

  Firebase.RTDB.setInt(&fbData, "/alarm4_sensor", 0);
  previousFireDetected4 = false;
}

//////
// Check alarm1
if (Firebase.RTDB.getInt(&fbData, "/real_alarm1")) {
  int alarm1Value = fbData.intData();
  if (alarm1Value == 1 && previousAlarm1 == 0) {
    Serial.println("⚠️ Alarm1 triggered externally!");
    sendEventToFirebase("Alarm Triggered", "Room1");
  }
  previousAlarm1 = alarm1Value;
}

// Check alarm2
if (Firebase.RTDB.getInt(&fbData, "/real_alarm2")) {
  int alarm2Value = fbData.intData();
  if (alarm2Value == 1 && previousAlarm2 == 0) {
    Serial.println("⚠️ Alarm2 triggered externally!");
    sendEventToFirebase("Alarm Triggered", "Room2");
  }
  previousAlarm2 = alarm2Value;
}

// Check alarm3
if (Firebase.RTDB.getInt(&fbData, "/Real_alarm3")) {
  int alarm3Value = fbData.intData();
  if (alarm3Value == 1 && previousAlarm3 == 0) {
    Serial.println("⚠️ Alarm3 triggered externally!");
    sendEventToFirebase("Alarm Triggered", "Room3");
  }
  previousAlarm3 = alarm3Value;
}

// Check alarm4
if (Firebase.RTDB.getInt(&fbData, "/real_alarm4")) {
  int alarm4Value = fbData.intData();
  if (alarm4Value == 1 && previousAlarm4 == 0) {
    Serial.println("⚠️ Alarm4 triggered externally!");
    sendEventToFirebase("Alarm Triggered", "Room4");
  }
  previousAlarm4 = alarm4Value;
}

 delay(1000);
}