let slide_index = 1;
carousel('FEATURED');
carousel('RANDOM');

function carousel(par) {
    let i;
    let x = document.getElementById(par).querySelectorAll('.carousel-box');
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    slide_index++;
    if (slide_index > x.length) {
        slide_index = 1;
    }
    x[slide_index-1].style.display = 'block';
    setTimeout(function() {carousel(par)}, 3000);
}