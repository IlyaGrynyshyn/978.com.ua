// var updateBtns = document.getElementsByClassName('update-cart')
//
// for (i = 0; i < updateBtns.length; i++) {
// 	updateBtns[i].addEventListener('click', function(){
// 		var productId = this.dataset.product
// 		var action = this.dataset.action
// 		console.log('productId:', productId, 'Action:', action)
// 		console.log('USER:', user)
//
// 		if (user == 'AnonymousUser'){
// 			addCookieItem(productId, action)
// 		}else{
// 			updateUserOrder(productId, action)
// 		}
// 	})
// }
//
// function updateUserOrder(productId, action){
// 	console.log('User is authenticated, sending data...')
//
// 		var url = '/update_item/'
//
// 		fetch(url, {
// 			method:'POST',
// 			headers:{
// 				'Content-Type':'application/json',
// 				'X-CSRFToken':csrftoken,
// 			},
// 			body:JSON.stringify({'productId':productId, 'action':action})
// 		})
// 		.then((response) => {
// 		   return response.json();
// 		})
// 		.then((data) => {
// 		    location.reload()
// 		});
// }
//
// function addCookieItem(productId, action){
// 	console.log('User is not authenticated')
//
// 	if (action === 'add'){
// 		if (cart[productId] === undefined){
// 		cart[productId] = {'quantity':1}
//
// 		}else{
// 			cart[productId]['quantity'] += 1
// 		}
// 	}
//
// 	if (action === 'remove'){
// 		cart[productId]['quantity'] -= 1
//
// 		if (cart[productId]['quantity'] <= 0){
// 			console.log('Item should be deleted')
// 			delete cart[productId];
// 		}
// 	}
// 	console.log('CART:', cart)
// 	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
//
// 	location.reload()
// }

//
//
// $(document).ready(function () {
//     $("#quantity-up").click(function () {
//         $.ajax({
//             url: $("quantity-up").data("url"),
//             type: "GET",
//             success: function (response) {
//                 $("cartDetail").append(' <div class="cart-row">\n' +
//                     '                            <div style="flex:2"><img class="row-image" src="'+ response.product.img.url +'" alt="No"></div>\n' +
//                     '                            <div style="flex:2"><p>'+ response.item.item.product.title +'</p></div>\n' +
//                     '                            <div style="flex:1"><p>$'+ response.item.item.price +'</p></div>\n' +
//                     '                            <div style="flex:1">\n' +
//                     '                                <p class="quantity">'+ response.item.item.quantity +'}}</p>\n' +
//                     '                                <div class="quantity" id="quantity">\n' +
//                     '                                    <img id="quantity-up" data-product="'+ response.item.item.product.id +'" data-action="add"\n' +
//                     '                                         class="chg-quantity update-cart" \n' +
//                     '                                         src="{% static  \'cart/images/arrow-up.png\' %}">\n' +
//                     '\n' +
//                     '\n' +
//                     '{#                                    <a href="{% url \'cart:subtraction_quantity\' product.id %}">#}\n' +
//                     '                                        <img data-product="{{ item.product.id }}" data-action="remove"\n' +
//                     '                                             class="chg-quantity update-cart"  data-url="{% url \'cart:subtraction_quantity\' product.id %}"\n' +
//                     '                                             src="{% static  \'cart/images/arrow-down.png\' %}">\n' +
//                     '                                    </a>\n' +
//                     '                                </div>\n' +
//                     '                            </div>\n' +
//                     '                            <div style="flex:1"><p>${{ item.total_price|floatformat:2 }}</p></div>\n' +
//                     '                            <a href="{% url "cart:cart_remove" product.id %}"\n' +
//                     '                               class=" btn-sm">X</a></td>\n' +
//                     '                        </div>')
//             }
//         })
//     })
// })
