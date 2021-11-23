const getInventoryPriceEndpoint = '/inventory_calc/price';
const calcTotalPriceEndpoint = '/inventory_calc/calc_total_price'

const inventoryRadios = document.querySelectorAll('input[name="inventory"]');
const storageRadios = document.querySelectorAll('input[name="storage"]');
const quantityBlock = document.querySelector('#quantity_block');
const quantity = document.querySelector('#id_quantity');
const storageBlock = document.querySelector('#storage_block');
const pricesBlock = document.querySelector('#prices_block');
const startDate = document.querySelector('#id_start_date');
const endDate = document.querySelector('#id_end_date');
const dateBlock = document.querySelector('#date_block');
const totalPrice = document.querySelector('#totalPrice');
const totalPriceBlock = document.querySelector('#total_price_block');
const goToPaymentButton = document.querySelector('#go_to_payment');
const totalPriceHiddenInput = document.querySelector('#id_price');
const orderForm = document.querySelector('#orderForm');

// здесь храним и динамически обновляем
// выбранные пользователем опции инвентаря и склада
const checkedStorageAndInventory = { storage: null, inventory: null };

const calcTotalPrice = async () => {
    const start = startDate.value;
    const end = endDate.value;
    const weekPrice = Number.parseInt(
        document.querySelector('#weekPrice').textContent
    );
    const monthPrice = Number.parseInt(
        document.querySelector('#monthPrice').textContent
    );
    const response = await fetch(`${calcTotalPriceEndpoint}/${start}/${end}`);
    const { months, weeks } = await response.json();
    const price = (months * monthPrice + weeks * weekPrice) * quantity.value;
    totalPrice.innerHTML = `${price}&#8381;`;
    return price;
}

const getInventoryPrice = async () => {
    const {storage, inventory} = checkedStorageAndInventory;
    const response = await fetch(
        `${getInventoryPriceEndpoint}/${storage}/${inventory}`
    );
    const { weekPrice, monthPrice } = await response.json();
    document.querySelector('#weekPrice').innerHTML = `${weekPrice}&#8381;`;
    document.querySelector('#monthPrice').innerHTML = `${monthPrice}&#8381;`;
  }

// инвентарь
const setInventory = async checkedRadio => {
    checkedStorageAndInventory.inventory = checkedRadio;
    if (quantityBlock.style.display === 'none') {
        quantityBlock.style.display = 'block';
    }
    if (checkedStorageAndInventory.storage) {
        await getInventoryPrice();
        if (startDate.value && endDate.value) { await calcTotalPrice(); }
    }
}
// количество товара
const setQuantity = async () => { 
    storageBlock.style.display = "block";
    if (startDate.value && endDate.value) { await calcTotalPrice(); }
}
// склады
const setStorage = async checkedStorage => {
    checkedStorageAndInventory.storage = checkedStorage;
    await getInventoryPrice();
    if (dateBlock.style.display === "none") {
        dateBlock.style.display = "block";
        pricesBlock.style.display = "block";
    }
    if (startDate.value && endDate.value) {
        await calcTotalPrice(); 
    }
};
// дата начала хранения
const setStartDate = async () => {
    // получаем значение даты начала хранения, которую установил пользователь
    const startDateValue = new Date(startDate.value);
    // получаем объект даты для минимально возможного времени аренды (1 неделя)
    const minEndDate = new Date(startDateValue.getTime() + 8.64e+7 * 7)
    // переопределяем значение валидатора в теге
    endDate.setAttribute("min", minEndDate.toISOString().split('T')[0]);
    const currentEndDate = endDate.value;
    if (currentEndDate && (new Date(currentEndDate) < minEndDate)) {
        endDate.value = minEndDate.toISOString().split('T')[0];
    }
    // вычисляем максимально возможное время аренды (+6 месяцев)
    const maxEndDate = new Date(
        startDateValue.setMonth(startDateValue.getMonth() + 6)
    );
    // переопределяем значение валидатора в теге
    endDate.setAttribute("max", maxEndDate.toISOString().split('T')[0]);
    if (startDate.value && endDate.value) {
        await calcTotalPrice();
        if (totalPriceBlock.style.display === "none") {
            totalPriceBlock.style.display = "block";
            goToPaymentButton.style.display = "flex";
        }
    }
}
// дата окончания хранения
const setEndDate = async () => {
    if (startDate.value && endDate.value) {
        await calcTotalPrice();
        if (totalPriceBlock.style.display === "none") {
            totalPriceBlock.style.display = "block";
            goToPaymentButton.style.display = "flex";
        }
    }
}

// слушатели
inventoryRadios.forEach(radio => {
    radio.addEventListener('change', 
        event => { setInventory(event.target.value) }
    )
});
storageRadios.forEach(radio => {
    radio.addEventListener('change', 
        event => { setStorage(event.target.value) }
    )
});
quantity.addEventListener('input', setQuantity);
startDate.addEventListener('input', setStartDate);
endDate.addEventListener('input', setEndDate);
orderForm.addEventListener(
    'submit',
    () => {
        console.log('Сработал сабмит');
        price = Number.parseInt(
            document.querySelector('#totalPrice').textContent
        );
        totalPriceHiddenInput.value = price;
    }
)
