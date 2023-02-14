$('.product-2-img img').bind('mouseenter mouseleave', function() {
    $(this).attr({
        src: $(this).attr('data-other-src'),
        'data-other-src': $(this).attr('src')
    })
});

$('.prod-link').hover(
    function() {
        $(this).find('.product-2-hover').css('display', 'block'); 
    }, function() {
        $(this).find('.product-2-hover').css('display', 'none');
    }
);