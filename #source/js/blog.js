$(function () {
    var mixer = mixitup('.blog__list', {
        callbacks: {
            onMixStart(state, futureState) {
                if (futureState.hasFailed) {
                    $('.blog__background').removeClass('blog__background--hide')
                    $('.blog__warning').removeClass('blog__background--hide')
                } else {
                    if ($('.blog__list').children().length == 0) {
                        $('.blog__background').removeClass('blog__background--hide')
                        $('.blog__warning').removeClass('blog__background--hide')
                    } else {
                        $('.blog__background').addClass('blog__background--hide')
                        $('.blog__warning').addClass('blog__background--hide')
                    }
                }
            },
            onMixEnd(state) {
                if ($('.offer-list').get(0).scrollWidth > $('.offer-list').get(0).offsetWidth && !state.hasFailed) {
                    $('.load-btn').removeClass('load-btn--disable')
                } else {
                    $('.load-btn').addClass('load-btn--disable')
                }
            }
        },
    })


    if ($('.offer-list').get(0).scrollWidth > $('.offer-list').get(0).offsetWidth) {
        $('.load-btn').removeClass('load-btn--disable')
    } else {
        $('.load-btn').addClass('load-btn--disable')
    }


    $('.blog__list__item-like-btn').on('click', function () {
        var action
        var postid = $(this).attr("data-postid")

        if ($(this).hasClass('blog__list__item-btn--active')) {
            $(this).removeClass('blog__list__item-btn--active')
            action = -1
        } else {
            $(this).addClass('blog__list__item-btn--active')
            action = 1
        }

        $.post('/like_post', {
            action: action,
            id: postid
        })
    })

    $('.blog__load-btn').on('click', function () {
        $('.blog__list').addClass('blog__list--stretch')
        $(this).addClass('load-btn--disable')
        post_number = 20
        length = $('.blog__list').children.length;


        (async function load () {
            await fetch(`/blog/load_more?p=${post_number + length}&l=${length}`).then(
                (response) => {
                    response.json().then(
                        (results) => {
                            console.log(results);
                            for (p of results) {
                                let instance = $('#blog_item').clone().prop('id', '')
                                if (p.heading_image) {
                                    instance.find('.blog__list__item-image img').prop('src', p.heading_image)
                                } else {
                                    instance.find('.blog__list__item-image').remove()
                                }
                                
                                instance.find('.blog__list__item-edit_btn').prop('href', p.edit)
                                instance.find('.blog__list__item-tag').html(p.tag)
                                instance.find('.blog__list__item-title').html(p.title)
                                instance.find('.blog__list__item-user').html(p.user_name)
                                instance.find('.blog__list__item-like-btn').addClass(p.liked)
                                instance.find('.blog__list__item-like-btn').attr('data-postid', p.id)
                                instance.find('.blog__list__item-description').html(p.text.replace(/<[^>]*>/g, ''))
                                instance.find('.blog__list__item-date').html(p.date)
                                instance.addClass(instance.attr('data-filt') + p.tag)
                                
                                mixer.append(instance).then(function(state) {
                                    console.log(state.show.length); // true
                                });
                                $('.blog__list').append(instance)
                            }
                        }
                    )
                }
            )
        })()
    })

    $('.aside__tags__list-item').on('click', function () {
        if ($(this).hasClass('aside__tags__list-item--active')) {
            mixer.show()
            $('.aside__tags__list-item').removeClass('aside__tags__list-item--active')
        } else {
            $('.aside__tags__list-item').removeClass('aside__tags__list-item--active')
            $(this).addClass('aside__tags__list-item--active')
        }
    })

    $('.aside-burger').on('click', function () {
        $('.aside__mobile').addClass('aside__mobile--active')
        $('main').addClass('main--blackout')
    })

    $('.aside__close-btn').on('click', function () {
        $('.aside__mobile').removeClass('aside__mobile--active')
        $('main').removeClass('main--blackout')
    })

    if (window.innerWidth <= 1200) {
        $('.aside').addClass('aside__mobile')
    } else {
        $('.aside').removeClass('aside__mobile')
        $('.aside__close-btn').css('display', 'none')
    }

    window.addEventListener('resize', () => {
        if (window.innerWidth <= 1200) {
            $('.aside').addClass('aside__mobile')
            $('.aside__close-btn').css('display', 'block')
        } else {
            $('.aside__close-btn').css('display', 'none')
            $('.aside').removeClass('aside__mobile')
            $('.aside').removeClass('aside__mobile--active')
            $('main').removeClass('main--blackout')
        }
    })

    $('.aside__search-input').focus(function () {
        $('.search_results').css('display', 'block')
        $('.wrapper').addClass('wrapper--blackout')
        $('.aside__search').addClass('aside__search--focused')

        $('.wrapper--blackout').click(function () {
            if (!$('.search_results:hover').length && !$('.aside__search:hover').length) {
                $('.search_results').css('display', 'none')
                $('.wrapper').removeClass('wrapper--blackout')
                $('.aside__search').removeClass('aside__search--focused')
            }
        })
    })

    $('.aside__search').click(function () {
        $('.search_results').css('display', 'block')
        if (!$('.wrapper').hasClass('wrapper--blackout')) {
            $('.aside__search').addClass('aside__search--focused')
            $('.wrapper').addClass('wrapper--blackout')
        }
    })

    $('.aside__search-input').on('input', async function () {
        let value = $(this).val()
        await fetch(`/blog/search/json?q=${value.replace(' ', '_')}`).then(
            function (response) {
                response.json().then(function (results) {
                    $('.search_results').empty()
                    let posts = results[0]
                    console.log(posts);

                    if (posts.length == 0) {
                        $('.search_results').append($('<p>No results</p>'))
                        $('.aside__search-predicted').html('')
                        return
                    }
                    posts = posts.sort((a, b) => {
                        return b.score - a.score
                    })

                    for (post of posts) {
                        let search = $(`<a href="/blog/${post.id}" class="search_results__link"><div class="search_results__item"><div class="search_results__caption">${post.caption}</div><div class="search_results__text">${post.text}</div></div></a>`)
                        $('.search_results').append(search)
                    }

                    if (!results[1].length) {
                        $('.aside__search-predicted').html('')
                        return 
                    }

                    for (p of results[1].slice(0, 6)) {
                        inp = $('.aside__search-predicted').html(value.replace(/\s/ug, '&nbsp'))
                        let x = inp.width() + +$('.aside__search').css('padding-left').match(/\d*/u)
                        $('.aside__search-predicted').css('left', `${x}px`)

                        if (value.length + 1 >= p.caption.length) {
                            $('.aside__search-predicted').html('')
                        } else {
                            $('.aside__search-predicted').html(p.caption.slice(value.length, p.caption.length).replace(' ', '&nbsp'))
                        }
                    }
                })
            })
    })
})