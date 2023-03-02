// Cart add remove functions


$(document).ready(function () {

    // ============ Прелоадер
    $(".preloader").hide();


    // ============ Кастомный выбор даты
    $('[data-toggle="datepicker"]').datepicker({
        language: 'ru-RU',
        format: 'dd-mm-yyyy'
    });

    // ============ Создание маски для поля ввода номера телоефона
    $('input[type="tel"]').mask('+38 (000) 000-00-00');

    /* Search */


    // ==================================== Общее функции ==================================== //


    // ============ Выполнять действие при клике вне елемента [аргумент 1: елемент], [аргумент 2: действие]
    function clickOutside(element, action) {
        var el = $(element);
        $(document).mouseup(function (e) {
            if (!el.is(e.target) && el.has(e.target).length === 0) {
                action(el);
            }
        });
    }


    // ============ Определение типа управления touch | mouse
    function device_type() {
        if ("ontouchstart" in document.documentElement) {
            touch_elements_support();

            return 'touch';
        } else {
            mouse_elements_support();

            return 'mouse';
        }
    }

    var device = device_type(); // Переменная которая сотержит тип устройства = 'mouse' / touch'


    // ============ Функции работы интерфейса для управления с помощу mouse / для десктопов
    function mouse_elements_support() {

        // Открыть выбор языка при наведении
        $(".header__language").hover(function () {
            $(this).addClass("active");
        }, function () {
            $(this).removeClass("active");
        });
    }


    // ============ Функции работы интерфейса для управления с помощу touch / для мобильных устройств
    function touch_elements_support() {

        // Открыть меню выбора языка при клике
        $(".header__language").click(function () {
            $(this).toggleClass("active");
        });

        // При клике вне меню выбора языка закрыть его
        function clickOutside__language(el) {
            el.removeClass("active");
        }

        clickOutside(".header__language", clickOutside__language);
    }

    // ==================================== /.Общее функции ==================================== //


    // ==================================== Инициализации каталога ==================================== //
    function initCatalog() {
        var catalog_wrap = $(".header__catalog")
        var catalog = $(".header__catalog-menu");

        // Добавление класов уровня [level-0 > level-1 > level 2]
        catalog.find("ul").each(function () {
            var levels = $(this).parents("ul").map(function () {
                return this;
            }).get();

            var level = levels.length;
            $(this).addClass("header__catalog-menu__level-" + level);
        });

        // Добавление класса .has-child и создание заголовков подкатегорий
        catalog.find("li > ul").each(function () {
            $(this).parent().addClass("has-child");
        });

        // Активировать кастомную прокрутку
        catalog.find("ul.header__catalog-menu__level-0, ul.header__catalog-menu__level-1").each(function () {
            $(this).mCustomScrollbar({
                scrollInertia: 300,
                moveDragger: true,
                mouseWheel: {preventDefault: true},
                setTop: 0
            });
        });

        function setWidth() {
            var padding = 30;

            if ($(window).width() < 1299) {
                padding = 20;
            }

            $(".header__catalog-menu__level-1").width($(".header__bottom .container").width() - $(".header__catalog-menu__level-0").width() - padding);

            $(window).resize(function () {
                setWidth();
            });
        }

        setWidth();


        // Открыть закрыть при навидении
        if (device === 'mouse') {
            catalog.find(".header__catalog-menu__level-0 > div > div > li").hover(function () {
                $(this).addClass("active");
            }, function () {
                $(this).removeClass("active");
            });

            $(".header__catalog-btn, .header__catalog-menu__level-0").hover(function () {
                catalog_wrap.addClass("active");
            }, function () {
                catalog_wrap.removeClass("active");
            });
        }

        // Открыть закрыть при клике
        if (device === 'touch') {
            $(".header__catalog-btn").click(function () {
                catalog_wrap.toggleClass("active");

                return false;
            });

            catalog.addClass("header__catalog-menu--touch");
            catalog.find(".header__catalog-menu__level-0 > div > div > li > a").click(function (e) {

                var div = $(this).find("span");
                if (!div.is(e.target) && div.has(e.target).length === 0) {
                    $(this).parent().parent().find("li").not($(this)).removeClass("active");
                    $(this).parent().toggleClass("active");

                    return false;
                }
            });

            // При клике вне каталога закрыть его
            function clickOutside__catalog(el) {
                el.find("li.active").removeClass("active");
                catalog_wrap.removeClass("active");
            }

            clickOutside(catalog.find("ul"), clickOutside__catalog);
        }
    }

    initCatalog();
    // ==================================== /.Инициализации каталога ==================================== //


    // ==================================== Инициализация Слайдеров ==================================== //

    // ============ Работа слайдера "Promo Slider"
    $(".promo__slider").slick({
        infinite: true,
        slide: '.promo__slider-slide',
        slidesToShow: 1,
        slidesToScroll: 1,
        speed: 1000,
        dots: true,
        arrow: true,
        autoplay: true,
        autoplaySpeed: 10000,
        appendArrows: '.promo__slider-controls .slick-controls__arrows',
        appendDots: '.promo__slider-controls .slick-controls__dots',
        animationPrev: 'promo__slider--prev',
        animationNext: 'promo__slider--next',
        fade: true,
        cssEase: 'linear',
    });


    // ============ Работа слайдера "Products Slider"
    $(".products-slider").each(function () {

        var slider = $(this);
        var slider_arrows = $(this).find(".slick-controls__arrows");
        var slider_dots = $(this).find(".slick-controls__dots");

        if (slider.hasClass("products-slider--1")) {
            slider.slick({
                infinite: true,
                slide: ".products-slider__slide",
                slidesToShow: 4,
                slidesToScroll: 1,
                speed: 100,
                dots: true,
                arrow: true,
                appendArrows: slider_arrows,
                appendDots: slider_dots,
                swipeToSlide: true,
                responsive: [
                    {
                        breakpoint: 992,
                        settings: {
                            slidesToShow: 3,
                        }
                    },
                    {
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 2,
                        }
                    }
                ]
            });
        } else {
            slider.slick({
                infinite: true,
                slide: ".products-slider__slide",
                slidesToShow: 4,
                slidesToScroll: 1,
                speed: 500,
                dots: true,
                arrow: true,
                appendArrows: slider_arrows,
                appendDots: slider_dots,
                swipeToSlide: true,
                responsive: [
                    {
                        breakpoint: 1300,
                        settings: {
                            slidesToShow: 3,
                        }
                    },
                    {
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 2,
                        }
                    }
                ]
            });
        }
    });


    // ============ Работа слайдера "News Slider"
    $(".news-slider").each(function () {

        var slider = $(this);
        var slider_arrows = $(this).find(".slick-controls__arrows");
        var slider_dots = $(this).find(".slick-controls__dots");

        slider.slick({
            infinite: true,
            slide: ".news-slider__slide",
            slidesToShow: 3,
            slidesToScroll: 1,
            speed: 1000,
            dots: true,
            arrow: true,
            appendArrows: slider_arrows,
            appendDots: slider_dots,
            swipeToSlide: true,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 2,
                    }
                },
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 3,
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 2,
                    }
                },
                {
                    breakpoint: 400,
                    settings: {
                        slidesToShow: 1,
                    }
                }
            ]
        });
    });
    // ==================================== /.Инициализация Слайдеров ==================================== //


    // ==================================== Изменение расположения секций на устройствах шириной менее 991px ==================================== //
    var resize;
    var resize_memory = 'desktop';

    function re_build_page() {

        if (!$("body").hasClass("page--product")) {
            if ($(window).outerWidth() <= 991) {
                resize = 'mobile';
            }
            if ($(window).outerWidth() >= 992) {
                resize = 'desktop';
            }
        } else {
            if ($(window).outerWidth() <= 1199) {
                resize = 'mobile';
            }
            if ($(window).outerWidth() >= 1200) {
                resize = 'desktop';
            }
        }

        if (resize_memory != resize) {

            // Перемещение если Мобильное устройство
            if (resize == 'mobile') {

                // Перемещение блока "Информация"
                $(".js_useful-info--desktop .useful-info").detach().appendTo(".js_useful-info--mobile");

                // Перемещение блока "Консультация"
                $(".js_consultation--desktop .consultation").detach().appendTo(".js_consultation--mobile");

                // Перемещение блока "Нужна помощ в выборе ?"
                $(".js_help--desktop .help").detach().appendTo(".js_help--mobile");


                // Перемещение отзывов
                $(".js_reviews--desktop > .review-card").each(function () {
                    var review = $(this).detach();
                    $(".js_reviews--mobile").append(review);
                }).promise().done(function () {
                    $(".js_reviews--mobile > .review-card").wrap('<div class="col-6"></div>');
                });

                // Перемещение блока "Акссесуары"
                $(".js_accessories--desktop .accessories__item").each(function () {
                    var review = $(this).detach();
                    $(".js_accessories--mobile .accessories").append(review);
                }).promise().done(function () {
                    $(".js_accessories--mobile .accessories__item").wrap('<div class="col-4"></div>');
                });

                // Перемещение фильтров каталога
                $("footer").after($(".js_catalog-filter > .catalog-filter").detach());
            }

            // Перемещение если устройство Десктоп
            if (resize == 'desktop') {

                // Перемещение блока "Информация"
                $(".js_useful-info--mobile .useful-info").detach().appendTo(".js_useful-info--desktop");

                // Перемещение блока "Консультация"
                $(".js_consultation--mobile .consultation").detach().appendTo(".js_consultation--desktop");

                // Перемещение блока "Нужна помощ в выборе ?"
                $(".js_help--mobile .help").detach().appendTo(".js_help--desktop");

                // Перемещение отзывов
                $(".js_reviews--mobile .review-card").each(function () {
                    var review = $(this).detach();
                    $(".js_reviews--desktop").append(review);
                });
                $(".js_reviews--mobile").empty();

                // Перемещение блока "Акссесуары"
                $(".js_accessories--mobile .accessories__item").each(function () {
                    var review = $(this).detach();
                    $(".js_accessories--desktop .accessories__content").append(review);
                }).promise().done(function () {
                    $(".js_accessories--mobile .accessories").empty();
                });


                // Перемещение фильтров каталога
                $(".catalog-filter").detach().appendTo(".js_catalog-filter");
            }
            resize_memory = resize;
        }
    }

    $(window).resize(function () {
        re_build_page();
    });
    re_build_page()
    // ==================================== /.Изменение расположения секций на устройствах шириной менее 991px ==================================== //


    // ==================================== Работа Табов ==================================== //
    $(".tabs").each(function () {
        var tabs = $(this);
        var tabs_nav = $(this).find(".tabs__nav-item");
        var tabs_tab = $(this).find(".tabs__tab");

        // Делаем активным первый таб
        tabs_nav.first().addClass("active");
        tabs_tab.not(':first').hide();

        tabs_nav.click(function () {
            tabs_nav.removeClass('active').eq($(this).index()).addClass('active');
            tabs_tab.hide().eq($(this).index()).fadeIn();

            if (tabs.find(".slick-slider").length) {
                tabs.find(".slick-slider").slick('setPosition');
            }
            $(".form__rating  .rateit33").rateit({max: 5, step: 1, mode: "font", starwidth: 20});
            return false;
        });
    });

    // Горизонтальная прокрутка навигации табов
    $(".tabs__nav--scrolling").mCustomScrollbar({
        axis: "x",
        scrollEasing: "linear",
        scrollInertia: 500,
        moveDragger: true,
        scrollbarPosition: "outside",
        moveDragger: true,
        mouseWheel: {preventDefault: true},
    });
    // ==================================== /.Работа Табов ==================================== //


    // ==================================== Работа прочих елементов интерфейса ==================================== //

    // ============ Работа поиска на мобильном

    // Открыть поиск на мобильных
    $(".header__m-search-open").click(function () {
        if (!$(".header").hasClass("search--active")) {
            $(".header").addClass("search--active");
            $(this).addClass("opn");
            $(".header").find("input").focus();
            return false;
        }
    });

    // Закрыть поиск на мобильных
    $(".header__m-search-close").click(function () {
        $('#livesearch_search_results').remove();
        updown = 0;
        $(this).parents(".header").removeClass("search--active");
        return false;
    });


    // ============ Работа модального окна обратной связи

    // При клике вне модального окна
    function clickOutside__popup(el) {
        $("body").removeClass("callback-popup--active");
    }

    clickOutside($("#orderModal"), clickOutside__popup);

    // Открыть / Закрыть модальное окно обратной связи
    $(".js-callback-popup").click(function () {
        $("body").removeClass("mobile-menu--active");
        $("body").toggleClass("callback-popup--active");
        return false;
    });

    // Закрыть модальное окно при нажатии на кнопку ESC
    $(document).keydown(function (e) {
        if (e.which == 27) {
            $("body").removeClass("callback-popup--active");
        }
    });

    function clickOutside__popup2(el) {
        $("body").removeClass("popup-popup--active");
    }

    clickOutside($("#popupModal"), clickOutside__popup2);

    // Открыть / Закрыть модальное окно обратной связи
    $(".popup__close").click(function () {
        $("body").removeClass("mobile-menu--active");
        $("body").removeClass("popup-popup--active");
        return false;
    });

    function clickOutside__popup3(el) {
        $("body").removeClass("ord-popup--active");
    }

    clickOutside($("#ordModal"), clickOutside__popup3);
    $(".ord__close").click(function () {
        $("body").removeClass("mobile-menu--active");
        $("body").removeClass("ord-popup--active");
        return false;
    });

    function clickOutside__popup8(el) {
        $("body").removeClass("preord-popup--active");
    }

    clickOutside($("#preordModal"), clickOutside__popup8);
    $(".preord__close").click(function () {
        $("body").removeClass("mobile-menu--active");
        $("body").removeClass("preord-popup--active");
        return false;
    });


    function clickOutside__popup9(el) {
        $("body").removeClass("getprice-popup--active");
    }

    clickOutside($("#getpriceModal"), clickOutside__popup9);
    $(".getprice__close").click(function () {
        $("body").removeClass("mobile-menu--active");
        $("body").removeClass("getprice-popup--active");
        return false;
    });

    function clickOutside__popup4(el) {
        $("body").removeClass("sk");
        $('.popup_mask').hide();
        $('.window_holder1').hide();
    }

    clickOutside($(".white-saas-generator"), clickOutside__popup4);


    // ==================================== /.Работа прочих елементов интерфейса ==================================== //


    // ==================================== Скрипты для страниц личного кабинета ==================================== //


    // ============ Установка класса для таблицы сравнения
    $(".compare-table table").addClass("compare-" + $(".compare-table table tr").first().find("td").length);

    // ============ Прокурутка таблицы сравнения
    $(".compare-table").mCustomScrollbar({
        axis: "x",
        scrollEasing: "linear",
        scrollInertia: 500,
        moveDragger: true,
        scrollbarPosition: "outside",
    });


    // ==================================== /.Скрипты для страниц личного кабинета ==================================== //


});


