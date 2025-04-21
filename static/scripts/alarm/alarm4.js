import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-database.js";

// Firebase Config
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

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const alarmRef4 = ref(db, "real_alarm4");

let fireAlertInterval = null;

onValue(alarmRef4, snapshot => {
    const alarmState = snapshot.val();

    if (alarmState === 1 && !fireAlertInterval) {
        fireAlertInterval = setInterval(() => {
            Swal.fire({
                title: "🔥 Fire Alert!",
                text: "Room 4 is on fire!",
                icon: "warning",
                timer: 5000,
                showConfirmButton: false,
                toast: true,
                position: "top-end",
                background: "#ff4d4d",
                color: "#fff"
            });

            const alarmAudio = document.getElementById("fireAlarmSound");
            alarmAudio.play().catch(error => console.log("Autoplay blocked:", error));

            setTimeout(() => {
                alarmAudio.pause();
                alarmAudio.currentTime = 0;
            }, 5000);
        }, 6000);
    } else if (alarmState === 0 && fireAlertInterval) {
        clearInterval(fireAlertInterval);
        fireAlertInterval = null;

        Swal.fire({
            title: "✅ Fire Cleared",
            text: "Room 4 is safe now.",
            icon: "success",
            timer: 3000,
            showConfirmButton: false,
            toast: true,
            position: "top-end",
            background: "#28a745",
            color: "#fff"
        });
    }
});