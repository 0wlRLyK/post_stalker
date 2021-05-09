/**
 *
 * aJax окошки. atmWnd 3.0
 *
 * Документация по ним тут:
 * https://bitbucket.org/atom-m/cms/wiki/Окна_atmWnd
 *
 *
 *    close - показывать (true) или скрывать (false) кнопку закрытия окна. По-умолчанию true
 *    time - время в секундах, после которого окно закроется. По-умолчанию 0 (не закрывать)
 *    align - задает выравнивание контента. По-умолчанию left
 *    css - массив со стилями окна
 *    callback - функция, принимающая [ответ, статус] и возвращащающая html код для сообщения внутри окна
 *
 *
 */
// Создаёт окно
function atmWnd(name, title, content, params, width = 450,) {
    if (name && name.length > 0) {
        var i = $("#" + name).length
        if (i > 0) {
            atmWnd.content(name, content)
            atmWnd.show(name)
            atmWnd.center(name)
            return false
        }
    }
    var props = $.extend({
        close: true,
        overlay: false,
        time: 0,
        align: 'left',
        css: {
            width: width,
        }
    }, params || {});

    $('body').append(atmWnd.html(name, title, content))
    // Скрывает окно
    atmWnd.hide = function (name) {
        $("#" + name).fadeOut()
        $('.overlay_' + name).fadeOut()
    }
    // Показывает окно
    atmWnd.show = function (name) {
        $("#" + name).fadeIn()
        $('.overlay_' + name).fadeIn()
    }
    // Меняет заголовок окна
    atmWnd.title = function (name, content) {
        $('#' + name + ' .atm-title').html(content)
    }
    // Меняет содержимое окна
    atmWnd.content = function (name, content) {
        $('#' + name + ' .atm-cont').html(content)
    }
    // Возвращает содержимое
    atmWnd.getWindow = function (name) {
        return $('#' + name + ' .atm-cont')
    }
    // Центрирует окно
    atmWnd.center = function (name) {
        $(window).resize(function () {
            let wnd = $('#' + name),
                mLeft = (wnd.width() % 2) / -1,
                mTop = (wnd.height() % 2) / -1;
            wnd.css({
                left: ($(window).width() - wnd.outerWidth()) / 2,
                top: ($(window).height() - wnd.outerHeight()) / 2,
                // "margin-left": mLeft,
                // "margin-top": mTop,
            });
        }).resize()
    }
    atmWnd.setWidth = function (name, width) {
        $(window).resize(function () {
            let wnd = $('#' + name),
                maxW = $(window).width();
            if (width > maxW) {
                wnd.css({
                    width: maxW,
                });
            } else {
                wnd.css({
                    width: width,
                });
            }

        }).resize()
    }

    // Меняет параметры окна
    atmWnd.param = function (name, param) {
        if (param.close == true) {
            $('#' + name + ' .atm-close').css({display: "block"})
        } else if (param.close == false) {
            $('#' + name + ' .atm-close').css({display: "none"})
        }

        if (param.overlay == true) {
            $('body').append('<div class="overlay overlay_' + name + '"></div>')
        } else {
            $('body').remove('.overlay_' + name)
        }

        if (param.css != undefined) {
            $('#' + name).css(param.css)
        }

        if (param.align != undefined) {
            $('#' + name + ' .atm-cont').css({"text-align": param.align})
        }

        if (param.time > 0) {
            setTimeout(function () {
                atmWnd.hide(name)
            }, param.time)
        }
    }
    // Меняет тип окна
    // по сути тип окна - это просто заготовка стилей
    atmWnd.type = function (name, type) {
        if (type == 'alert') {
            atmWnd.param(name, {
                close: false,
                overlay: false,
                css: {left: 'auto', top: 'auto', right: '30px', top: '65px'}
            })
        } else if (type == 'grand') {
            atmWnd.param(name, {
                close: true,
                overlay: true,
                css: {left: '40%', top: '40%', right: 'auto', bottom: 'auto'}
            })
        }
    }

    atmWnd.param(name, props)
    atmWnd.center(name)
    atmWnd.setWidth(name, width)
    atmWnd.show(name)

}

