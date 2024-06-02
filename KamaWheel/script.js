const positions = {
    low: {
        foreplay: ["Position 1", "Position 2", "Position 3"],
        intercourse: ["Position 4", "Position 5", "Position 6"],
        climax: ["Position 7", "Position 8", "Position 9"]
    },
    medium: {
        foreplay: ["Position 10", "Position 11", "Position 12"],
        intercourse: ["Position 13", "Position 14", "Position 15"],
        climax: ["Position 16", "Position 17", "Position 18"]
    },
    high: {
        foreplay: ["Position 19", "Position 20", "Position 21"],
        intercourse: ["Position 22", "Position 23", "Position 24"],
        climax: ["Position 25", "Position 26", "Position 27"]
    }
};

const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");
const spinButton = document.getElementById("spinButton");
const intensitySelect = document.getElementById("intensity");
const momentSelect = document.getElementById("moment");
const resultDiv = document.getElementById("result");

let currentAngle = 0;
let isSpinning = false;

function drawWheel(segments, angleOffset = 0) {
    const arcSize = (2 * Math.PI) / segments.length;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    segments.forEach((segment, index) => {
        const angle = index * arcSize + angleOffset;
        ctx.beginPath();
        ctx.arc(250, 250, 250, angle, angle + arcSize);
        ctx.lineTo(250, 250);
        ctx.fillStyle = index % 3 === 0 ? "#f9c74f" : index % 3 === 1 ? "#90be6d" : "#f94144";
        ctx.fill();
        ctx.save();

        ctx.translate(250 + Math.cos(angle + arcSize / 2) * 150, 250 + Math.sin(angle + arcSize / 2) * 150);
        ctx.rotate(angle + arcSize / 2);
        ctx.fillStyle = "#333";
        ctx.fillText(segment, -ctx.measureText(segment).width / 2, 0);
        ctx.restore();
    });
}

function getRandomPosition(positionsArray) {
    const randomIndex = Math.floor(Math.random() * positionsArray.length);
    return positionsArray[randomIndex];
}

function spinWheel() {
    if (isSpinning) return;

    const intensity = intensitySelect.value;
    const moment = momentSelect.value;
    const selectedPositions = positions[intensity][moment];
    const chosenPosition = getRandomPosition(selectedPositions);

    let spinDuration = 3000; // Spin for 3 seconds
    let start = null;

    function rotate(timestamp) {
        if (!start) start = timestamp;
        let progress = timestamp - start;
        let remainingTime = Math.max(spinDuration - progress, 0);

        currentAngle += remainingTime / 1000;
        drawWheel(selectedPositions, currentAngle);

        if (progress < spinDuration) {
            requestAnimationFrame(rotate);
        } else {
            isSpinning = false;
            // Determine the selected position
            const arcSize = (2 * Math.PI) / selectedPositions.length;
            const selectedSegment = Math.floor((2 * Math.PI - (currentAngle % (2 * Math.PI))) / arcSize);
            resultDiv.textContent = "Selected Position: " + selectedPositions[selectedSegment];
        }
    }

    isSpinning = true;
    resultDiv.textContent = "";
    requestAnimationFrame(rotate);
}

spinButton.addEventListener("click", spinWheel);

drawWheel(["Low Intensity", "Medium Intensity", "High Intensity"]);
