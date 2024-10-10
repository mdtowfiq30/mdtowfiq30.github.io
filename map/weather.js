const apiKey = 'fe13d6dc96ac9f2e34bbec6e7c656482'; // Your API key

// Function to fetch weather data based on the selected division
function fetchWeather(city) {
    document.getElementById('weather').innerHTML = '<p>Loading weather data...</p>';
    
    fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const temperature = data.main.temp;
            const description = data.weather[0].description;
            const humidity = data.main.humidity;
            const windSpeed = data.wind.speed;
            const icon = data.weather[0].icon;

            const weatherDiv = document.getElementById('weather');
            weatherDiv.innerHTML = `
                <h2>Weather in ${city}</h2>
                <p><strong>Temperature:</strong> ${temperature} °C</p>
                <p><strong>Description:</strong> ${description.charAt(0).toUpperCase() + description.slice(1)}</p>
                <p><strong>Humidity:</strong> ${humidity}%</p>
                <p><strong>Wind Speed:</strong> ${windSpeed} m/s</p>
                <img src="http://openweathermap.org/img/wn/${icon}@2x.png" alt="weather icon">
            `;
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            document.getElementById('weather').innerHTML = `
                <p>Unable to load weather data. Please try again later.</p>
            `;
        });
}

// Event listener to fetch weather data when the selected division changes
document.getElementById('divisionSelect').addEventListener('change', function() {
    const selectedDivision = this.value;
    fetchWeather(selectedDivision);  // Fetch weather data for selected division
});

// Fetch weather for the initial selected division
fetchWeather('Chittagong');  // Default division
