// weather.js
// Định nghĩa đối tượng JavaScript chứa URL hình ảnh tùy thuộc vào tình trạng thời tiết
var weatherIcons = {
    "Clear": "https://nchmf.gov.vn/Upload/WeatherSymbol/icon_resized/2501.png", //nóng
    "Rain": "https://nchmf.gov.vn/Upload/WeatherSymbol/icon_resized/2301.png", //mưa
    "Clouds": "https://nchmf.gov.vn/Upload/WeatherSymbol/icon_resized/2001.png" //lạnh
};

// Hàm JavaScript để cập nhật hình ảnh dựa trên tình trạng thời tiết và chỉ số
function updateWeatherIcon(index) {
    var weatherStatus = document.getElementById("weather-status-" + index).textContent;
    //sử dụng weatherStatusc để tìm key trùng trong weatherIcons
    var imageUrl = weatherIcons[weatherStatus];
    var imgElement = document.getElementById("weather-icon-" + index);
    if (imgElement) {
        imgElement.src = imageUrl;
    }
}
