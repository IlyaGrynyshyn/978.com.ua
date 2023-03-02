
jQuery(function($){

	function init_mobile_menu(){

		var menu = $(".mobile-menu");
		var menu_nav;
		var menu_nav_content;

		// Переменна для анимации смещения
		var transform = 0;


		// ============== Создание структуры меню и добавление классов ============== //

		// Создание Overlay
		menu.after('<div class="mobile-menu__overlay js__mobile-menu"></div>');

		// Добавление классов  
		menu.find(".mobile-menu__content > ul").each(function (){
			$(this).addClass("mobile-menu__nav");

			menu_nav = $(".mobile-menu__nav");
		});

		// Добавление класса .has-child 
		menu_nav.find("li > ul").each(function (){			
			$(this).parent().addClass("has-child");
		});

		// Создание структуры подменю
		menu_nav.find("ul").each(function (){
			$(this).before(`<div class="mobile-menu__nav-wrapper">
									<div class="mobile-menu__nav-content"></div>
								</div>`);
			menu_nav_content = $(".mobile-menu__nav-content");
			$(this).appendTo($(this).prev().children().first());
		});

		// Добавление заголовка и кнопки назад в подменю
		menu_nav_content.each(function (){
			$(this).prepend(`<p class="mobile-menu__nav-title"></p>
								  <a href="#" class="mobile-menu__nav-back">Назад</a>`);
		});

		// Cоздание заголовков подкатегорий
		menu_nav.find("li.has-child").each(function (){			
			$(this).find("div > div > .mobile-menu__nav-title").html($(this).find("> a > span").html());
		});



		// ============== События для взаимодействия с меню ============== //

		// При клике на область пункта меню вне ссылки открыть подменю 
		menu_nav.find("li.has-child > a").click(function (e){
			if (!$(this).find("span").is(e.target) && $(this).find("span").has(e.target).length === 0){ 
            var menu_nav_item_wrap = $(this).parent().find("> .mobile-menu__nav-wrapper");

				// Активировать подменю
				menu_nav_item_wrap.addClass("active");

				// Анимация смещения 
			//	transform = transform + 40;
				$(".mobile-menu__wrapper").css("transform", "translate3d(" + transform + "px , 0, 0)");
				menu_nav_item_wrap.css("transform", "translate3d(-" + 0 + "px , 0, 0)");
				
				// Добавление Overlay
				$(".mobile-menu__wrapper").addClass("open");
				menu_nav_item_wrap.parents(".mobile-menu__nav-wrapper").addClass("open");	

				return false;
         }
		});
		menu_nav.find("li.has-child > #mobmenu").click(function (e){
			
            var menu_nav_item_wrap = $(this).parent().find("> .mobile-menu__nav-wrapper");

				// Активировать подменю
				menu_nav_item_wrap.addClass("active");

				// Анимация смещения 
			//	transform = transform + 40;
				$(".mobile-menu__wrapper").css("transform", "translate3d(" + transform + "px , 0, 0)");
				menu_nav_item_wrap.css("transform", "translate3d(-" + 0 + "px , 0, 0)");
				
				// Добавление Overlay
				$(".mobile-menu__wrapper").addClass("open");
				menu_nav_item_wrap.parents(".mobile-menu__nav-wrapper").addClass("open");	

				return false;
         
		});

		// При клике вне подменю закрыть текущее подменю
		$(document).mouseup(function (e){
			$(".mobile-menu__nav-wrapper.active").each(function() {
				if(!$(this).hasClass("open")){
					if (!$(this).is(e.target) && $(this).has(e.target).length === 0){
						
						// Закрыть подменю
						$(this).removeClass("active");
						$(this).parent().parent().parent().parent().removeClass("open");
						$(this).css("transform", "translate3d(-" + 100 + "% , 0, 0)");
					//	transform = transform - 40;
						
						$(".mobile-menu__wrapper").css("transform", "translate3d(" + transform + "px , 0, 0)");	
					}
				}
			});
		});

		// Закрыть текущее подменю при клике на кнопку назад
		$(".mobile-menu__nav-back").on("click", function (){
			var menu_nav_item_wrap = $(this).parent().parent();
			
			// Закрыть подменю 
			menu_nav_item_wrap.removeClass("active");	

			// Анимация смещения 
		//	transform = transform - 40;
			$(".mobile-menu__wrapper").css("transform", "translate3d(" + transform + "px , 0, 0)");
			menu_nav_item_wrap.css("transform", "translate3d(-" + 100 + "% , 0, 0)");

			// Удалить Overlay
			menu_nav_item_wrap.parent().parent().parent().parent().removeClass("open");

			if($(".mobile-menu__nav-wrapper").length == 0){		
				$(".mobile-menu__wrapper").removeClass("open");
			}	
		});

		// Закрыть мобильное меню при клике на overlay
		$(".mobile-menu__overlay").click(function (){
			$(".mobile-menu__nav-wrapper").removeClass("active").removeClass("open").css("transform", "translate3d(-100%, 0, 0)");
			transform = 0; 
			$(".mobile-menu__wrapper").removeClass("open").css("transform", "translate3d(" + transform + "px , 0, 0)");
		});

		// Добавить событие Открыть / Закрыть Меню , активируеться добавлением класса [.js__mobile-menu]
		$(".js__mobile-menu").click(function (){
			$("body").toggleClass("mobile-menu--active");

			return false;
		});
	}

	init_mobile_menu();	


	
	$(".mobile-menu").removeClass("mobile-menu--hide");
});