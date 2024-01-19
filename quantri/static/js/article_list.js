//// chọn vùng ///////////////////////
    
    document.addEventListener('DOMContentLoaded', function() {
        var selectElement = document.querySelector('select#id_vung_trong');
        
        if (selectElement) {
            selectElement.addEventListener('change', function() {
                var selectedRegion = this.value;
                if (selectedRegion) {
                    // Variable selectedRegion has a value
                    console.log("selectedRegion has a value: " + selectedRegion);
                    var url = "{% url 'post:show_related_articles' %}?region_id=" + selectedRegion;
                    window.location.href = url;
                } else {
                    // Variable selectedRegion is empty
                    console.log("selectedRegion is empty");
                }
            });
        }
    });



