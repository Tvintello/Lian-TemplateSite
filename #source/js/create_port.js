$(function () {
    let tag_list = []
    $('#tags_btn').on('click', function () {
        let select = $('#tag_wrap').clone().prop('id', '')
        select.find('*').prop({ 'id': '' })
        select.find('*').css('display', 'block')
        $(this).before(select)
        tag_list.push(select.find('select').val())

        $('.tags_list__select').on('change', function () {
            tag_list[$(this).parent().index() - 2] = $(this).val().replace(" ", "_") 
            $('#tags').val(tag_list.join(' '))
        })

        $('.delete_button').on('click', function (e) {
            tag_list.splice($(this).parent().index() - 2, 1)
            $(this).parent().remove()
            e.stopImmediatePropagation();
        })

        $('#tags').val(tag_list.join(' '))
        console.log($('#tags').val());
    })

    $('#images').on('change', function () {
        if ($('#images').prop('files').length != 0) {
            $('#file_warning').css({'display': 'none', 'margin': '-10px', 'height': '0'})
        }
    })

    $('.form').on('submit', function (e) {
        if ($('#images').prop('files').length == 0) {
            $('#file_warning').css({'margin': '0 auto 20px', 'height': 'auto'})
            $('#file_warning').html('You didn`t choose any file')
            $('#file_warning').addClass('flash-error')
            e.preventDefault()
        }
    })
})