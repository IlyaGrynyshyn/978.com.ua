$(document).ready(function(){
   $('.justselect').each(function(){
      $(this).wrap('<div class="justselect-wrapper">');
   
      var justselectUL = document.createElement( "ul" );
         justselectUL.className = "justselect-list";
         
      var justselectTitle = document.createElement( "div" );   
         justselectTitle.className = "justselect-title";
         
      var   select = $(this).parent(),
         option = $(this).find($('option'));
		
         
         select.append(justselectTitle, justselectUL);      
         
         for (i = 0; i< option.length; i++) {
            var justselectLI = document.createElement( "li" );
                justselectUL.append(justselectLI),
                justselectLI_option = select.find($('.justselect-list li'));
                
                justselectLI_option.eq(i).text(option.eq(i).text());
				justselectLI_option.eq(i).attr("onClick", "location.href='" + option.eq(i).val() + "'");
				
                
                if (option.eq(i).attr('selected')) {
                   justselectLI_option.eq(i).addClass('selected');
                   select.find($('.justselect-title')).text(justselectLI_option.eq(i).text());
                }
                
                justselectLI_option.click(function(){
                   $(this).addClass('selected').siblings().removeAttr('class');
                   var index = $(this).index();
                   
                   select.find($('.justselect-list')).fadeOut();
                   $('.justselect-body-overlay').remove();  
                   
                   option.eq(index).attr("selected", true).siblings().removeAttr("selected");
                   select.find($('.justselect-title')).text($(this).text());
                });            
         }
		
          
      select.find($('.justselect-title')).click(function(){
         select.find($('.justselect-list')).fadeToggle(); 
      });         

      $(document).mouseup(function (e){     
         if (!select.is(e.target) && select.has(e.target).length === 0){ 
            select.find($('.justselect-list')).fadeOut();
         }
      });
   });   
});