// Template AtmWindow
atmWnd.html = function (id, title, content) {
    return '<div id="' + id + '" class="atm-fwin" style="display: none"> \
            <div class="drag_window"> \
            <div class="wnd_left_drag" onmousedown="drag_object(event, this.parentNode)"></div>\
            <div class="wnd_bottom_drag" onmousedown="drag_object(event, this.parentNode)"></div>\
              <div class="atm-title" onmousedown="drag_object(event, this.parentNode)">' + title + '</div> \
              <div onClick="atmWnd.hide(\'' + id + '\')" class="atm-close"></div> \
              <div class="atm-cont-wrap"><div class="atm-cont">' + content + '</div></div> \
            </div> \
        </div>';
}

// Создание окна с необычным содержимым
// {type: "dom", source: ".class"} - содержимое со страницы из элемента с классом class
// {type: "url", source: "/path/to/file.htm"} - выводит содержимое любой страницы сайта
function atmWndData(name, title, data, params) {
    var data = $.extend({
        type: "",
        source: "",
        ajax_type: "POST",
        data: {}
    }, data || {});

    var content;
    atmWnd(name, title, atmWnd.loader_tpl, params)
    if (data['type'] == 'dom') {
        content = $(data['source']).html()
        atmWnd.content(name, content)
        return
    } else if (data['type'] == 'url') {
        jQuery.ajax({
            url: data['source'],
            type: data['ajax_type'],
            data: data['data'],
            success: function (response) {
                content = response
                if (params.callback != undefined)
                    content = params.callback(content, 'success');
                atmWnd.content(name, content)
                return
            },
            error: function (response) {
                content = response
                if (params.callback != undefined)
                    content = params.callback(content, 'error');
                atmWnd.content(name, content)
                return
            }
        })
    } else {
        content = 'error'
        atmWnd.content(name, content)
        return
    }
}

// HTML for loading
atmWnd.loader_tpl = '<span id="loader"><img src="/static/post_stalker/ajax/pda_anim1.gif" alt="loading"></span>';
// HTML for progress
atmWnd.progress_tpl = '<progress min="0" max="100" value="0">0% complete</progress>';
// Function for progress
sendu.progress = function (e) {
    var progressBar = document.querySelector('progress')
    if (e.lengthComputable) {
        progressBar.value = (e.loaded / e.total) * 100
        progressBar.textContent = progressBar.value // Если браузер не поддерживает элемент progress
    }
}
// Function for full update page
sendu.update_page = function (obj, url, is_new_load) {
    if (is_new_load === true) {
        nhash = url.indexOf('#')
        if (nhash === -1) nhash = undefined;
        ohash = document.location.href.indexOf('#')
        if (ohash === -1) ohash = undefined;
        if (document.location.href.substring(0, ohash) == url.substring(0, nhash)) {
            if (typeof nhash != 'undefined')
                document.location.href = url;
            document.location.reload()
        } else
            document.location.href = url;

    } else {
        var content = $('body').html();
        history.pushState({}, '', url);
        $('body').html(obj.response);
        $(window).bind('popstate', function () {
            $('body').html(content);
        });
    }
}
// Дополнительная обработка URL
sendu.parseurl = function (url) {
    if (url.indexOf("?") > -1)
        url += '&ajax=true';
    else
        url += '?ajax=true';
    return url;
};

