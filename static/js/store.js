const STORAGE_KEY = "myBooks";

window.books = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];

window.saveBooks = function () {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(window.books));
};

window.buyBook = function (book) {
  if (!window.books.find(b => b.id === book.id)) {
    window.books.push(book);
    window.saveBooks();
  }
};

window.getBooks = function () {
  return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
};

window.removeBook = function (index) {
  window.books.splice(index, 1);
  window.saveBooks();
};