window.onload = hello;

function hello() {
  document.getElementById("col1").innerHTML = "WORKS"
  alert("Hello");
}

$(function(){
    $('#title-area').text(loadPageVar('title'));
    $('.product-img').text(loadPageVar('img')); // will set text

    // To set an image with the src
    $('.product-img').append($('<img/>', {
        'src':loadPageVar('img')
    }));
});
