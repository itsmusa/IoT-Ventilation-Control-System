function updateTime() {
    let now = new Date();

    // Get current time in HH:MM format
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const time = `${hours}:${minutes}`;

    // Get current date in the format: Saturday, 02 Nov
    const options = { weekday: 'long', month: 'short', day: '2-digit' };
    const date = now.toLocaleDateString('en-US', options);

    document.getElementById('time').innerHTML = `${time}`;
    document.getElementById('date').innerHTML = `${date}`;
}
updateTime();
setInterval(updateTime, 60000); // Update every minute

// Retrieve system_data from localStorage or initialize an empty array
let system_data = JSON.parse(localStorage.getItem('system_data')) || [];

// Function to update fetched value
function updateFetchedValue(value) {
    let dateTime = new Date();
    const newData = {
        temperature: value['temperature'],
        humidity: value['humidity'],
        date_time: value['date_time']
    };

    // Ensure system_data does not exceed 50 entries
    if (system_data.length >= 50) {
        system_data.shift(); // Remove the oldest value
    }
    system_data.push(newData);

    localStorage.setItem('system_data', JSON.stringify(system_data));

    document.getElementById('tempValue').textContent = value['temperature'];
    document.getElementById('humValue').textContent = value['humidity'];
    document.getElementById('intakeValue').textContent = value['intake_speed'];
    document.getElementById('exhaustValue').textContent = value['exhaust_speed'];

    // Update temperature chart
    temperatureChart.data.labels.push(newData.date_time);
    temperatureChart.data.datasets[0].data.push(newData.temperature);
    if (temperatureChart.data.labels.length > 50) {
        temperatureChart.data.labels.shift();
        temperatureChart.data.datasets[0].data.shift();
    }
    temperatureChart.update();

    // Update humidity chart
    humidityChart.data.labels.push(newData.date_time);
    humidityChart.data.datasets[0].data.push(newData.humidity);
    if (humidityChart.data.labels.length > 50) {
        humidityChart.data.labels.shift();
        humidityChart.data.datasets[0].data.shift();
    }
    humidityChart.update();
}

// Initialize temperature chart
const temperatureCtx = document.getElementById('tempChart').getContext('2d');
const temperatureChart = new Chart(temperatureCtx, {
    type: 'line',
    data: {
        labels: system_data.map(data => data.date_time),
        datasets: [{
            label: 'Temperature (°C)',
            data: system_data.map(data => data.temperature),
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: false
        }]
    },
    options: {
        scales: {
            x: { title: { display: true, text: 'Time' } },
            y: { title: { display: true, text: 'Temperature (°C)' } }
        }
    }
});

// Initialize humidity chart
const humidityCtx = document.getElementById('humChart').getContext('2d');
const humidityChart = new Chart(humidityCtx, {
    type: 'line',
    data: {
        labels: system_data.map(data => data.date_time),
        datasets: [{
            label: 'Humidity (%)',
            data: system_data.map(data => data.humidity),
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: false
        }]
    },
    options: {
        scales: {
            x: { title: { display: true, text: 'Time' } },
            y: { title: { display: true, text: 'Humidity (%)' } }
        }
    }
})

async function fetchData(){
    try {
        const response = await fetch('/data'); // Replace with your URL
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json(); // Parse the JSON from the response
        // Handle the response data here
        console.log(data);
        updateFetchedValue(data);
    } catch (error) {
        console.error("Error fetching data: ", error); // Handle any errors here
    }
}
setInterval(fetchData, 10000);
