$(function () {
    var mixer = mixitup('.offers__body', {
        callbacks: {
            onMixEnd (state) {
                if ($('.offer-list').get(0).scrollWidth > $('.offer-list').get(0).offsetWidth && !state.hasFailed) {
                    $('.load-btn').removeClass('load-btn--disable')
                } else {
                    $('.load-btn').addClass('load-btn--disable')
                }
            }
        }
    });

    if ($('.offer-list').get(0).scrollWidth > $('.offer-list').get(0).offsetWidth && !state.hasFailed) {
        $('.load-btn').removeClass('load-btn--disable')
    } else {
        $('.load-btn').addClass('load-btn--disable')
    }

    $('.offers__load-btn').on('click', function () {
        $('.offers__body').addClass('offers__body--stretch')
        $(this).addClass('offers__load-btn--disable')
    })

    $('.header__slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 5000,
        draggable: false,
        arrows: false,
        infinite: true,
        dots: true,
        speed: 1000,
        appendDots: $('.header__slider-dots'),
        responsive: [{
            breakpoint: 980,
            settings: {
                draggable: true,
            }
        }]
    })

    $('.header__slider').slick('setPosition')

    $('.header__slider-prev').on('click', function () {
        $('.header__slider').slick('slickPrev')
    })
    $('.header__slider-next').on('click', function () {
        $('.header__slider').slick('slickNext')
    })

    // var lastScrollTop = 0, delta = 5;
	//  $(window).scroll(function(){
	// 	 var nowScrollTop = $(this).scrollTop();
	// 	 if(Math.abs(lastScrollTop - nowScrollTop) >= delta){
	// 	 	if (nowScrollTop > lastScrollTop){
    //             $('.header__top').removeClass('header__top--fixed')
	// 	 	} else {
    //             $('.header__top').addClass('header__top--fixed')
	// 		}
	// 	 lastScrollTop = nowScrollTop;
	// 	 }
	//  });
})