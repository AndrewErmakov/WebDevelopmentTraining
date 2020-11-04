ymaps.ready(init);
function init(){
    // Создание карты.
    var myMap = new ymaps.Map("map", {
        center: [56.830093, 60.553628],
        zoom: 13,
        controls: ['zoomControl'],
        behaviors: ['drag']
    });

    // Создание экземпляра метки
    var placemark = new ymaps.Placemark([56.83, 60.55], {
        hintContent: 'ул.Крауля 57',
        balloonContent: 'Пункт самовывоза'
    });

    myMap.geoObjects.add(placemark);
}