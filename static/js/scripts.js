$(document).ready(function() {
    $('.nav-link').on('click', function(e) {
        e.preventDefault();
        const category = $(this).data('category');
        if (category) {
            if (category === 'all') {
                $('.product-card').show();
            } else {
                $('.product-card').hide();
                $(`.product-card[data-category='${category}']`).show();
            }
            $('.nav-link').removeClass('active');
            $(this).addClass('active');
        }
    });
});