// Отправляет форму на сервер и открывает окно со статусом выполненного действия
function sendu(e, ret, params) {
    if (e instanceof Object != true) {
        e = $('#' + e)
    }
    var name = 'atmWinSendu',
        title = 'Информация',
        url, formname, formData;

    setTimeout(function () {
        if ($(e).attr("action")) {
            atmWnd(name, title, atmWnd.progress_tpl, params)
            formname = $(e).attr("name")
            formData = new FormData(document.forms[formname])
            url = $(e).attr("action")
        } else {
            atmWnd(name, title, atmWnd.loader_tpl, params)
            url = $(e).attr("href")
        }

        atmWnd.type(name, 'alert')
        xhr = new XMLHttpRequest()
        xhr.open('POST', sendu.parseurl(url), true)
        xhr.onload = function (e) {

            if (this.status == 200) {
                // Если ошибка, или нужно что то почитать в окошке
                if (this.getResponseHeader('ResponseAjax') == 'error' || this.getResponseHeader('ResponseAjax') == 'grand') {
                    atmWnd.content(name, this.response)
                    atmWnd.type(name, 'grand')
                    // Если пришло сообщение об успешном выполнении операции
                } else if (this.getResponseHeader('ResponseAjax') == 'ok') {
                    atmWnd.content(name, this.response)
                    if (this.getResponseHeader('Refresh')) {
                        // если ответ OK и содержит редирект то загружаем страницу по адресу в редиректе
                        s = this.getResponseHeader('Refresh').split('url=');
                        // Дополнительные действия, если нужно
                        var out;
                        if (ret != undefined)
                            out = ret(this, s[1]);
                        if (out != false)
                            sendu.update_page(this, s[1], true);
                    } else {
                        // если ответ OK, но нет редиректа, то выполняем callback функцию(предполагается, что отобразить изменения на странице можно незначительными преобразованиями)
                        if (ret != undefined)
                            ret(this, url);
                        // Если ответ OK но нет ни редиректа ни callback функции, то просто обновляем текущую страницу
                        else
                            sendu.update_page(this, window.location.pathname, true);
                    }
                    // При ответе ok не может быть сообщений сильно нагруженных информацией, через 5 сек скрываем любое такое сообщение.
                    atmWnd.param(name, {time: 5000})

                    // Если статус неизвестен значит вернулась полноценная страница, а не сообщение
                } else {
                    atmWnd.hide(name)
                    sendu.update_page(this, url, false)
                }
            } else {
                atmWnd.content(name, 'Произошла неизвестная ошибка')
            }

        }

        if ($(e).attr("action")) {
            // Слушаем процесс загрузки файла
            xhr.upload.onprogress = sendu.progress(e)
            xhr.send(formData)
        } else {
            xhr.send()
        }
    }, 1)
    // костыль, чтобы визуальный редактор успел отправить сформированное сообщение в textarea
}


/**
 * For Atom Windows
 */
function drag_object(evt, obj) {
    evt = evt || window.event;

    // флаг, которые отвечает за то, что мы кликнули по объекту (готовность к перетаскиванию)
    obj.clicked = true;

    // устанавливаем первоначальные значения координат объекта
    obj.mousePosX = evt.clientX;
    obj.mousePosY = evt.clientY;

    // отключаем обработку событий по умолчанию, связанных с перемещением блока (это убирает глюки с выделением текста в других HTML-блоках, когда мы перемещаем объект)
    if (evt.preventDefault) evt.preventDefault();
    else evt.returnValue = false;

    // когда мы отпускаем кнопку мыши, убираем «проверочный флаг»
    document.onmouseup = function () {
        obj.clicked = false
    }

    // обработка координат указателя мыши и изменение позиции объекта
    document.onmousemove = function (evt) {
        evt = evt || window.event;
        if (obj.clicked) {
            posLeft = !obj.style.left ? obj.offsetLeft : parseInt(obj.style.left);
            posTop = !obj.style.top ? obj.offsetTop : parseInt(obj.style.top);

            mousePosX = evt.clientX;
            mousePosY = evt.clientY;

            obj.style.left = posLeft + mousePosX - obj.mousePosX + 'px';
            obj.style.top = posTop + mousePosY - obj.mousePosY + 'px';

            obj.mousePosX = mousePosX;
            obj.mousePosY = mousePosY;
        }
    }
}