$(document).ready(function() {
    $('.testimonials-carousel').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        dots: true,
        speed: 300,
        adaptiveHeight: true,
        arrows: true,
        prevArrow: '<button type="button" class="slick-prev"><i class="fas fa-chevron-left"></i></button>',
        nextArrow: '<button type="button" class="slick-next"><i class="fas fa-chevron-right"></i></button>'
    });

    $('.accordion-header').click(function() {
        $(this).next('.accordion-content').slideToggle();
        $(this).parent().toggleClass('active');
    });

    const ballonCover = document.querySelector('.ballon-cover');
    const ballonImg = document.querySelector('.ballon-img');

    if (ballonImg && ballonCover) {
        ballonImg.addEventListener('click', function() {
            ballonImg.style.transform = 'scale(0)';
            setTimeout(() => {
                ballonCover.classList.add('hidden');
            }, 500);
        });
    }

    const checkboxes = document.querySelectorAll('.checkbox');
    const selectedCategoriesInput = document.getElementById('selected-categories');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', () => {
            checkbox.classList.toggle('selected');
            updateSelectedCategories();
        });
    });

    function updateSelectedCategories() {
        const selectedValues = Array.from(checkboxes)
                                    .filter(checkbox => checkbox.classList.contains('selected'))
                                    .map(checkbox => checkbox.dataset.value);
        selectedCategoriesInput.value = selectedValues.join(',');
    }

    // S'assurer que les catégories sont mises à jour avant la soumission du formulaire
    document.querySelector('.form').addEventListener('submit', function(event) {
        updateSelectedCategories();
    });
});