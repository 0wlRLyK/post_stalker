/*
AJAX Load Functions
 */
function ajaxLoadingFirst(page_url = "", uid = 1, ajaxWndName = "", moduleName = "") {
    $.ajax({
        url: page_url + uid + '/',
        success: function (data) {
            atmWnd.content(ajaxWndName, data);
        }
    })
}

$(document).on('click', '.atm-cont a[href]', function (e) {
    if (!$(this).data("local")) {
        e.preventDefault();
        let wnd = $(this).parents(".atm-cont");
        $.ajax({
            url: $(this).attr('href'),
            success: function (data) {
                let repPage = $(data).filter("section"),
                    html = repPage.html(),
                    atmWindow = wnd;
                console.log(atmWindow);
                atmWindow.html(html);

            }
        })
    }
});

/*
Reputation functions
 */
function loadReputation(uid = 1) {
    const ajaxWndName = 'rep_wnd';
    atmWnd(
        ajaxWndName,
        'История репутации',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    ajaxLoadingFirst("/u/funcs/rep/", uid, ajaxWndName, "reputation");
}

function loadRespectForm(uid = 1) {
    const ajaxWndName = 'add_rep_wnd';
    atmWnd(
        ajaxWndName,
        'Изменить уровень репутации',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    $.ajax({
        url: '/u/funcs/add/rep/' + uid + '/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data).filter('#respect_changing'));
            $('#respect_change_form').on('submit', function (event) {
                event.preventDefault();
                $('#add_rep_wnd .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                changeRepsect(uid);
            });
        }
    })
}


function changeRepsect(uid = 1) {
    $.ajax({
        url: '/u/funcs/add/rep/' + uid + '/',
        type: "POST", // http method
        data: {
            subject: $('#id_subject').val(),
            type: $('input[name="operation_type"]:checked').val()
        },


        success: function (data) {
            console.log(data)
            if (data.result) {
                $('#id_subject').val('');
                atmWnd.hide('add_rep_wnd');
                $("#user-respect").text(data.current_respect);
                $('#add_rep_wnd .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
            } else {
                $("#transfer_fall").text(data.cause);
                $('#add_rep_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
            }


        },

        error: function (xhr, errmsg, err) {
            $('#transfer_fall').text();
            console.log(xhr.status + ": " + errmsg);
            $('#add_rep_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

/*
Money functions
 */
function loadMoneyTransactions(uid = 1) {
    const ajaxWndName = 'transactions_wnd';
    atmWnd(
        ajaxWndName,
        'Баланс денежных средств',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    ajaxLoadingFirst("/u/funcs/money/", uid, ajaxWndName, "transactions");
}

function loadTransactionForm(uid = 1) {
    const ajaxWndName = 'transfer_wnd';
    atmWnd(
        ajaxWndName,
        'Перевести средства',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    $.ajax({
        url: '/u/funcs/transfer/money/' + uid + '/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data).filter('#money_transfer'));
            let valueInput = $('#id_value'),
                maxMoney = Number($("#wnd_my_currency_transfer").attr("data-money"));
            valueInput.attr({
                "min": 0,
                "max": maxMoney
            });
            $('#money_transfer_form').on('submit', function (event) {
                event.preventDefault();
                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                transferMoney(uid);
            });
        }
    })
}


function transferMoney(uid = 1) {
    $.ajax({
        url: '/u/funcs/transfer/money/' + uid + '/',
        type: "POST", // http method
        data: {
            message: $('#id_message').val(),
            value: $('#id_value').val()
        },

        success: function (data) {
            if (data.result) {
                $('#id_message').val('');
                atmWnd.hide('transfer_wnd');
                $("#user-currency").text(data.user_currency);
                $("#wnd_user_currency").text(data.user_currency);
                $("#wnd_my_currency").text(data.my_currency);
                $('#id_value').attr({
                    "min": 0,
                    "max": data.my_currency
                });
                $('#transfer_wnd .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
            } else {
                $("#transfer_fall").text(data.cause);
                $('#transfer_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
            }


        },

        error: function (xhr, errmsg, err) {
            $('#transfer_fall').text();
            console.log(xhr.status + ": " + errmsg);
            $('#transfer_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

/*
Changing icon/color
 */
function selectImgColorForm() {
    const ajaxWndName = 'img_color_select_wnd';
    atmWnd(
        ajaxWndName,
        'Меню выбора иконки/цвета никнейма для чата',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    $.ajax({
        url: '/u/funcs/img_select/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data).filter('#img_color_select'));
            $('#img_color_select_form').on('submit', function (event) {
                event.preventDefault();
                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                changeImgColor();
                $("#img_color_cause").text("");
            });
        }
    })
}

function changeImgColor() {
    $.ajax({
        url: '/u/funcs/img_select/',
        type: "POST", // http method
        data: {
            icon: $('input[name="ico"]:checked').val(),
            color: $('input[name="color"]:checked').val()
        },

        success: function (data) {
            if (data.result) {
                $('input[name="ico"]:checked').prop('checked', false);
                $('input[name="color"]:checked').prop('checked', false);
                $('#transfer_wnd .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
                atmWnd.hide('img_color_select_wnd');
                $("#img_color_select_wnd").attr("src", data.src);
            } else {
                $('#transfer_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
                $("#img_color_select_wnd").text(data.cause);
            }


        },

        error: function (xhr, errmsg, err) {
            $('#img_color_cause').text();
            console.log(xhr.status + ": " + errmsg);
            $('#img_color_select_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

/*
Status
 */
function changeStatusForm() {
    const ajaxWndName = 'set_status_wnd';
    atmWnd(
        ajaxWndName,
        'Меню изменения статуса',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    $.ajax({
        url: '/u/funcs/status_set/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data).filter('#status_change'));
            $('#status_change_form').on('submit', function (event) {
                event.preventDefault();
                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                changeStatus();
                $("#status_cause").text("");
            });
        }
    })
}

function changeStatus() {
    $.ajax({
        url: '/u/funcs/status_set/',
        type: "POST", // http method
        data: {
            status: $("#id_status").val(),
        },

        success: function (data) {
            if (data.result) {
                $("#id_status").val("");
                $("#user_status").text(data.status);
                $('#set_status_wnd .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
                atmWnd.hide('set_status_wnd');
            } else {
                $("#status_cause").text(data.cause);
                $('#set_status_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
            }


        },

        error: function (xhr, errmsg, err) {
            $('#status_cause').text();
            console.log(xhr.status + ": " + errmsg);
            $('#set_status_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

/*
Awards functions
 */
function loadAwards(uid = 1) {
    const ajaxWndName = 'awards_wnd';
    atmWnd(
        ajaxWndName,
        'Список наград',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    ajaxLoadingFirst("/u/funcs/awards/", uid, 'awards_wnd', "awards");
}

function addAwardForm(uid = 1) {
    const ajaxWndName = 'add_award_wnd';
    atmWnd(
        ajaxWndName,
        'Вручить награду',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    $.ajax({
        url: '/u/funcs/add/award/' + uid + '/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data).filter('#add_award'));
            let award_view = $("#" + ajaxWndName + " #award_view"),
                awards_list = $("#" + ajaxWndName + " #awards_list");
            $('#add_award_form select').on('change', function () {
                let award_item = awards_list.children("#award" + this.value).clone();
                award_view.html(award_item);
                award_view.children("div").children(".award_itm_img").css("display", "block");
            });
            $('#add_award_form').on('submit', function (event) {
                event.preventDefault();
                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                addAward(uid);
            });
        }
    })
}


function addAward(uid = 1) {
    $.ajax({
        url: '/u/funcs/add/award/' + uid + '/',
        type: "POST", // http method
        data: {
            value: $('#add_award_form #id_award').val(),
            msg: $("#add_award_form #id_message").val()
        },


        success: function (data) {
            if (data.result) {
                $('#id_subject').val('');
                $('#add_award_wnd .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
                atmWnd.hide('add_award_wnd');
                $("#user-awards").text(data.awards_num);
            } else {
                $('#add_award_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
                $("#award_add_fall").text(data.cause);
            }


        },

        error: function (xhr, errmsg, err) {
            $('#award_add_fall').text();
            console.log(xhr.status + ": " + errmsg);
            $('#add_award_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

function changeUsernameForm() {
    const ajaxWndName = 'change_uname_wnd';
    atmWnd(
        ajaxWndName,
        'Изменить имя пользователя',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    $.ajax({
        url: '/u/funcs/change_username/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data).filter('#change_username'));
            $('#change_username_form').on('submit', function (event) {
                event.preventDefault();
                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                changeUsername();
            });
        }
    })
}


function changeUsername() {
    $.ajax({
        url: '/u/funcs/change_username/',
        type: "POST", // http method
        data: {new_username: $('#change_username_form #id_new_username').val()},


        success: function (data) {
            if (data.result) {
                $('#id_new_username').val('');
                atmWnd.hide('change_uname_wnd');
                $("#user-username").text(data.new_username);
                $("#user-currency").text(data.money);
                $('#change_uname_wnd .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
            } else {
                $("#change_username_fall").text(data.cause);
                $('#change_uname_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
            }


        },

        error: function (xhr, errmsg, err) {
            $('#change_username_fall').text();
            console.log(xhr.status + ": " + errmsg);
            $('#change_uname_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

/*
Equipment shop
 */
function equipShopLoadForm() {
    const ajaxWndName = 'equip_shop_wnd';
    atmWnd(
        ajaxWndName,
        'Магазин снаряжения',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
        1000
    );
    let allowDeal = true,
        variablesArray = []
    $.ajax({
        url: '/u/funcs/shop/',
        success: function (data) {

            atmWnd.content(ajaxWndName, data)
            let ajaxWndForm = atmWnd.getWindow(ajaxWndName).find("form"),
                formId = "#" + ajaxWndForm.attr("id"),
                sumMoney = atmWnd.getWindow(ajaxWndName).find("#shop_sum"),
                userMoney = atmWnd.getWindow(ajaxWndName).find("#shop_u_money");
            $(formId + " input:checkbox[name='wpn_sell']," +
                "input:checkbox[name='gun_sell'], input:checkbox[name='outfit_sell']," +
                "input:checkbox[name='addons_w_sell'], input:checkbox[name='addons_p_sell']").change(function () {
                let sName = $(this).attr("name").replace("_sell", "");
                if ($(this).is(':checked')) {
                    $(formId + " #" + sName + "_list").hide();
                    $(formId + " input:radio[name='" + sName + "']").hide().prop({"disabled": true, 'checked': false});
                } else {
                    $(formId + " #" + sName + "_list").show();
                    $(formId + " input:radio[name='" + sName + "']").show().prop({"disabled": false,});
                }
            }).change();

            $(formId).change(function () {
                let wpn = $(formId + ' input:radio[name="wpn"]:checked').data("name")
                    ? $(formId + ' input:radio[name="wpn"]:checked')
                    : $(formId + ' input:checkbox[name="wpn_sell"]:checked'),
                    gun = $(formId + ' input:radio[name="gun"]:checked').data("name")
                        ? $(formId + ' input:radio[name="gun"]:checked')
                        : $(formId + ' input:checkbox[name="gun_sell"]:checked'),
                    outfit = $(formId + ' input:radio[name="outfit"]:checked').data("name")
                        ? $(formId + ' input:radio[name="outfit"]:checked')
                        : $(formId + ' input:checkbox[name="outfit_sell"]:checked'),
                    ammoW = $(formId + ' input:radio[name="ammo_w"]:checked'),
                    ammoWQuantity = intOr0($(formId + ' #ammo_w_quantity').val()),
                    ammoWSum = intOr0(ammoW.data("cost")) * ammoWQuantity,
                    ammoWTitle = ammoW.data("name") ? ammoW.data("name") + " x" + ammoWQuantity + " --  "
                        + intOr0(ammoW.data("cost")) + "ДФ" : null,
                    ammoPQuantity = intOr0($(formId + ' #ammo_p_quantity').val()),
                    ammoP = $(formId + ' input:radio[name="ammo_p"]:checked'),
                    ammoPSum = intOr0(ammoP.data("cost")) * ammoPQuantity,
                    ammoPTitle = ammoP.data("name") ? ammoP.data("name") + " x" + ammoPQuantity + " --  "
                        + intOr0(ammoP.data("cost")) + "ДФ" : null,
                    addonW = $(formId + ' input:radio[name="addon_w"]:checked').data("name")
                        ? $(formId + ' input:radio[name="addon_w"]:checked')
                        : $(formId + ' input:checkbox[name="addon_w_sell"]:checked'),
                    addonP = $(formId + ' input:radio[name="addon_p"]:checked').data("name")
                        ? $(formId + ' input:radio[name="addon_p"]:checked')
                        : $(formId + ' input:checkbox[name="addon_p_sell"]:checked'),
                    grenade = $(formId + ' input:radio[name="grenade"]:checked'),
                    grenadeQuantity = intOr0($(formId + ' #grenade_quantity').val()),
                    grenadeSum = intOr0(grenade.data("cost")) * grenadeQuantity,
                    grenadeTitle = grenade.data("name") ? grenade.data("name") + " x" + grenadeQuantity + " --  "
                        + intOr0(grenade.data("cost")) + "ДФ" : null,
                    total_upgrades = 0,
                    upgrNames = $("input:checkbox[name='upgr_w']:checked, input:checkbox[name='upgr_p']:checked, input:checkbox[name='upgr_o']:checked"),
                    upgradesNames = upgrNames.map(function () {
                        return $(this).data("name") + " --  " + $(this).data("cost") + "ДФ";
                    }).get(),
                    sum = 0,
                    namesArray = [
                        wpn.data("name") ? wpn.data("name") + " --  " + intOr0(wpn.data("cost")) + "ДФ" : null,
                        gun.data("name") ? gun.data("name") + " --  " + intOr0(gun.data("cost")) + "ДФ" : null,
                        outfit.data("name") ? outfit.data("name") + " --  " + intOr0(outfit.data("cost")) + "ДФ" : null,
                        ammoWTitle,
                        ammoPTitle,
                        grenadeTitle,
                        addonW.data("name") ? addonW.data("name") + " --  " + intOr0(addonW.data("cost")) + "ДФ" : null,
                        addonP.data("name") ? addonP.data("name") + " --  " + intOr0(addonP.data("cost")) + "ДФ" : null,
                    ];
                variablesArray = {
                    "wpn": wpn.val() ? wpn.val() : "",
                    "gun": gun.val() ? gun.val() : "",
                    "outfit": outfit.val() ? outfit.val() : "",
                    "ammoW": ammoW.val() ? {
                        "id": ammoW.val(),
                        "quantity": ammoWQuantity
                    } : "",
                    "ammoP": ammoP.val() ? {
                        "id": ammoP.val(),
                        "quantity": ammoPQuantity
                    } : "",
                    "grenade": grenade.val() ? {
                        "id": grenade.val(),
                        "quantity": grenadeQuantity
                    } : "",
                    "addonW": addonW.val() ? addonW.val() : "",
                    "addonP": addonP.val() ? addonP.val() : "",
                    "upgrW": $("input:checkbox[name='upgr_w']:checked").map(function () {
                        return $(this).val();
                    }).get(),
                    "upgrP": $("input:checkbox[name='upgr_p']:checked").map(function () {
                        return $(this).val();
                    }).get(),
                    "upgrO": $("input:checkbox[name='upgr_o']:checked").map(function () {
                        return $(this).val();
                    }).get(),
                }
                upgrNames.each(function () {
                    total_upgrades += isNaN(parseInt($(this).data("cost"))) ? 0 : parseInt($(this).data("cost"));
                });
                Array.prototype.push.apply(namesArray, upgradesNames);
                sum = intOr0(wpn.data("cost")) + intOr0(gun.data("cost")) + intOr0(outfit.data("cost")) + ammoWSum + ammoPSum + intOr0(addonW.data("cost")) + intOr0(addonP.data("cost")) + grenadeSum + total_upgrades;
                console.log(intOr0(wpn.data("cost")), intOr0(gun.data("cost")), intOr0(outfit.data("cost")), ammoWSum, ammoPSum, intOr0(addonW.data("cost")), intOr0(addonP.data("cost")), grenadeSum, total_upgrades);
                sumMoney.text(sum);
                if (intOr0(sumMoney.text()) > intOr0(userMoney.text())) {
                    sumMoney.css("color", "red");
                } else {
                    sumMoney.css("color", "inherit");
                }
                $(formId + ' #buy_list').html("")
                for (const element of namesArray) {
                    if (element) {
                        $(formId + ' #buy_list').append("<li>" + element + "</li>");
                    }
                }
                if (intOr0(sumMoney.text()) > intOr0(userMoney.text())) {
                    allowDeal = false;
                    $(formId + ' #buy_list').append("<hr>" +
                        "<li style='color: red'><strong>Сумма: " + sum + "ДФ</strong></li>" +
                        "<li style='color: red'><i>Недостаточно <strong>" + (sum - intOr0(userMoney.text()))
                        + "ДФ</strong> для совершения покупки</i></li>");
                } else {
                    allowDeal = true;
                    $(formId + ' #buy_list').append("<hr><li><strong>Сумма: " + sum + "ДФ</strong></li>");
                }
                console.log(variablesArray);
            });
            $(formId).on('submit', function (event) {
                event.preventDefault();
                if (!allowDeal) {
                    alert("Денег нет, но вы держитесь")
                } else {
                    $(formId + "input[type='submit']").prop('disabled', true);
                    $(formId + ' #sending_form').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Загрузка'>Отправка данных...")

                    equipShopPost(variablesArray);
                }


            });


        }
    })
}


function equipShopPost(data) {
    $.ajax({
        url: '/u/funcs/shop/',
        type: "POST", // http method
        data: {"equip": JSON.stringify(data)},


        success: function (data) {
            if (data.result) {

                $('#equip_shop_form #sending_form').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>Успешно");
                $.ajax({
                    url: location.href,
                    type: "GET",
                    success: function (page_data) {
                        let inv = $(page_data).find('#user_inventory').html();
                        $('#user_inventory').html(inv);
                    }
                });
                atmWnd.hide("equip_shop_wnd");
                $("#equip_shop_form input[type='submit']").prop('disabled', false);
                $("#user-currency").text(data.money);
            } else {
                $("#equip_shop_form input[type='submit']").prop('disabled', false);
                $('#equip_shop_form #sending_form').html("<img src='/static/post_stalker/ajax/er.png' alt='Ошибка'>" +
                    "<b style='color: red'>" + data.cause + "</b>");

            }


        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + errmsg);
            $('#equip_shop_form #sending_form').html("<img src='/static/post_stalker/ajax/er.png' alt='Ошибка'>" +
                "<b style='color: red'>" + xhr.status + ": " + errmsg + "</b>");

        }
    });
}

/*
Edit user data
 */
function editUserForm() {
    const ajaxWndName = 'edit_user_wnd';
    atmWnd(
        ajaxWndName,
        'Изменение личной информации пользователя',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
        700
    );
    $.ajax({
        url: '/pda/edit/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data));
            $('#edit_user_form').on('submit', function (event) {
                event.preventDefault();
                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                for (let instance in CKEDITOR.instances)
                    CKEDITOR.instances[instance].updateElement();
                let data = $(this).serialize();
                console.log(data)
                editUser(data);
            });
        }
    })
}


function editUser(send_data) {
    $.ajax({
        url: '/pda/edit/',
        type: "POST", // http method
        data: JSON.stringify(send_data),


        success: function (data) {
            $('#edit_user_form #sending_form').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>Успешно");
            $.ajax({
                url: location.href,
                type: "GET",
                success: function (page_data) {
                    let personalData = $(page_data).find('#user_personal_data').html(),
                        signature = $(page_data).find('#user_signature').html();
                    $('#user_personal_data').html(personalData);
                    $('#user_signature').html(signature);
                }
            });
            $("#edit_user_wnd").fadeOut(1000);
            atmWnd.hide("edit_user_wnd");

        },

        error: function (xhr, errmsg, err) {
            $('#change_username_fall').text();
            console.log(xhr.status + ": " + errmsg);
            $('#edit_user_form .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

/*
Edit user email
 */
function editEmailForm() {
    const ajaxWndName = 'edit_user_email_wnd';
    atmWnd(
        ajaxWndName,
        'Изменение почты пользователя',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
        700
    );
    $.ajax({
        url: '/pda/edit_email/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data).find("#edit_email_form"));
            $('#edit_email_form').on('submit', function (event) {
                event.preventDefault();
                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                editEmail(data, ajaxWndName);
            });
        }
    })
}


function editEmail(email_data, ajaxWndName) {
    $.ajax({
        url: '/pda/edit_email/',
        type: "POST", // http method
        data: {'email': $("#id_email").val()},


        success: function (data) {
            $('#edit_email_form .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
            $.ajax({
                url: data.redirect_url,
                type: "GET",
                success: function (page_data) {
                    atmWnd.content(ajaxWndName, $(page_data));
                }
            });

        },

        error: function (xhr, errmsg, err) {
            $('#change_username_fall').text();
            console.log(xhr.status + ": " + errmsg);
            $('#edit_email_form .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

/*
Edit user password
 */
function editPasswordForm() {
    const ajaxWndName = 'edit_password_email_wnd';
    atmWnd(
        ajaxWndName,
        'Изменение почты пользователя',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
        700
    );
    $.ajax({
        url: '/pda/change_password/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data).find("#password_change_form"));
            $('#password_change_form').on('submit', function (event) {
                event.preventDefault();
                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                editPassword(ajaxWndName);
            });
        }
    })
}


function editPassword(ajaxWndName) {
    $.ajax({
        url: '/pda/change_password/',
        type: "POST", // http method
        data: {
            'old_password': $("#id_old_password").val(),
            'new_password1': $("#id_new_password1").val(),
            'new_password2': $("#id_new_password2").val(),
        },


        success: function (data) {
            console.log(data)
            if (data.result) {
                $('#password_change_form .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
                $.ajax({
                    url: data.redirect_url,
                    type: "GET",
                    success: function (page_data) {
                        atmWnd.content(ajaxWndName, $(page_data));
                        setTimeout(() => window.location.replace("/pda/login/"), 2500);
                    }
                });
            } else {
                $('#password_change_form .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
                $("#password_change_form #password_change_form_reload").html(data.load_html)
            }


        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + errmsg);
            $('#password_change_form .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

/*
Sign In
 */
function signInAJAX(ajaxWndName, reload = true) {
    $.ajax({
        url: '/pda/login/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data).find("#sign_in_form"));
            $('#sign_in_form').on('submit', function (event) {
                event.preventDefault();

                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                signIn(ajaxWndName, reload);
            });
        }
    })
}

function signInForm(reload = true) {
    const ajaxWndName = 'sign_in_wnd';
    atmWnd(
        ajaxWndName,
        'Изменение почты пользователя',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
        700
    );
    signInAJAX(ajaxWndName, reload)

}


function signIn(ajaxWndName, reload) {
    $.ajax({
        url: '/pda/login/',
        type: "POST", // http method
        data: {
            'identification': $("#id_identification").val(),
            'password': $("#id_password").val(),
            'remember_me': $("#id_remember_me").val(),
        },


        success: function (data) {
            console.log(data)
            if (data.result) {
                $('#sign_in_form .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
                if (reload) {
                    location.reload();
                } else {
                    setTimeout(() => atmWnd.hide(ajaxWndName), 2500);
                }
            } else {
                $('#sign_in_form .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
                $("#sign_in_form #password_change_form_reload").html(data.load_html)
            }


        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + errmsg);
            $('#sign_in_form .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

/*
 User fraction
 */
function loadFraction(uid = 1) {
    const ajaxWndName = 'fraction_wnd';
    atmWnd(
        ajaxWndName,
        'Cписок пользователей группы',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
        1000
    );
    ajaxLoadingFirst("/pda/fraction/", uid, ajaxWndName, "fraction");
}

/* Join the Fraction */
function JoinFractionForm() {
    const ajaxWndName = 'join_fraction_wnd';
    atmWnd(
        ajaxWndName,
        'Вступить в группировку',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
    );
    $.ajax({
        url: 'fraction/join/',
        success: function (data) {
            atmWnd.content(ajaxWndName, $(data));
            let fraction_view = $("#" + ajaxWndName + " #fraction_view"),
                fractions_list = $("#" + ajaxWndName + " #fractions_list");
            $('#join_fraction_form select').on('change', function () {
                let fraction_item = fractions_list.children("#fraction" + this.value).clone();
                fraction_view.html(fraction_item);
                fraction_view.children("div").children(".fraction_img").css("display", "block");
            });
            $('#join_fraction_form').on('submit', function (event) {
                $('#join_fraction_cause').text("");
                event.preventDefault();
                $('#' + ajaxWndName + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
                JoinFraction();
            });
        }
    })
}


function JoinFraction() {
    $.ajax({
        url: 'fraction/join/',
        type: "POST", // http method
        data: {
            fraction_id: $('#join_fraction_form #id_group').val(),
            comment: $("#join_fraction_form #id_user_message").val()
        },


        success: function (data) {
            if (data.result) {
                $('#join_fraction_wnd .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
                atmWnd.hide('join_fraction_wnd');
            } else {
                $('#join_fraction_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
                $("#join_fraction_cause").text(data.cause);
            }


        },

        error: function (xhr, errmsg, err) {
            $('#join_fraction_cause').text(xhr.status + ": " + errmsg);
            console.log(xhr.status + ": " + errmsg);
            $('#join_fraction_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });
}

function loadUserFractionApps(uid = 1) {
    const ajaxWndName = 'user_fraction_apps_wnd';
    atmWnd(
        ajaxWndName,
        'Cписок заявок на вступление в группировки',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
        1000
    );
    ajaxLoadingFirst("/pda/fraction/apps/", uid, ajaxWndName, "fraction");
}

function loadGroupFractionApps(uid = 1) {
    const ajaxWndName = 'group_fraction_apps_wnd';
    atmWnd(
        ajaxWndName,
        'Cписок заявок на вступление в группировку',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
        1000
    );
    ajaxLoadingFirst("/pda/fraction/apps_lead/", uid, ajaxWndName, "fraction");
}

/* Accept/Refuse joining */
function accept(pk) {
    let id = Number(pk),
        comment = $("#app_comment" + id).val();
    $("#leader_decision" + id).hide();
    $('#app_form' + id + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");
    $.ajax({
        url: "/pda/fraction/decide/accept/",
        type: 'POST',
        data: {
            'app_id': id,
            'message': comment
        },

        success: function (data) {
            if (data.result) {
                $('#app_form' + id + ' .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
            } else {
                $('#join_fraction_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
                $('#app_form' + id + ' .post_result').text(data.cause);
            }
        },
        error: function (xhr, errmsg, err) {
            $('#join_fraction_cause').text(xhr.status + ": " + errmsg);
            console.log(xhr.status + ": " + errmsg);
            $('#app_form' + id + ' .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });

    return false;
}

function refuse(pk) {
    let id = Number(pk),
        comment = $("#app_comment" + id).val();
    $("#leader_decision" + id).hide();
    $('#app_form' + id + ' .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");

    $.ajax({
        url: "/pda/fraction/decide/refuse/",
        type: 'POST',
        data: {
            'app_id': id,
            'message': comment
        },

        success: function (data) {
            if (data.result) {
                $('#app_form' + id + ' .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
            } else {
                $('#join_fraction_wnd .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
                $('#accept_group_cause').text(data.cause);
            }
        },
        error: function (xhr, errmsg, err) {
            $('#accept_group_cause').text(xhr.status + ": " + errmsg);
            console.log(xhr.status + ": " + errmsg);
            $('#app_form' + id + ' .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });

    return false;
}

function expire(pk) {
    let id = Number(pk),
        comment = $("#expire_user #expired_cause").val();
    $('#expire_user .post_result').html("<img src='/static/post_stalker/ajax/pda_anim2.gif' alt='Отправка данных'>");

    $.ajax({
        url: "/pda/fraction/decide/expel/",
        type: 'POST',
        data: {
            'uid': id,
            'message': comment
        },

        success: function (data) {
            if (data.result) {
                $('#expire_user .post_result').html("<img src='/static/post_stalker/ajax/ok.png' alt='Успешно'>");
            } else {
                $('#expire_user .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
                $('#expire_user #error_cause').text(data.cause);
            }
        },
        error: function (xhr, errmsg, err) {
            $('#expire_user #error_cause').text(xhr.status + ": " + errmsg);
            console.log(xhr.status + ": " + errmsg);
            $('#expire_user .post_result').html("<img src='/static/post_stalker/ajax/er.png' alt='Возникла ошибка'>");
        }
    });

    return false;
}

/* Avatar changing */
function changeAvatar() {
    const ajaxWndName = 'ava_wnd';
    atmWnd(
        ajaxWndName,
        'Окно для изменения аватара',
        "<img src='/static/post_stalker/ajax/pda_anim1.gif' alt='Загрузка'>Загрузка...",
        '1',
        1000,
    );
    $.ajax({
        url: "/pda/edit/avatar/",
        type: "GET",
        success: function (data) {
            atmWnd.content(ajaxWndName, data);
        }
    })
}

/* OTHER Functions */
function intOr0(value = "") {
    return parseInt(value || 0);
}

function strToBool(value) {
    if (value === "true") {
        return true
    } else if (value === "false") {
        return false
    }
}

/*
TODO:
1. Create a state windows after get response from server
 */