let temp = 0; // Initial temperature
let alarmSound = document.getElementById("alarmSound");
let alarmInterval = null; // Store interval ID
console.log("dashboard.js loaded successfully!");

function showTemp() {
    document.getElementById("number-display").textContent = "Temp: " + temp + "°C";
}
setInterval(showTemp, 500);
function updateTheme() {
    if (temp > 5) {
        document.body.classList.add("fire");
        document.body.classList.remove("light-mode");
        document.getElementById("hotMessage").style.display = "block";
    } else {
        document.body.classList.add("light-mode");
        document.body.classList.remove("fire");
        document.getElementById("hotMessage").style.display = "none";
    }
}

function increaseTemp() {
    temp++;
    console.log("Temperature:", temp);
    updateTheme();
    
    if (temp > 5 && !alarmInterval) {
        startAlarm();
    }
}

function decreaseTemp() {
    temp--;
    console.log("Temperature:", temp);
    updateTheme();

    if (temp <= 5) {
        stopAlarm();
    }
}

function resetTemp() {
    temp = 0;
    console.log("Temperature reset:", temp);
    updateTheme();
    stopAlarm();
}

function startAlarm() {
    if (!alarmInterval) {
        alarmSound.play();
        alarmInterval = setInterval(() => {
            if (temp > 5) {
                alarmSound.play();
            } else {
                stopAlarm();
            }
        }, 1000); // Adjust time as needed
    }
}

function stopAlarm() {
    clearInterval(alarmInterval);
    alarmInterval = null;
    alarmSound.pause();
    alarmSound.currentTime = 0; // Reset sound
}