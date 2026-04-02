
var isOpen, prevIsOpen, topNode;
setInterval(function() {
    prevIsOpen = isOpen;
    topNode = $('[data-outside-boundary-for="source-properties-editor"]')
    isOpen = topNode.length != 0;
    if (!prevIsOpen && isOpen) {
        console.log('opened')
        init()
    }
    if (prevIsOpen && !isOpen) {
        console.log('closed')
    }
}, 100)


function init() {
    topNode = $('[data-outside-boundary-for="source-properties-editor"]');

    data = {};
    tradingviewToAnywhere = {}

    prefix = topNode.find(`[data-section-name='Risk/RewardlongEntryPrice']`).length ? 'Risk/Rewardlong': 'Risk/Rewardshort'
    action = topNode.find(`[data-section-name='Risk/RewardlongEntryPrice']`).length ? 'Buy': 'Sell'
    topNode.find(`[data-section-name="${prefix}LotSize"], [data-section-name="${prefix}AccountSize"]`).remove()
    topNode.find('[data-section-name] input').attr('autocomplete', 'off')


    first = $('<span>')
    function createBtn(text) {
        return $('<button>', { class: "btn btn-outline-warning btn-sm", text: text}) //.append($('<i>', {class: 'bi bi-house'}))
    }

    $(`[data-section-name]`).first().before(first)
    first.before($('<div>', {text: action + ' (TP)', class: 'mb-2 mt-2'}), $('<div>', {class: 'mb-2 mt-2'}).append(
        $('<button>', { id: 'market_tp', class: "tta-tooltip btn btn-outline-info btn-sm", text: 'Market'}).addClass('me-3'),
        $('<button>', { id: 'limit_tp', class: "tta-tooltip btn btn-outline-info btn-sm", text: 'Limit'})
    ))
    first.before($('<div>', {text: action + ' (No-TP)', class: 'mb-2 mt-2'}), $('<div>', {class: 'mb-2 mt-2'}).append(
        $('<button>', { id: 'market_no_tp', class: "tta-tooltip btn btn-outline-secondary btn-sm", text: 'Market'}).addClass('me-3'),
        $('<button>', { id: 'limit_no_tp', class: "tta-tooltip btn btn-outline-secondary btn-sm", text: 'Limit'})
    ))

    $('.tta-tooltip').on('click', (event) => {navigator.clipboard.writeText($(event.target).attr('data-original-title'))})
    first.before($('<hr>'), $('<hr>'))
    first.remove()



    attrs = {
        AccountSize: prefix + "AccountSize",
        LotSize: prefix + "LotSize",
        Risk: prefix + "Risk",
        EntryPrice: prefix + "EntryPrice",
        ProfitLevel: prefix + "ProfitLevel",
        ProfitLevelTicks: prefix + "ProfitLevelTicks",
        ProfitLevelPrice: prefix + "ProfitLevelPrice",
        StopLevel: prefix + "StopLevel",
        StopLevelTicks: prefix + "StopLevelTicks",
        StopLevelPrice: prefix + "StopLevelPrice",
    }


		get_data()
		updateTTA();
		topNode.find('[data-section-name] input').on('change', updateTTA)
}

function get_data() {
    topNode.find('[data-section-name]').each(
        (_, el) => {
            el = $(el);
            data[el.attr('data-section-name')] = parseFloat(el.find('input').val())
    });
}

function updateTTA() {
    get_data()
    symbol = $('#header-toolbar-symbol-search .js-button-text').text()
    market_no_tp = `${action} ${symbol} SL=${data[attrs.StopLevelPrice]} Q=${data[attrs.Risk]}%`
    market_tp = `${action} ${symbol} SL=${data[attrs.StopLevelPrice]} TP=${data[attrs.ProfitLevelPrice]} Q=${data[attrs.Risk]}%`
    limit_no_tp = `${action} ${symbol} SL=${data[attrs.StopLevelPrice]} P=${data[attrs.EntryPrice]} Q=${data[attrs.Risk]}%`
    limit_tp = `${action} ${symbol} SL=${data[attrs.StopLevelPrice]} TP=${data[attrs.ProfitLevelPrice]} P=${data[attrs.EntryPrice]} Q=${data[attrs.Risk]}%`
    tradingviewToAnywhere = {
        market_no_tp: market_no_tp,
        market_tp: market_tp,
        limit_no_tp: limit_no_tp,
        limit_tp: limit_tp,
    }
    for (let key in tradingviewToAnywhere) {
        $(`#${key}`).attr('data-original-title', tradingviewToAnywhere[key]).tooltip()
    }
}

function addCssLink(href) {
  if ($(`link[href="${href}"]`).length === 0) {
    $('head').append($('<link>').attr('rel', 'stylesheet').attr('href', href));
  }
}

function addJsScript(src) {
  if ($(`script[src="${src}"]`).length === 0) {
    $('body').append($('<script>').attr('src', src).attr('type', 'text/javascript'));
  }
}

$(document).ready(function () {
  var customStyleId = 'styleID';
  if ($('#' + customStyleId).length === 0) {
    $('<style>').attr('id', customStyleId).appendTo('head')
      .text(`[data-name="source-properties-editor"] .btn:hover { color: white }`);
  }

  addCssLink('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css');
  addJsScript('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js');
});
