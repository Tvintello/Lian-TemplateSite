$(function () {
    let re = new RegExp('(.*){{.*}}(.*)')
    let children = $('.post-inner').find('img')
    for (let j = 0; children.length > j; j++) {
        let str = children[j].getAttribute('src').replace(re, `$1${$('.post-inner').attr('data-postid')}$2`)
        children[j].setAttribute('src', str)
    }

    $('.comment__message_clone').css('width', $('.comment__message').css('width'))

    $('.comment__message').on('input', function() {
        text = $(this).val()
        $('.comment__message_clone').html(text)
        height = $('.comment__message_clone').css('height').match(/[0-9]+/)[0]
        $(this).css('height', `${Number(height) + 30}px`)
    })

    $('.comment__discard-btn').on('click', function () {
        $('.comment__message').val('')
        $('.comment__message').css('height', '52px')
    })

    $('.comment_list__like-btn').on('click', function () {
        if ($(this).hasClass('comment_list__like-btn--active')) {
            $(this).removeClass('comment_list__like-btn--active')
        } else {
            $(this).addClass('comment_list__like-btn--active')
        }
    })
})