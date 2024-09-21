$(function() {
    $('#images').on('change', function () {
        let files = document.getElementById('images').files;
        $("#file_stats").html(files.length + " files were choosen")


        // preview

        // for (let i = 0; files.length > i; i += 1) {
        //     if (files[i].type.startsWith("image/")) {
        //         let img = document.createElement("img");
        //         let preview = document.querySelector('.user_heading__edit_icon__preview')
        //         img.classList.add("obj");
        //         img.file = files[i];
        //         preview.appendChild(img);
        //         let reader = new FileReader();
        //         reader.onload = (function (aImg) {
        //             return function (e) {
        //                 aImg.src = e.target.result;
        //             };
        //         })(img);
        //         reader.readAsDataURL(files[i]);
        //     }}
    })
})