document.addEventListener('DOMContentLoaded', function () {
    $(".header__m-search-form").find("[name=searchmob]").first().keyup(function (a) {

        doLiveSearchMobile(a, this.value)
    }).blur(function () {
        window.setTimeout("$('#livesearch_search_results').remove();updown=0;", 1500)
    })

    $("#search").find("[name=search]").first().keyup(function (a) {
        doLiveSearch(a, this.value)
    }).blur(function () {
        window.setTimeout("$('#livesearch_search_results').remove();updown=0;", 1500)
    }), $(document).bind("keydown", function (a) {
        try {
            13 == a.keyCode && $(".highlighted").length > 0 && (document.location.href = $(".highlighted").find("a").first().attr("href"))
        } catch (a) {
        }
    });

});


function doLiveSearch(a, b) {
    return 38 != a.keyCode && 40 != a.keyCode && ($("#livesearch_search_results").remove(), updown = -1, !("" == b || b.length < 3 || (b = encodeURI(b), $.ajax({
        url: $("base").attr("href") + "index.php?route=product/search/ajax&keyword=" + b + "&filter_category_id=" + $('#search input[name=category_id]').val(),
        dataType: "json",
        success: function (a) {
            if (a.length > 0) {
                var c = document.createElement("ul");
                c.id = "livesearch_search_results";
                var d, e;
                for (var f in a) {
                    if (d = document.createElement("li"), eListHr = document.createElement("hr"), eListDiv = document.createElement("div"), eListDiv.setAttribute("style", "height: 10px; clear: both;"), eListDivpr = document.createElement("span"), eListDivpr.innerHTML = a[f].price, eListDivpr.setAttribute("style", "height: 14px; color: #147927;"), eListDivprspec = document.createElement("span"), eListDivprspec.innerHTML = a[f].special, eListDivprspec.setAttribute("style", "font-weight: bold; margin-left: 8px; color: #a70d0d; font-size: 16px;"), eListImg = document.createElement("img"), eListImg.src = a[f].image, eListImg.setAttribute("style", "margin-right: 10px;"), eListImg.align = "left", eListDivstatus = document.createElement("span"), eListDivstatus.innerHTML = a[f].stock, eListDivstatus.setAttribute("style", "height: 14px; color: #337ab7; margin-left: 15px; font-weight: bold;"), e = document.createElement("a"), e.setAttribute("style", "display: block;"), e.appendChild(document.createTextNode(a[f].name)), "undefined" != typeof a[f].href) {
                        "" != a[f].special && eListDivpr.setAttribute("style", "text-decoration: line-through;");
                        var g = a[f].href;
                        e.href = g.replace(/&amp;/g, "&")
                    } else e.href = $("base").attr("href") + "index.php?route=product/product&product_id=" + a[f].product_id + "&keyword=" + b;
                    d.appendChild(e), c.appendChild(eListImg), c.appendChild(d), c.appendChild(eListDivpr), "" != a[f].special && c.appendChild(eListDivprspec), c.appendChild(eListDivstatus), c.appendChild(eListHr), c.appendChild(eListDiv)
                }
                $("#livesearch_search_results").length > 0 && $("#livesearch_search_results").remove(), $("#search").append(c), $("#livesearch_search_results").css("display", "none"), $("#livesearch_search_results").slideDown("slow"), $("#livesearch_search_results").animate({
                    backgroundColor: "rgba(255, 255, 255, 0.98)"
                }, 2e3)
            }
        }
    }), 0)))
}

