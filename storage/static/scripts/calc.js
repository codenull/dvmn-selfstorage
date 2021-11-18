//TODO: загрузка данных по складам и тарифам с бэкенда.
const storages = getStorages();

const elStorageTime = document.getElementById('storageTime');
const elStorageSize = document.getElementById('storageSize');
const elStorageTimeLabel = document.getElementById('storageTimeLabel');
const elStorageSizeLabel = document.getElementById('storageSizeLabel');
const elStoragePrice = document.getElementById('storagePrice');
const elSelectedStorage = document.getElementById('selectedStorage');


function getStorages() {
    let storageList = [
        {
            'id': 1,
            'name': 'Воронеж-Фрахт',
            'address': 'Воронеж, ул. Минская д. 16',
            'description': '',
            'picture': '',
            'first_square_meter_price': 599,
            'rest_meters_price': 150
        },
        {
            'id': 2,
            'name': 'Каскад-Воронеж',
            'address': 'Воронеж, ул. Ленина д. 5',
            'description': '',
            'picture': '',
            'first_square_meter_price': 400,
            'rest_meters_price': 100
        },
        {
            'id': 3,
            'name': 'Кладовка ООО',
            'address': 'Воронеж, ул. Ворошилова д. 104',
            'description': '',
            'picture': '',
            'first_square_meter_price': 450,
            'rest_meters_price': 120
        },
    ];

    return storageList;
}

function fillStorageList() {
    
    for (const storage of storages) {
        let newOption = document.createElement('option');
        newOption.value = storage.id;
        newOption.text = `${storage.name} (${storage.address})`;
        elSelectedStorage.add(newOption, null);
    }

    if(storages.length> 0){
        elSelectedStorage.value = storages[0].id;
    }

}

function getStorageById(id) {
    let findedStorage = null;

    for (const storage of storages) {
        if(storage.id == id){
            findedStorage = storage;
            break;
        }
    }

    return findedStorage;
}

function calcPrice() {
    let storage = getStorageById(elSelectedStorage.value);
    if(!storage){  
        elStoragePrice.textContent = ``;
        return;
    }

    elStorageTimeLabel.textContent = `${elStorageTime.value}`;
    elStorageSizeLabel.textContent = `${elStorageSize.value}`;

    if(elStorageTime.value == 0) return;
    storagePrice = (storage.first_square_meter_price + (elStorageSize.value - 1) * storage.rest_meters_price) * elStorageTime.value;
    elStoragePrice.textContent = `${storagePrice} руб`;
}


elStorageTime.addEventListener('input', calcPrice);
elStorageSize.addEventListener('input', calcPrice);
elSelectedStorage.addEventListener('input', calcPrice);

fillStorageList();
calcPrice();