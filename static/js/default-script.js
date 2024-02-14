// Add Edit Feature for every item

const addButton = document.getElementById("add");
const itemsList = document.getElementById("list-of-items");
const dateSelector = document.getElementById("date-selector");
const addItemButton = document.getElementById("add");
const timeSelector = document.getElementById("time");
const itemNameHelper = document.getElementById("item-name-text");
const itemQuantityHelper = document.getElementById("item-quantity-text");
const itemAmountHelper = document.getElementById("item-amount-text");
const duplicateHelper = document.getElementById("duplicate-helper-text");
const previewButton = document.getElementById("preview");
const emptyItemsHelper = document.getElementById("empty-items-helper");

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
  let itemDescription = document.getElementById("description").value;
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
  if (!itemAmount) {
    itemAmountHelper.classList.remove("invisible");
    return;
  }
  if (!itemQuantity) {
    itemQuantityHelper.classList.remove("invisible");
    return;
  }
  if (!itemDescription) {
    itemDescription = "No Description";
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
  itemsArray.push({
    itemName: itemName,
    itemDescription: itemDescription,
    itemAmount: itemAmount,
    itemQuantity: itemQuantity,
  });

  newItem.innerHTML = `Item Name: <input type='text' disabled class='editable-input' value='${itemName}'> Description: <input type='text' disabled class='editable-input' value='${itemDescription}'> Item Amount: <input type='text' disabled class='editable-input' value='${itemAmount}'> Item Quantity: <input type='text' disabled class='editable-input' value='${itemQuantity}'><button onClick = "removeElement('${itemName}')">Remove Item</button> <button onClick = "editItem('${
    itemsArray[itemsArray.length - 1]
  }', ${
    itemsArray.length - 1
  }, '${itemName}')" id="edit-button-${itemName}">Edit Item</button>`;

  itemsList.appendChild(newItem);
}

function editItem(itemObj, itemIndex, itemClass) {
  const currentListItem = document.querySelector(`li.${itemClass}`);
  const saveButton = document.createElement("button");
  const editButton = document.querySelector(`#edit-button-${itemClass}`);
  const itemNameInput = currentListItem.querySelector("input");
  const initialItemNameInput = itemNameInput.value;
  const itemDescriptionInput = itemNameInput.nextElementSibling;
  const itemAmountInput = itemDescriptionInput.nextElementSibling;
  const itemQuantityInput = itemAmountInput.nextElementSibling;
  const removeButton = itemQuantityInput.nextElementSibling;

  itemNameInput.disabled =
    itemDescriptionInput.disabled =
    itemQuantityInput.disabled =
    itemAmountInput.disabled =
      false;

  itemNameInput.classList.add("editing-state");
  itemDescriptionInput.classList.add("editing-state");
  itemQuantityInput.classList.add("editing-state");
  itemAmountInput.classList.add("editing-state");

  editButton.classList.add("invisible");
  saveButton.textContent = "Save Item";
  saveButton.id = "save-button";
  saveButton.addEventListener("click", () => {
    const itemNameInputValue = currentListItem.querySelector("input").value;
    const itemDescriptionInputValue = itemNameInput.nextElementSibling.value;
    const itemAmountInputValue = itemDescriptionInput.nextElementSibling.value;
    const itemQuantityInputValue = itemAmountInput.nextElementSibling.value;

    for (const item of itemsArray) {
      if (
        item.itemName === itemNameInputValue &&
        item.itemDescription === itemDescriptionInputValue &&
        item.itemAmount === itemAmountInputValue &&
        item.itemQuantity === itemQuantityInputValue
      ) {
        currentListItem.querySelector("input").value = initialItemNameInput;
        duplicateHelper.classList.remove("invisible");
        editButton.classList.remove("invisible");
        saveButton.remove();
        itemNameInput.classList.remove("editing-state");
        itemDescriptionInput.classList.remove("editing-state");
        itemQuantityInput.classList.remove("editing-state");
        itemAmountInput.classList.remove("editing-state");
        itemNameInput.disabled =
          itemDescriptionInput.disabled =
          itemQuantityInput.disabled =
          itemAmountInput.disabled =
            true;
        return;
      }
    }

    itemNameInput.disabled =
      itemDescriptionInput.disabled =
      itemQuantityInput.disabled =
      itemAmountInput.disabled =
        true;

    itemsArray[itemIndex].itemName = itemNameInputValue;
    itemsArray[itemIndex].itemDescription = itemDescriptionInputValue;
    itemsArray[itemIndex].itemAmount = itemAmountInputValue;
    itemsArray[itemIndex].itemQuantity = itemQuantityInputValue;

    editButton.classList.remove("invisible");
    itemNameInput.classList.remove("editing-state");
    itemDescriptionInput.classList.remove("editing-state");
    itemQuantityInput.classList.remove("editing-state");
    itemAmountInput.classList.remove("editing-state");
    saveButton.remove();

    itemNameInput.className = itemNameInputValue + " editable-input";
    itemDescriptionInput.className =
      itemDescriptionInputValue + " editable-input";
    itemAmountInput.className = itemAmountInputValue + " editable-input";
    itemQuantityInput.className = itemQuantityInputValue + " editable-input";
    currentListItem.className = itemNameInputValue;

    removeButton.onclick = null;
    removeButton.addEventListener(
      "click",
      removeElement.bind("this", itemNameInputValue)
    );

    editButton.onclick = null;
    editButton.addEventListener(
      "click",
      editItem.bind(this, itemsArray[itemIndex], itemIndex, itemNameInputValue)
    );
    editButton.id = `edit-button-${itemNameInputValue}`;
  });
  currentListItem.appendChild(saveButton);
  duplicateHelper.classList.add("invisible");
}

// Function to remove Item from DOM & Items Array
function removeElement(itemToRemove) {
  const elementToRemove = document.querySelector(`.${itemToRemove}`);
  for (const element of itemsArray) {
    if (element.itemName === itemToRemove) {
      itemsArray.splice(itemsArray.indexOf(element), 1);
    }
  }
  elementToRemove.remove();
  if (itemsArray.length === 0) {
    itemsList.classList.add("invisible");
    itemsList.parentElement.classList.add("invisible");
  }
}

addButton.addEventListener("click", addItemToList);

console.log(emptyItemsHelper);

previewButton.addEventListener("click", () => {
  console.log(itemsArray);
  if (itemsArray.length === 0) {
    emptyItemsHelper.classList.remove("invisible");
    return;
  }
  emptyItemsHelper.classList.add("invisible");
});
