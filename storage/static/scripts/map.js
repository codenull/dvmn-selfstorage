const storageLocations = JSON.parse(
    document.getElementById("storage-locations").textContent
);

const storagesMap = L.map('map').setView(
    storageLocations.town.location, 11
);

L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {attribution: '&copy; <a rel="nofollow" href="http://osm.org/copyright">OpenStreetMap</a>contributors'}
).addTo(storagesMap);

const addStorageOnMap = storage => {
    L.marker(storage.location).addTo(storagesMap).bindPopup(
        storage.short_description
    );
};

storageLocations.storages.forEach(storage => {
    addStorageOnMap(storage);
});
