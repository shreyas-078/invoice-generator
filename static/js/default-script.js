const addButton = document.getElementById("add");
const itemList = document.getElementById("list-of-items");

function displayList() {
  if (itemList.classList.contains("invisible")) {
    itemList.classList.remove("invisible");
  } else {
    return;
  }
}

addButton.addEventListener("click", displayList);
