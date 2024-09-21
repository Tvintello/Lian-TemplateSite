$(function () {
    function UpdateIconEditing () {
        $('.user_heading__edit_icon__preview img').css('width', $('#scale').val() + '%')
        let re = new RegExp('anchor-([a-zA-Z]+)')
        let anchor = $('.user_heading__edit_icon__preview').attr('class').match(re)
        if (anchor) {
            $('.user_heading__edit_icon__preview').removeClass('anchor-' + anchor[1])
        }
        $('.user_heading__edit_icon__preview').addClass('anchor-' + $('#binding').val())
    }
    $('.user_heading__icon').on('click', function () {
        $('.user_heading__edit_icon').css('display', 'block')
        $('.wrapper').addClass('wrapper--blackout')
        UpdateIconEditing();
    })

    $('.user_heading__edit-btn').on('click', function () {
        $('.user_heading__name__text').css('display', 'none')
        $('.user_heading__edit_name-block').css('display', 'block')
        $(this).css('display', 'none')
    })

    $('.user_heading__save-btn').on('click', function () {
        $('.user_heading__name__text').css('display', 'block')
        $('.user_heading__edit_name-block').css('display', 'none')
    })

    $('.user_heading__edit_icon__close').on('click', function () {
        $('.user_heading__edit_icon').css('display', 'none')
        $('.wrapper').removeClass('wrapper--blackout')
    })

    $('#ava').on('change', function () {
        let files = document.getElementById('ava').files;
        let file = files[files.length - 1];

        if (file.type.startsWith("image/")) {
            let img = document.querySelector('.user_heading__edit_icon__preview img')
            img.file = file;
            let reader = new FileReader();
            reader.onload = (function (aImg) {
                return function (e) {
                    aImg.src = e.target.result;
                };
            })(img);
            reader.readAsDataURL(file);
        }
        UpdateIconEditing();
    })

    $('#scale').on('input', function () {
        $('.user_heading__edit_icon__preview img').css('width', $(this).val() + '%')
    })

    $('#binding').on('change', function () {
        let re = new RegExp('anchor-([a-zA-Z]+)')
        let anchor = $('.user_heading__edit_icon__preview').attr('class').match(re)
        if (anchor) {
            $('.user_heading__edit_icon__preview').removeClass('anchor-' + anchor[1])
        }
        $('.user_heading__edit_icon__preview').addClass('anchor-' + $('#binding').val())
    })

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

    $('.aside__btn-list__btn').on('click', function () {
        $('.aside__btn-list__btn').removeClass('aside__btn-list__btn--active')
        $(this).addClass('aside__btn-list__btn--active')
        $('.user_body__info').removeClass('selected_page')
        $(`.${$(this).prop('id')}-page`).addClass('selected_page')
    })

    $('.product_item').hover(function() {
        $(this).find('.user_body__actions').css('display', 'flex')
        $(this).find('figure').addClass('product_item--blackout')
    }, function() {
        $(this).find('.user_body__actions').css('display', 'none')
        $(this).find('figure').removeClass('product_item--blackout')
    })

    $('.user_body__delete_btn').on('click', function() {
        $('.window').css('display', 'block')
        href = $('.window-accept').prop('href').split("/")
        href[href.length - 2] = $(this).attr('data-productid')
        $('.window-accept').prop('href', href.join("/"))
    })

    $('.window-cancel').on('click', function() {
        $('.window').css('display', 'none')
    })
})