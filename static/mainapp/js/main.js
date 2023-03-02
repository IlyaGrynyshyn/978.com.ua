var price__slider = document.getElementById("filter-price__slider");
var price__min = document.getElementById("price-range-slider-input-1");
var price__max = document.getElementById("price-range-slider-input-2");
console.log(price__slider)
if (price__max != null) {
    noUiSlider.create(price__slider, {
        start: [30, 799],
        connect: true,
        direction: 'rtl',
        step: 1,
        range: {
            'min': [30],
            'max': [799]
        }
    });

}