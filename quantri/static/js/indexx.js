// map goong.io

goongjs.accessToken = 'ItuJ0fjOr47yyCV7PPFIrqQ8dlDaxQNaCfIdxP8U';

var map = new goongjs.Map({
    container: 'map',
    style: 'https://tiles.goong.io/assets/goong_map_web.json',
    center: [105.71366, 16.26566],
    zoom: 4
});

// thêm chức năng tìm kiếm
map.addControl(
    new GoongGeocoder({
        accessToken: 'PDYJ9HcYG0hIx998OoH85Ab1nzBSncvaEoidMWxb',
        goongjs: goongjs
    })
);

// thêm chức năng zomm
map.addControl(new goongjs.NavigationControl());

// Tạo một danh sách dữ liệu điểm đánh dấu từ biến locationsData
const markers = [];

// Lấy danh sách vị trí từ biến locations
const locations = JSON.parse(document.getElementById('locations').getAttribute('data-locations'));

//locations là 1 mảng bắt đầu từ 0
console.log('test',locations)

// Sử dụng vòng lặp để thêm mỗi vị trí vào mảng markers
for (const location of locations) {
    markers.push({
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [location.Longitude, location.Latitude]
        },
        properties: {
            title: location.Name,
            description: `<p>Kinh tuyến: ${location.Latitude} </p>
            <p>Vĩ tuyến: ${location.Longitude}</p>`,
            fruitType: location.FruitType,
            fruit_name: location.fruit_name,
            id: location.id_article,
        }
    });
}

// Sử dụng biến markers để tạo các điểm đánh dấu
markers.forEach(marker => {
    const properties = marker.properties;

    // Tạo một điểm đánh dấu và đặt lớp CSS 'custom-marker'
    const customMarker = new goongjs.Marker({ element: createCustomMarkerElement() })
        .setLngLat(marker.geometry.coordinates)
        .setPopup(new goongjs.Popup()
            .setHTML(`<h3>${properties.title}</h3>
            <p>${properties.description}</p>
            <p> Cây trồng: ${properties.fruit_name}</p>
            <h3>${properties.fruitType}</h3> 
            <a href="/article_detail/${properties.id}">Xem bài viết </a>   
            
            `)
        )
        .addTo(map);

    // Thêm lớp CSS dựa trên giá trị `properties.fruitType`
    customMarker.getElement().classList.add(properties.fruitType); // lấy giá trị của properties.fruitType làm thuộc tính css
    // customMarker.getElement().classList.add('custom-marker');


});

function createCustomMarkerElement() {
    const customMarker = document.createElement('div');
    customMarker.className = 'custom-marker';
    return customMarker;
}


  /////js thông báo cmt
  document.addEventListener('DOMContentLoaded', function () {
  const notificationContainer = document.querySelector('#notification-container');
  const closeNotificationBtn = document.querySelector('#close-notification-container');
  const notificationIcon = document.querySelector('#notification-icon');

  // Bắt sự kiện khi người dùng nhấn vào notification-icon
  notificationIcon.addEventListener('click', function(event) {
      event.preventDefault();  // Ngăn chặn hành vi mặc định của thẻ <a>

      // Thực hiện các hành động khi notification-icon được nhấn
      // Ví dụ: Hiển thị hoặc ẩn thông báo
      notificationContainer.style.display = 'block'; // Hiển thị thông báo
  });
  closeNotificationBtn.addEventListener('click', () => {
      notificationContainer.style.display = 'none';
  });
});