function doLiveSearchMobile(a, b) {
    return 38 != a.keyCode && 40 != a.keyCode && ($("#livesearch_search_results").remove(), updown = -1, !("" == b || b.length < 3 || (b = encodeURI(b), $.ajax({
        url: $("base").attr("href") + "index.php?route=product/search/ajax&keyword=" + b,
        dataType: "json",
        success: function (a) {
            if (a.length > 0) {
                var c = document.createElement("ul");
                c.id = "livesearch_search_results";
                var d, e;
                for (var f in a) {
                    if (d = document.createElement("li"), eListHr = document.createElement("hr"), eListDiv = document.createElement("div"), eListDiv.setAttribute("style", "height: 10px; clear: both;"), eListDivpr = document.createElement("span"), eListDivpr.innerHTML = a[f].price, eListDivpr.setAttribute("style", "height: 14px; color: #147927;"), eListDivprspec = document.createElement("span"), eListDivprspec.innerHTML = a[f].special, eListDivprspec.setAttribute("style", "font-weight: bold; margin-left: 8px; color: #a70d0d; font-size: 16px;"), eListImg = document.createElement("img"), eListImg.src = a[f].image, eListImg.setAttribute("style", "margin-right: 10px;"), eListImg.align = "left", eListDivstatus = document.createElement("span"), eListDivstatus.innerHTML = a[f].stock, eListDivstatus.setAttribute("style", "height: 14px; color: #337ab7; margin-left: 15px; font-weight: bold;"), e = document.createElement("a"), e.setAttribute("style", "display: block;"), e.appendChild(document.createTextNode(a[f].name)), "undefined" != typeof a[f].href) {
                        "" != a[f].special && eListDivpr.setAttribute("style", "text-decoration: line-through;");
                        var g = a[f].href;
                        e.href = g.replace(/&amp;/g, "&")
                    } else e.href = $("base").attr("href") + "index.php?route=product/product&product_id=" + a[f].product_id + "&keyword=" + b;
                    d.appendChild(e), c.appendChild(eListImg), c.appendChild(d), c.appendChild(eListDivpr), "" != a[f].special && c.appendChild(eListDivprspec), c.appendChild(eListDivstatus), c.appendChild(eListHr), c.appendChild(eListDiv)
                }
                $("#livesearch_search_results").length > 0 && $("#livesearch_search_results").remove(), $(".header__m-search-form").append(c), $("#livesearch_search_results").css("display", "none"), $("#livesearch_search_results").slideDown("slow"), $("#livesearch_search_results").animate({
                    backgroundColor: "rgba(255, 255, 255, 0.98)"
                }, 2e3)
            }
        }
    }), 0)))
    /*     if( ev.keyCode == 38 || ev.keyCode == 40 ) {
return false;
}

$('#livesearch_search_results').remove();
updown = -1;

if( keywords == '' || keywords.length < 3 ) {
return false;
}
keywords = encodeURI(keywords);

$.ajax({url: $('base').attr('href') + 'index.php?route=product/search/ajax&keyword=' + keywords, dataType: 'json', success: function(result) {


     if( result.length > 0 ) {
    console.log(result);


var eList = document.createElement('ul');
eList.id = 'msearchresults';
var eListElem;
var eLink;
for( var i in result ) {
    eListElem = document.createElement('li');

eListDiv = document.createElement('div');
eListDiv.setAttribute("style", "height: 10px; clear: both;");

eListDivpr = document.createElement("span");
eListDivpr.innerHTML = result[i].price;
eListDivpr.setAttribute("style", "height: 14px; color: #147927;");
"" != result[i].special && eListDivpr.setAttribute("style", "text-decoration: line-through;");

eListDivprspec = document.createElement("span");
eListDivprspec.innerHTML = result[i].special;
eListDivprspec.setAttribute("style", "font-weight: bold; margin-left: 8px; color: #a70d0d; font-size: 16px;");

eListImg = document.createElement('img');
eListImg.src = result[i].image;
eListImg.setAttribute("style", "margin-right: 10px;");
eListImg.align = 'left';

eLink = document.createElement('a');
eLink.setAttribute("style", "display: block;");
    eLink.appendChild( document.createTextNode(result[i].name) );
    if( typeof(result[i].href) != 'undefined' ) {
        var convertlink = result[i].href;
        eLink.href = convertlink.replace(/&amp;/g, "&");

    } else {
        eLink.href = $('base').attr('href') + 'index.php?route=product/product&product_id=' + result[i].product_id + '&keyword=' + keywords;
    }
    eListElem.appendChild(eLink);
eList.appendChild(eListImg);
    eList.appendChild(eListElem);
eList.appendChild(eListDivpr);
"" != result[i].special && eList.appendChild(eListDivprspec);
    eList.appendChild(eListDiv);
}
if( $('#msearchresults').length > 0 ) {
    $('#msearchresults').remove();
}
$('#searchm').append(eList);
}
}});

return true;*/
}

function upDownEvent(a) {
    var b = document.getElementById("livesearch_search_results");
    if ($("#search").find("[name=search]").first(), b) {
        var c = b.childNodes.length - 1;
        if (updown != -1 && "undefined" != typeof b.childNodes[updown] && $(b.childNodes[updown]).removeClass("highlighted"), 38 == a.keyCode ? updown = updown > 0 ? --updown : updown : 40 == a.keyCode && (updown = updown < c ? ++updown : updown), updown >= 0 && updown <= c) {
            $(b.childNodes[updown]).addClass("highlighted");
            var d = b.childNodes[updown].childNodes[0].text;
            "undefined" == typeof d && (d = b.childNodes[updown].childNodes[0].innerText), $("#search").find("[name=search]").first().val(new String(d).replace(/(\s\(.*?\))$/, ""))
        }
    }
    return !1
}