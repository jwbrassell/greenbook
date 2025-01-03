// Your OpenWeatherMap API key (you'll need to sign up at https://openweathermap.org/api)
const API_KEY = 'YOUR_API_KEY_HERE';

// Base URL for OpenWeatherMap API
const BASE_URL = 'https://api.openweathermap.org/data/2.5';

// Weather icon mappings to Weather Icons classes
const WEATHER_ICONS = {
    '01d': 'wi-day-sunny',
    '01n': 'wi-night-clear',
    '02d': 'wi-day-cloudy',
    '02n': 'wi-night-cloudy',
    '03d': 'wi-cloud',
    '03n': 'wi-cloud',
    '04d': 'wi-cloudy',
    '04n': 'wi-cloudy',
    '09d': 'wi-showers',
    '09n': 'wi-showers',
    '10d': 'wi-day-rain',
    '10n': 'wi-night-rain',
    '11d': 'wi-thunderstorm',
    '11n': 'wi-thunderstorm',
    '13d': 'wi-snow',
    '13n': 'wi-snow',
    '50d': 'wi-fog',
    '50n': 'wi-fog'
};

// Add event listener for Enter key in search input
document.getElementById('city-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        getWeather();
    }
});

// Main function to fetch weather data
async function getWeather() {
    // Get the city name from input
    const cityInput = document.getElementById('city-input');
    const city = cityInput.value.trim();
    
    // Clear any previous error messages
    const errorDiv = document.getElementById('error-message');
    errorDiv.style.display = 'none';
    
    // Validate input
    if (!city) {
        showError('Please enter a city name');
        return;
    }
    
    try {
        // Show loading state
        document.body.classList.add('loading');
        
        // Fetch current weather
        const weatherData = await fetchWeatherData(city);
        
        // Fetch 5-day forecast
        const forecastData = await fetchForecastData(city);
        
        // Update the UI with the weather data
        updateWeatherUI(weatherData);
        
        // Update the forecast section
        updateForecastUI(forecastData);
        
        // Show the weather container
        document.getElementById('weather-container').style.display = 'block';
        
    } catch (error) {
        showError('Could not fetch weather data. Please try again.');
        console.error('Error:', error);
    } finally {
        // Hide loading state
        document.body.classList.remove('loading');
    }
}

// Fetch current weather data from API
async function fetchWeatherData(city) {
    const response = await fetch(
        `${BASE_URL}/weather?q=${encodeURIComponent(city)}&units=metric&appid=${API_KEY}`
    );
    
    if (!response.ok) {
        throw new Error('Weather data not found');
    }
    
    return response.json();
}

// Fetch 5-day forecast data from API
async function fetchForecastData(city) {
    const response = await fetch(
        `${BASE_URL}/forecast?q=${encodeURIComponent(city)}&units=metric&appid=${API_KEY}`
    );
    
    if (!response.ok) {
        throw new Error('Forecast data not found');
    }
    
    return response.json();
}

// Update the UI with current weather data
function updateWeatherUI(data) {
    // Update city name
    document.getElementById('city-name').textContent = `${data.name}, ${data.sys.country}`;
    
    // Update temperature
    document.getElementById('temperature').textContent = 
        Math.round(data.main.temp);
    
    // Update weather icon
    const iconCode = data.weather[0].icon;
    const iconClass = WEATHER_ICONS[iconCode] || 'wi-day-sunny';
    document.getElementById('weather-icon').className = `wi ${iconClass}`;
    
    // Update description
    document.getElementById('description').textContent = 
        data.weather[0].description;
    
    // Update details
    document.getElementById('humidity').textContent = 
        `${data.main.humidity}%`;
    document.getElementById('wind-speed').textContent = 
        `${Math.round(data.wind.speed)} m/s`;
    document.getElementById('pressure').textContent = 
        `${data.main.pressure} hPa`;
}

// Update the UI with forecast data
function updateForecastUI(data) {
    const forecastDiv = document.getElementById('forecast');
    forecastDiv.innerHTML = ''; // Clear previous forecast
    
    // Get one forecast per day (data is in 3-hour intervals)
    const dailyForecasts = data.list.filter(item => 
        item.dt_txt.includes('12:00:00')
    ).slice(0, 5);
    
    // Create forecast items
    dailyForecasts.forEach(forecast => {
        const date = new Date(forecast.dt * 1000);
        const iconCode = forecast.weather[0].icon;
        const iconClass = WEATHER_ICONS[iconCode] || 'wi-day-sunny';
        
        const forecastItem = document.createElement('div');
        forecastItem.className = 'forecast-item';
        forecastItem.innerHTML = `
            <div class="date">${formatDate(date)}</div>
            <i class="wi ${iconClass}"></i>
            <div class="temp">${Math.round(forecast.main.temp)}°C</div>
            <div class="desc">${forecast.weather[0].description}</div>
        `;
        
        forecastDiv.appendChild(forecastItem);
    });
}

// Format date for forecast display
function formatDate(date) {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    return `${days[date.getDay()]} ${date.getDate()}`;
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    document.getElementById('weather-container').style.display = 'none';
}

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    // You could add default city weather here
    // getWeather('London');
});
