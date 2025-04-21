// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-database.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyB-ENheeyuJs8GFQVzFNq1silxSIQk8TbM",
    authDomain: "esp32-fire-alarm-a8fc5.firebaseapp.com",
    databaseURL: "https://esp32-fire-alarm-a8fc5-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "esp32-fire-alarm-a8fc5",
    storageBucket: "esp32-fire-alarm-a8fc5.firebasestorage.app",
    messagingSenderId: "138078759671",
    appId: "1:138078759671:web:06b4af915ffd11839681f2",
    measurementId: "G-ZZW6Q5DB2S"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// Utility function to update values in the HTML
function updateSensorValues(roomId, data, tempKey, smokeKey, flameKey) {
  document.getElementById(`${roomId}-temp`).textContent = data[tempKey] + "°C";
  document.getElementById(`${roomId}-smoke`).textContent = data[smokeKey];
  document.getElementById(`${roomId}-flame`).textContent = data[flameKey];
}

// ROOM 1: b1/r1/temp1, smoke1, flame1
onValue(ref(db, 'b1/r1'), (snapshot) => {
  const data = snapshot.val();
  updateSensorValues("room1", data, "temp1", "smoke1", "flame1");
});

// ROOM 2: b1/r2/temp2, smoke2, flame2
onValue(ref(db, 'b1/r2'), (snapshot) => {
  const data = snapshot.val();
  updateSensorValues("room2", data, "temp2", "smoke2", "flame2");
});

// ROOM 3: b2/r3/temp3, smoke3, flame3
onValue(ref(db, 'b2/r3'), (snapshot) => {
  const data = snapshot.val();
  updateSensorValues("room3", data, "temp3", "smoke3", "flame3");
});

// ROOM 4: b2/r4/temp4, smoke4, flame4
onValue(ref(db, 'b2/r4'), (snapshot) => {
  const data = snapshot.val();
  updateSensorValues("room4", data, "temp4", "smoke4", "flame4");
});