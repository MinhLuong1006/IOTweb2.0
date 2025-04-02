import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-database.js";

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

// Reference Room 1 sensor values
const tempRef = ref(db, "b1/r1/temp1");
const smokeRef = ref(db, "b1/r1/smoke1");
const flameRef = ref(db, "b1/r1/flame1");

let fireAlertShown = false; // Prevent multiple alerts

// Function to check fire condition for Room 1
function checkFireCondition(temp, smoke, flame) {
    if (flame > 0 || smoke > 50 || temp >= 50) {
        if (!fireAlertShown) {
            Swal.fire({
                title: "🔥 Fire Alert! 🔥",
                text: "Fire detected in Room 1!",
                icon: "warning",
                confirmButtonText: "OK",
                timer: 10000
            });
            fireAlertShown = true;
        }
    } else {
        fireAlertShown = false; // Reset alert when conditions return to normal
    }
}

// Listen for sensor value changes
onValue(tempRef, snapshot => {
    const temp = snapshot.val();
    checkFireCondition(temp, window.smoke1 || 0, window.flame1 || 0);
});

onValue(smokeRef, snapshot => {
    const smoke = snapshot.val();
    window.smoke1 = smoke; // Store the value globally
    checkFireCondition(window.temp1 || 0, smoke, window.flame1 || 0);
});

onValue(flameRef, snapshot => {
    const flame = snapshot.val();
    window.flame1 = flame; // Store the value globally
    checkFireCondition(window.temp1 || 0, window.smoke1 || 0, flame);
});
