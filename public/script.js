console.log("xy");
let closebtn = document.querySelector(".btn-close");
let diary_div = document.querySelector(".diary");

let diary_btn = document.querySelector(".diary_btn")

closebtn.addEventListener('click', function(event) {
    diary_div.style.display = 'none';
});

diary_btn.addEventListener('click', function(event) {
    event.preventDefault();
    diary_div.style.display = 'flex';
});