window.books = JSON.parse(localStorage.getItem("mybooks")) || [];

window.saveBooks = function () {
  localStorage.setItem("mybooks", JSON.stringify(window.books));
};

window.buyBook = function (book) {
  window.books.push(book);
  window.saveBooks();
};

window.getBooks = function () {
  return window.books;
};

window.removeBook = function (index) {
  window.books.splice(index, 1);
  window.saveBooks();
};