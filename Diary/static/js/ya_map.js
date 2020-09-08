ymaps.ready(init);
function init(){
    var myMap = new ymaps.Map("map", {
        zoom: 13,
        controls: ['zoomControl'],
        behaviors: ['drag']
    });
    // Создание экземпляра метки
    var placemark = new ymaps.Placemark([56.83, 60.55], {
        hintContent: 'Место встречи',
        balloonContent: 'Детали встречи'
    });

    myMap.geoObjects.add(placemark);
}