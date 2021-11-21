const inventoryChoice = document.querySelector('#id_inventory');
const quantityBlock = document.querySelector('#quantity_block');
const quantity = document.querySelector('#id_quantity');
const storageBlock = document.querySelector('#storage_block');
const storageChoice = document.querySelector('#id_storage');
const pricesBlock = document.querySelector('#prices_block');
const startDate = document.querySelector('#id_start_service');
const endDate = document.querySelector('#id_end_service');
const dateBlock = document.querySelector('#date_block');
const totalPrice = document.querySelector('#totalPrice');
const totalPriceBlock = document.querySelector('#total_price_block');
const goToPaymentButton = document.querySelector('#go_to_payment');
 
let inventory;
let storage;

const calcTotalPrice = async () => {
    const start = startDate.value;
    const end = endDate.value;
    const weekPrice = Number.parseInt(
        document.querySelector('#weekPrice').textContent
    );
    const monthPrice = Number.parseInt(
        document.querySelector('#monthPrice').textContent
    );
    const response = await fetch(`/get_price/${start}/${end}`);
    const { months, weeks } = await response.json();
    console.log(
        'Кол-во месяцев хранения - ', months,
        '\nЦена за месяцы - ', monthPrice,
        '\nКол-во недель хранения - ', weeks,
        '\nЦена за недели -', weekPrice
    );
    const price = (months * monthPrice + weeks * weekPrice) * quantity.value;
    console.log('Цена - ', price);
    totalPrice.innerHTML = `${price}&#8381;`;
    return months * monthPrice + weeks * weekPrice;
}

const showQuantity = () => {
    quantityBlock.style.display = 'block';
}

const setStartDateAndCalcPrice = () => {
    // получаем значение даты начала хранения, которую установил пользователь
    const startDateValue = new Date(startDate.value);
    // получаем объект даты для минимально возможного времени аренды
    const minEndDate = new Date(startDateValue.getTime() + 8.64e+7 * 7)
    // переопределяем значение валидатора в теге
    endDate.setAttribute("min", minEndDate.toISOString().split('T')[0]);
    // получаем объекты даты для текущего указанного времени окончания аренды
    const currentEndDate = new Date(endDate.value);
    // если текущая дата меньше минимальной, то в инпуте показываем минимальную дату
    // if (currentEndDate < minEndDate) {
    //     endDate.value = minEndDate.toISOString().split('T')[0];
    // }
    // вычисляем максимально возможное время аренды (+6 месяцев)
    const maxEndDate = new Date(
        startDateValue.setMonth(startDateValue.getMonth()+6)
    );
    // переопределяем значение валидатора в теге
    endDate.setAttribute("max", maxEndDate.toISOString().split('T')[0]);
    // если текущая конечная дата больше максимальной, то в инпуте показываем максимальную дату
    // if (currentEndDate > maxEndDate) {
    //     endDate.value = minEndDate.toISOString().split('T')[0];
    // }
    if (startDate.value && endDate.value) {
        calcTotalPrice();
        totalPriceBlock.style.display = "block";
        goToPaymentButton.style.display = "block";
    }
}

const getInventoryPrice = async() => {
    const getStorageChecked = () => {
      const result = document.querySelector('input[name="storage"]:checked');
      if (!result) { return getStorageChecked(); }
      return result;
    }
    const StorageChecked = getStorageChecked();
    const inventoryChecked = document.querySelector(
        'input[name="inventory"]:checked'
    )
    storage = StorageChecked?.value;
    inventory = inventoryChecked?.value;
    const response = await fetch(`/inventory_price/${storage}/${inventory}`);
    const { weekPrice, monthPrice } = await response.json();
    return [ weekPrice, monthPrice ]
  }

const calcChangedInventoryPrice = async () => {
    if (storage) {
        const [weekPrice, monthPrice] = await getInventoryPrice();
        document.querySelector('#weekPrice').innerHTML = `${weekPrice}&#8381;`;
        document.querySelector('#monthPrice').innerHTML = `${monthPrice}&#8381;`;
        calcTotalPrice();
      }
}

const calcPriceCheckedStorage = async () => {
    if (document.querySelector('input[name="storage"]:checked')) {
        const [weekPrice, monthPrice] = await getInventoryPrice();
        document.querySelector('#weekPrice').innerHTML = `${weekPrice}&#8381;`;
        document.querySelector('#monthPrice').innerHTML = `${monthPrice}&#8381;`;
        
        if (startDate.value && endDate.value) {
            console.log('!!!!');
            calcTotalPrice(); 
        }
        pricesBlock.style.display = "block";
        dateBlock.style.display = "block";
    }
};

const calcPriceIfSetQuantity = () => { 
    storageBlock.style.display = "block";
    if (startDate.value && endDate.value) {
        calcTotalPrice();
    }
}

const calcPriceSetEndDate = () => {
    if (startDate.value && endDate.value) {
        calcTotalPrice();
        totalPriceBlock.style.display = "block";
        goToPaymentButton.style.display = "block";
    }
}

inventoryChoice.addEventListener('click', showQuantity);
inventoryChoice.addEventListener('click', calcChangedInventoryPrice);
quantity.addEventListener('input', calcPriceIfSetQuantity);
storageChoice.addEventListener('click', calcPriceCheckedStorage);
startDate.addEventListener('input', setStartDateAndCalcPrice);
endDate.addEventListener('input', calcPriceSetEndDate);