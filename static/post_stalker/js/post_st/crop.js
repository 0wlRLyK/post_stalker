function cropIt() {
    let result = document.querySelector('.result'),
        img_result = document.querySelector('.img-result'),
        save = document.querySelector('#show_avatar_preview'),
        cropped = document.querySelector('.cropped'),
        upload = $('#id_avatar');
    window.cropper = '';

// on change show image with crop options
    upload.on('change', (e) => {
        $("#cropper_toolbox").removeClass('hide');
        if (e.target.files.length) {
            // start file reader
            const reader = new FileReader();
            reader.onload = (e) => {
                if (e.target.result) {
                    // create new image
                    let img = document.createElement('img');
                    img.id = 'image';
                    img.src = e.target.result
                    // clean result before
                    result.innerHTML = '';
                    // append new image
                    result.appendChild(img);
                    // show save btn and options
                    save.classList.remove('hide');
                    let minCroppedWidth = 165,
                        minCroppedHeight = 215,
                        maxCroppedWidth = 495,
                        maxCroppedHeight = 645;
                    window.cropper = new Cropper(img, {
                        viewMode: 2,
                        aspectRatio: 165 / 215,
                        data: {
                            width: (minCroppedWidth + maxCroppedWidth) / 2,
                            height: (minCroppedHeight + maxCroppedHeight) / 2,
                        },


                    });
                }
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    });

// save on click
    save.addEventListener('click', (e) => {
        e.preventDefault();
        // get result to data uri
        let imgSrc = window.cropper.getCroppedCanvas({
            width: 165,
            height: 215,
        }).toDataURL();
        cropped.classList.remove('hide');
        img_result.classList.remove('hide');
        cropped.src = imgSrc;
        var cropData = window.cropper.getData(true);
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#formUpload").submit();
        console.log(cropData)

    });
    $('#change_avatar_form').on('submit', function (event) {
        event.preventDefault();
        if (window.cropper) {
            let cropData = window.cropper.getData(true);
            console.log(cropData);
            $("#id_x").val(cropData["x"]);
            $("#id_y").val(cropData["y"]);
            $("#id_height").val(cropData["height"]);
            $("#id_width").val(cropData["width"]);
            $('#change_avatar_form .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
            let data = new FormData($(this).get(0));
            console.log(data)
            $.ajax({
                url: '/pda/edit/avatar/',
                type: "POST", // http method
                processData: false,
                contentType: false,
                data: data,
                success: function (data) {
                    $('#change_avatar_form .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
                    if ($("#user_avatar").length) {
                        $("#user_avatar").attr("src", data.avatar)
                    }
                    if ($("#change_avatar_form").parents().find(".atm-fwin")) {
                        atmWnd.hide($("#change_avatar_form").parents().find(".atm-fwin").attr("id"));
                    }
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + ": " + errmsg);
                    $('#change_avatar_form .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>" +
                        "<b style='color: red'>" + xhr.status + ": " + errmsg + "</b>");
                }
            });
        } else {
            $('#change_avatar_form .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>" +
                "<b style='color: red'>Отсутствует изображение для отправки</b>");
        }
    });
};
$("#crop_mode-move").click(function () {
    window.cropper.setDragMode("move");
});
$("#crop_mode-crop").click(function () {
    window.cropper.setDragMode("crop");
});
$("#crop_zoom-in").click(function () {
    window.cropper.zoom(0.1);
});
$("#crop_zoom-out").click(function () {
    window.cropper.zoom(-0.1);
});
$("#crop_left").click(function () {
    window.cropper.move(-10, 0);
});
$("#crop_right").click(function () {
    window.cropper.move(10, 0);
});
$("#crop_up").click(function () {
    window.cropper.move(0, 10);
});
$("#crop_down").click(function () {
    window.cropper.move(0, -10);
});
// $("#crop_rotate-in").click(function () {
//   window.cropper.rotate(-45);
// });
// $("#crop_rotate-out").click(function () {
//   window.cropper.rotate(45);
// });
// $("#crop_scale-x").click(function () {
//     if (window.cropper.getData().scaleX === 1) {
//        window.cropper.scaleX(-1);
//     } else {
//         window.cropper.scaleX(1);
//     }
//
// });
// $("#crop_scale-y").click(function () {
//     if (window.cropper.getData().scaleY === 1) {
//        window.cropper.scaleY(-1);
//     } else {
//         window.cropper.scaleY(1);
//     }
// });