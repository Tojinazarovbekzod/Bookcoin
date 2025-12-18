window.onload = function(){
  let books = [];

  fetch("/static/data/app.json")
    .then(res => res.json())
    .then(data => {
      books = data;
      renderBooks(books);
  });

}
  
