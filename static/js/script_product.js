$(document).ready(function() {
	
	// ==================================== Скрипты для страницы товара ==================================== //
 	function product_gallary(){

 		// Большое фото товара
		var detail = $("#product-detail");

		// Маленькое фото товара
		var product_gallery = $('#product-gallery > .product-gallery__item');

		// Установить первое фото
		product_gallery.eq(0).addClass("active");
		detail.attr("data-index", 0).attr("href", product_gallery.eq(0).find("> a").attr("href"));
		detail.find("img").attr("src", product_gallery.eq(0).find("> a").attr("href"));
		detail.find("source").attr("srcset", product_gallery.eq(0).find("> a").attr("href"));


		// При клике на слайд сделать активным и открыть текущее фото
		product_gallery.find("> a").on("click", function(e) {
		   e.preventDefault();		

		   var current_index = $(this).parents('.product-gallery__item').index(),
	    		 current_image = $(this).attr("href");

		   // Сделать активным при клике
		   $(".product-gallery__item").removeClass("active");
		   $(this).parent().addClass("active");


		   detail.attr("data-index", current_index).attr("href", current_image);
		   detail.find("img").attr("src", current_image);
		   detail.find("source").attr("srcset", current_image);

		   return false;
		});


		// Работа Fancybox
		$(".product-gallery__detail").on("click", function (){
			$.fancybox.open(product_gallery.find("> a"),{}, detail.attr('data-index'));
			return false;
		});
 	}
 	product_gallary();


 	// ============ Установка рейтинга
 	function set_rating(){

 	}

 	set_rating();
	

	// ============ Скролить до характеристик
 	$(".js_to-parameters").click(function (){
 		$(".js_parameters").click();
 		$('html, body').animate({
         scrollTop: $(".product-tabs").offset().top - 30
      }, 500);

 		return false;
 	});


 	// ============ Просмотр фото в отзывах
 	$(".product-comment__photo").each(function (){
 		$(this).find("a").attr("data-fancybox", "reviews_photo-" + $(this).index());
 	}); 

});

$(document).ready(function() {

	// ==================================== Работа каталога ==================================== //

	$(document).on("click", ".js_filter", function (){
		 $("body").toggleClass("catalog-filter--active");


	 	return false;
	});

	// Добавить overlay для фильров
	$("footer").after(`<div class="catalog-filter__overlay js_filter"></div>`);

	// Открыть все фильтры
	$(".catalog-filter__group").each(function (){
		$(this).addClass("active");
	});

	// Открыть / Скрыть филтр
	$(".catalog-filter__group-title").click(function (){
		$(this).parent().toggleClass("active");
		$(this).parent().find(".catalog-filter__group-content").slideToggle();
	});

	// Установить прокрутку если елементы фильтра не помещаються
   $(".catalog-filter__select-box").each(function (){
   	if($(this).find(".catalog-filter__checkbox").length > 7){
   		$(this).parent().parent().addClass("scroll");
   	}
   });


	// ============ ИНициализация позунка для выбора цены
	function	init_price_slider(){
		var price__slider = document.getElementById("filter-price__slider");
		var price__min = document.getElementById("filter-price__min");
		var price__max = document.getElementById("filter-price__max");
                if(price__max != null) {
		noUiSlider.create(price__slider, {
		   start: [0, parseInt(price__max.getAttribute("max"))],
		   connect: true,
		   step: 1,
		   range: {
		      'min': parseInt(price__min.getAttribute("min")),
		      'max': parseInt(price__max.getAttribute("max"))
		   }
		});

		price__slider.noUiSlider.on('update', function (values, handle) {
		   var value = values[handle];
		   if(handle){
		      price__max.value =  Math.round(value);
		   } else{
		      price__min.value = Math.round(value);
		   }
		});

		price__min.addEventListener('change', function () {
		   price__slider.noUiSlider.set([this.value, null]);
		});

		price__max.addEventListener('change', function () {
		   price__slider.noUiSlider.set([null, this.value]);
		});

            }
	}
	init_price_slider();


	// Изменить вид просмотра товара
	$("[data-view]").click(function (){
		$(this).addClass("active").siblings().removeClass("active");
		if($(this).data("view") === "row"){
			$(".catalog-products").addClass("catalog-view--row");
		}else{
			$(".catalog-products").removeClass("catalog-view--row");
		}
		return false;
	});

	// ==================================== /.Работа каталога ==================================== //

});