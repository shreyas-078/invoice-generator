// Add Edit Feature for every item

const addButton = document.getElementById("add");
const itemsList = document.getElementById("list-of-items");
const dateSelector = document.getElementById("date-selector");
const addItemButton = document.getElementById("add");
const timeSelector = document.getElementById("time");
const itemNameHelper = document.getElementById("item-name-text");
const itemQuantityHelper = document.getElementById("item-quantity-text");
const itemAmountHelper = document.getElementById("item-amount-text");

const date = new Date();

let itemsArray = [];

let currentDate;

let day = date.getDate();
let month = date.getMonth();
let year = date.getFullYear();

if (month < 10) {
  if (date < 10) {
    currentDate = `${year}-0${month}-0${day}`;
  } else {
    currentDate = `${year}-0${month}-${day}`;
  }
} else if (date < 10) {
  currentDate = `${year}-${month}-0${day}`;
}

dateSelector.value = currentDate;

const hour = date.getHours();
const min = date.getMinutes();
let time = `${hour}:${min}:00`;

if (hour < 10) {
  if (min < 10) {
    time = `0${hour}:0${min}:00`;
  } else {
    time = `0${hour}:${min}:00`;
  }
} else if (min < 10) {
  time = `${hour}:0${min}:00`;
}

timeSelector.value = time;

// Function to add Item to DOM & Array
function addItemToList() {
  const itemName = document.getElementById("item").value;
  const itemDescription = document.getElementById("description").value;
  const itemAmount = document.getElementById("amount").value;
  const itemQuantity = document.getElementById("quantity").value;

  if (!isNaN(parseInt(itemName.charAt(0)))) {
    itemNameHelper.textContent = "Invalid Item Name.";
    itemNameHelper.classList.remove("invisible");
    return;
  }
  if (!itemName) {
    itemNameHelper.textContent = "Please Provide an Item Name to Add.";
    itemNameHelper.classList.remove("invisible");
    return;
  }
  if (!itemQuantity) {
    itemQuantityHelper.classList.remove("invisible");
    return;
  }
  if (!itemAmount) {
    itemAmountHelper.classList.remove("invisible");
    return;
  }

  itemsList.classList.remove("invisible");
  itemsList.parentElement.classList.remove("invisible");
  itemNameHelper.classList.add("invisible");
  itemQuantityHelper.classList.add("invisible");
  itemAmountHelper.classList.add("invisible");

  // Updated Logic for Duplicate Elements
  for (const element of itemsArray) {
    if (element.itemName === itemName) {
      itemNameHelper.textContent = "This Item Has already been added.";
      itemNameHelper.classList.remove("invisible");
      return;
    }
  }

  const newItem = document.createElement("li");
  newItem.className = `${itemName}`;
  newItem.innerHTML = `Item Name: <input type='text' disabled class='editable-input' value=${itemName}> Description: <input type='text' disabled class='editable-input' value=${itemDescription}> Item Amount: <input type='text' disabled class='editable-input' value=${itemAmount}> Item Quantity: <input type='text' disabled class='editable-input' value=${itemQuantity}><button onClick = removeElement('${itemName}')>Remove Item</button> <button onClick = editItem(${
    itemsArray[itemsArray.length]
  })>Edit Item</button>`;
  itemsArray.push({
    itemName: itemName,
    itemDescription: itemDescription,
    itemAmount: itemAmount,
    itemQuantity: itemQuantity,
  });

  itemsList.appendChild(newItem);
}

function editItem(itemIndex) {}

// Function to remove Item from DOM & Items Array
function removeElement(itemToRemove) {
  const elementToRemove = document.querySelector(`.${itemToRemove}`);
  for (const element of itemsArray) {
    if (element.itemName === itemToRemove) {
      itemsArray.splice(itemsArray.indexOf(itemToRemove), 1);
    }
  }
  elementToRemove.remove();
  if (itemsArray.length === 0) {
    itemsList.classList.add("invisible");
    itemsList.parentElement.classList.add("invisible");
  }
}

addButton.addEventListener("click", addItemToList);
