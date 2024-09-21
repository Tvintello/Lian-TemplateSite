$(function () {
    $('.project__view-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        draggable: false,
        arrows: false,
        speed: 400,
        dots: true,
        appendDots: $('.project__view__dots'),
        responive: [
            {
                breakpoint: 600,
                settings: {
                    draggable: true
                }
            }
        ]
    }).on('afterChange', function(event, slick, currentSlide, nextSlide){
        var i = currentSlide + 1;
        $('.project__paging-page').html(i + '/' + slick.slideCount);
    })

    var first = 1
    var last = 4
    let d = 1


    $('.project__view__dots .slick-dots').slick({
        slidesToShow: last,
        slidesToScroll: d,
        arrows: false,
        infinite: false,
        draggable: false,
    })


    $('.project__view__dots .slick-slide').removeClass('slick-active')
    $('.project__view__dots .slick-slide:first-child').addClass('slick-active')

    $(`.slick-slide button`).on('click', function () {
        let i = Number(this.id.split('l').at(-1)) + 1
        let len = $('.project__view__dots .slick-track').children().length
        if (i == last && i != len && last != len) {
            $('.project__view__dots .slick-dots').slick('slickNext')
            first += d
            last += d
        } else if (i == first && i != 1) {
            $('.project__view__dots .slick-dots').slick('slickPrev')
            last -= d
            first -= d
        }
    })

    let len = $('.project__view__image').length
    let wrapper
    let image
    let li
    let li_inx = 1;

    for (let i = 1; i < len + 1; i++) {
        wrapper = $('<div class="project__view__image-dots"></div>')
        image = $('.project__view__image:nth-child(' + i + ')')
        li = $('.project__view__dots li:nth-child(' + li_inx + ')')
        wrapper.append($('.project__view__image:nth-child(' + i + ') img').clone())

        if (!image.hasClass('slick-cloned')) {
            li.append(wrapper)
            li_inx++
        }
    }

    $('.project__like-btn').on('click', function () {
        var action
        var id = $(this).attr("data-product_id")
        let likes = $('.likes_number').text()

        if ($(this).hasClass('project__like-btn--active')) {
            $(this).removeClass('project__like-btn--active')
            $('.likes_number').html(Number(likes) - 1)
            action = -1
        } else {
            $(this).addClass('project__like-btn--active')
            $('.likes_number').html(Number(likes) + 1)
            action = 1
        }

        $.post('/like_product', {
            action: action,
            id: id
        })
    })

    $('.project__view__image').on('click', function () {
        $('.project__full_view').css('display', 'block')
        $('.wrapper').addClass('wrapper--blackout')
        src = $('.slick-active img').prop('src')
        $('.project__full_view img').prop('src', src)

    })

    $('.project__full_view__close').on('click', function () {
        $('.project__full_view').css('display', 'none')
        $('.wrapper').removeClass('wrapper--blackout')
    })
})