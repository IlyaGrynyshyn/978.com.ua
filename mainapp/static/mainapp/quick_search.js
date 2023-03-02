// START LIVE search

const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultBox = document.getElementById('results-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (product) => {
    $.ajax({
        type: 'POST',
        url: '/search/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'product': product
        },
        success: (res) => {
            const data = res.data
            if (Array.isArray(data)) {
                resultBox.innerHTML = ""
                data.forEach(product => {
                    resultBox.innerHTML += `<ul class="b-hbs-search-quick-res-list">
    <li class="b-item"><a class="b-link" href='${product.url}'><span class="b-hbs-res-pic"><img src="${product.img}" alt="" width="55" height="55"></span><span class="b-hbs-res-desc"><span class="b-hbs-res-name">${product.title}</span><span class="b-hbs-res-price">${product.price} <i>грн</i></span></span></a></li>
</ul>
`
                })
            } else {
                if (searchInput.value.length > 0) {
                    resultBox.innerHTML = `<b>${data}</b>`
                } else {
                    resultBox.classList.add('not-visible')
                }
            }
        },
        error: (err) => {
            console.log(err)
        }
    })
}

searchInput.addEventListener('keyup', e => {

    if (resultBox.classList.contains('not-visible')) {
        resultBox.classList.remove('not-visible')
    }
    sendSearchData(e.target.value)
})

// END LIVE search