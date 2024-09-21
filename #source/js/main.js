$(function () {
    $('.header__search-btn').on('click', function () {
        $('.header__search-bar').addClass('header__search-bar--active')
        $('.header__search').addClass('header__search--active')
        $('.header__nav-list').removeClass('header__nav-list--active')
        $('.header__close').addClass('header__close--active')
        if ($('.header__burger').css('display').toLowerCase() == 'block') {
            $('.header__burger').css('display', 'none')
        }
        $('.header__user').css('display', 'none')
    })

    $('.header__close').on('click', function () {
        $('.header__search-bar').removeClass('header__search-bar--active')
        $('.header__search').removeClass('header__search--active')
        $('.header__nav-list').addClass('header__nav-list--active')
        $('.header__close').removeClass('header__close--active')
        $('.header__user').css('display', 'flex')
    })

    $('.header__burger').on('click', function () {
        if ($('.header__nav').hasClass('header__nav--show')) {
            $('.header__top').css('display', 'block')
            $('.header__mobile').css('display', 'none')
            $('.header__nav').removeClass('header__nav--show')
        } else {
            $('.header__top').css('display', 'none')
            $('.header__mobile').css('display', 'block')
            $('.header__nav').addClass('header__nav--show')
        }
    })
})