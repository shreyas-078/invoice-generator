const addButton = document.getElementById("add");
const itemList = document.getElementById("list-of-items");
const dateSelector = document.getElementById("date-selector");
const addItemButton = document.getElementById("add");
const timeSelector = document.getElementById("time");

const date = new Date();

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
let time;

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

function displayList() {
  if (itemList.classList.contains("invisible")) {
    itemList.classList.remove("invisible");
  } else {
    return;
  }
}

addButton.addEventListener("click", displayList);
