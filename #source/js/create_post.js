$(function () {
    $('#images').on('change', function () {
        let files = document.getElementById('images').files;
        let post_images = []

        if (files === undefined) {return}
        str = $('#post_image')

        for (let i = 0; files.length > i; i += 1) {
            if (files[i].type.startsWith("image/")) {
                // image reading
                let reader = new FileReader();
                reader.readAsDataURL(files[i]);
                reader.onload = function () {
                    // image defining
                    $('.image_list__body').append(str.clone().prop('id', ''))
                    let img = document.querySelector(`.image_list__item:last-child img`)
                    img.file = files[i];

                    // name processing
                    let image_name = document.querySelector('.image_list__item:last-child .image_name')
                    let text_name = files[i].name.split('.').slice(0, -1)
                    image_name.innerHTML = "file name: " + text_name

                    img.src = reader.result

                    post_images.push(img.file)

                    $('.image_list__item:last-child .copy_image').click(function () {
                        let i = $(this).parent().index() - 1
                        let img_name = post_images[i].name
                        navigator.clipboard.writeText(`/load_post_image/{{id}}/${img_name}`).then(function () {
                            alert('The image link was successfully copied');
                        }, function (err) {
                            alert('An error has occured while copying');
                        });
                    })
                
                    $('.image_list__item:last-child .delete_image').click(function () {
                        i = $(this).parent().index() - 1
                        post_images.splice(i, 1)
                        $(this).parent().remove()
                        console.log(post_images);
                    })
                }
            }
        }
    })

    $('.form_submit').submit(function(e) {
        dt = new DataTransfer()

        for (file of post_images) {
            dt.items.add(file)
        }

        document.getElementById('#images').files = dt.files;
    })

    $('.show_btn').on('click', function () {
        $(this).css('display', 'none')
        $('.hide_btn').css('display', 'block')
        $('.image_list__body').css('height', 'auto')
    })

    $('.hide_btn').on('click', function () {
        $(this).css('display', 'none')
        $('.show_btn').css('display', 'block')
        $('.image_list__body').css('height', 0)
    })

    $('#heading').on('change', function () {
        let files = document.getElementById('heading').files;
        let file = files[files.length - 1];

        if (files.length == 0) {
            $('.heading_preview').css('display', 'none')
            return
        }

        $('.heading_preview').css('display', 'flex')
        $(".heading_preview img").css('margin-bottom', '15px')
        $(".heading_preview p").html('Heading image')

        if (file.type.startsWith("image/")) {
            let img = document.querySelector('.heading_preview img')
            img.file = file;
            let reader = new FileReader();
            reader.onload = (function (aImg) {
                return function (e) {
                    aImg.onload = function () {
                        if (aImg.width > aImg.height) {
                            aImg.style.width = '100%'
                            aImg.style.height = 'auto'
                        } else if (aImg.width < aImg.height) {
                            aImg.style.height = '100%'
                            aImg.style.width = 'auto'
                        }
                    };
                    aImg.src = e.target.result;
                };
            })(img);
            reader.readAsDataURL(file);
        }
    })

    $('#delete_heading').on('click', function () {
        $('.heading_preview img').prop({ 'src': '', 'file': '' })
        $('.heading_preview').css('display', 'none')
        $('#heading').val('')
    })
})