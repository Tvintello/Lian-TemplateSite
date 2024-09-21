$(function() {
    $('.delete_btn').on('click', function() {
        $('.window').css('display', 'block')
    })

    $('.window-cancel').on('click', function() {
        $('.window').css('display', 'none')
    })
})