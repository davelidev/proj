// app.js — tabopener2 frontend
(function () {
'use strict';

var PALETTE = ['#ef4444','#f97316','#f59e0b','#eab308','#84cc16',
               '#22c55e','#10b981','#14b8a6','#06b6d4','#0ea5e9',
               '#3b82f6','#6366f1','#8b5cf6','#a855f7','#d946ef',
               '#ec4899','#f43f5e','#64748b','#6b7280','#78716c'];
var FALLBACK = ['#0d6efd','#dc3545','#198754','#fd7e14','#6f42c1','#d63384'];
var PROVIDER = {claude:'#fd7e14',opus:'#fd7e14',sonnet:'#fd7e14',haiku:'#fd7e14',
                gemini:'#8b5cf6',auto:'#8b5cf6',deepseek:'#0d6efd'};

var _tabs = [], _selectedIdx = -1, _filterText = '';
var _lastActiveFrontTty = null, _lastTitleChange = {};
var _isDragging = false, _dragSrcTty = null;
var _spawnAfterTty = null, _prevTtys = new Set();

// ── Storage ──────────────────────────────────────────────────────────────
function getColors() { try { return JSON.parse(localStorage.getItem('tabColors')||'{}'); } catch(e) { return {}; } }
function saveColors(c) { localStorage.setItem('tabColors', JSON.stringify(c)); }
function getOrder() { try { return JSON.parse(localStorage.getItem('tabOrder')||'[]'); } catch(e) { return []; } }
function saveOrder(o) { localStorage.setItem('tabOrder', JSON.stringify(o)); }

// ── Helpers ──────────────────────────────────────────────────────────────
function esc(s) { var d = document.createElement('div'); d.textContent = s||''; return d.innerHTML; }

function stableHash(str) {
  var h = 0;
  for (var i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) & 0xffff;
  return h;
}

function providerColor(model) {
  if (!model) return null;
  var m = model.toLowerCase();
  for (var k in PROVIDER) if (m.includes(k)) return PROVIDER[k];
  return null;
}

function barClass(pct) { return pct > 70 ? 'bg-red-500' : pct > 50 ? 'bg-amber-400' : 'bg-emerald-400'; }

function fmtResets(resetsAt) {
  if (!resetsAt) return '';
  var secs = Math.max(0, resetsAt - Date.now() / 1000);
  var h = Math.floor(secs / 3600);
  var m = Math.floor((secs % 3600) / 60);
  if (h > 0) return h + 'h' + (m > 0 ? ' ' + m + 'm' : '');
  return m > 0 ? m + 'm' : '<1m';
}

function barHtml(label, pct, resetsAt) {
  if (pct == null) return '';
  var resetStr = fmtResets(resetsAt);
  return (
    '<div class="flex flex-col gap-0.5">' +
      '<div class="flex items-center gap-1">' +
        '<span class="text-[10px] font-mono text-gray-400 whitespace-nowrap">' + esc(label) + '</span>' +
        '<div class="w-11 h-1.5 bg-gray-200 rounded-full overflow-hidden">' +
          '<div class="h-full rounded-full transition-all ' + barClass(pct) + '" style="width:' + pct + '%"></div>' +
        '</div>' +
        '<span class="text-[10px] font-mono text-gray-400">' + pct + '%</span>' +
      '</div>' +
      (resetStr ? '<span class="text-[9px] font-mono text-gray-400 leading-none text-center">' + resetStr + '</span>' : '') +
    '</div>'
  );
}

function visibleTabs() {
  if (!_filterText) return _tabs.slice();
  var q = _filterText;
  return _tabs.filter(function(t) {
    return (t.title||'').toLowerCase().includes(q) ||
           (t.cwd||'').toLowerCase().includes(q) ||
           (t.model||'').toLowerCase().includes(q);
  });
}

// ── API ──────────────────────────────────────────────────────────────────
function post(path, body) {
  fetch(path, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)}).catch(function(){});
}

// ── Palette popup ─────────────────────────────────────────────────────────
function showPalette(swatchEl, tty) {
  var old = document.querySelector('.palette-popup');
  if (old) old.remove();
  var cur = swatchEl.style.background;
  var popup = document.createElement('div');
  popup.className = 'palette-popup fixed z-50 bg-white rounded-xl shadow-2xl p-2 gap-1';
  PALETTE.forEach(function(hex) {
    var s = document.createElement('div');
    s.className = 'w-7 h-7 rounded-md cursor-pointer border-2 transition-all ' +
      (hex === cur ? 'border-blue-500 scale-110' : 'border-transparent hover:scale-110 hover:border-blue-400');
    s.style.background = hex;
    s.onclick = function() {
      var c = getColors(); c[tty] = hex; saveColors(c);
      swatchEl.style.background = hex; popup.remove();
    };
    popup.appendChild(s);
  });
  document.body.appendChild(popup);
  var r = swatchEl.getBoundingClientRect();
  popup.style.left = Math.min(r.left, window.innerWidth - popup.offsetWidth - 10) + 'px';
  popup.style.top = (r.bottom + 6) + 'px';
  setTimeout(function() {
    document.addEventListener('click', function close(e) {
      if (!e.target.closest('.palette-popup') && !e.target.closest('[data-action="color"]')) {
        popup.parentNode && popup.remove();
        document.removeEventListener('click', close);
      }
    });
  }, 10);
}

// ── Inline rename ─────────────────────────────────────────────────────────
function makeEditable(span, winId, tabId, tty) {
  span.contentEditable = true; span.focus();
  var r = document.createRange(); r.selectNodeContents(span);
  var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  span.onblur = function() {
    span.contentEditable = false;
    var t = span.textContent.trim();
    if (t) post('/api/rename', {winId:winId, tabId:tabId, title:t, tty:tty});
  };
  span.onkeydown = function(e) {
    if (e.key === 'Enter') { e.preventDefault(); span.blur(); }
    if (e.key === 'Escape') { span.contentEditable = false; }
  };
}

// ── Spawn ─────────────────────────────────────────────────────────────────
window.spawnTerminal = function() {
  var cwd = (document.getElementById('spawnCwd').value || '').trim();
  _spawnAfterTty = _lastActiveFrontTty;
  post('/api/spawn', {cwd:cwd});
};

window.spawnModel = function() {
  var sel = document.getElementById('modelSelect');
  var model = sel.value;
  var group = sel.options[sel.selectedIndex].parentNode.label || '';
  var cmd;
  if (model.startsWith('deepseek')) cmd = 'deepseek --model ' + model;
  else if (model.startsWith('gemini') || model === 'auto' || group === 'Gemini')
    cmd = 'gemini' + (model !== 'auto' ? ' --model ' + model : '');
  else cmd = 'claude --dangerously-skip-permissions --model ' + model;
  var cwd = (document.getElementById('spawnCwd').value || '').trim();
  _spawnAfterTty = _lastActiveFrontTty;
  post('/api/spawn', {cwd:cwd, cmd:cmd});
};

// ── Render ────────────────────────────────────────────────────────────────
function rowHtml(t, colorHex, isThinking, isFront, isSelected) {
  var mc = providerColor(t.model) || '#6b7280';
  var isGemini = (t.model||'').toLowerCase().includes('gemini') || t.model === 'auto';
  var isDeepseek = (t.model||'').toLowerCase().includes('deepseek');
  var statsHtml = barHtml(isGemini ? 'quota' : 'ctx', t.ctx_pct);
  if (!isDeepseek && !isGemini) statsHtml += barHtml('5h', t.rate_5h_pct, t.rate_5h_resets) + barHtml('7d', t.rate_7d_pct, t.rate_7d_resets);
  var hasBars = t.ctx_pct || t.rate_5h_pct || t.rate_7d_pct;
  var spinCls = isThinking ? ' animate-spin' : '';
  var pinBtn = t.manual
    ? '<span class="cursor-pointer text-blue-500 text-xs leading-none flex-shrink-0" data-action="unpin">⦿</span>'
    : '<span class="cursor-pointer opacity-30 hover:opacity-100 text-gray-400 hover:text-blue-500 text-xs leading-none flex-shrink-0' + spinCls + '" data-action="pin">↻</span>';
  var badge = t.model
    ? '<span class="text-[11px] font-mono px-1.5 py-0.5 rounded border font-medium flex-shrink-0 whitespace-nowrap" style="background:' + mc + '18;color:' + mc + ';border-color:' + mc + '44">' + esc(t.model) + '</span>'
    : '<span class="text-[11px] font-mono px-1.5 py-0.5 rounded border bg-gray-50 text-gray-400 border-gray-200 flex-shrink-0">—</span>';
  return (
    '<div class="flex items-center gap-2 min-w-0">' +
      '<span class="text-gray-400 opacity-25 hover:opacity-60 cursor-grab text-sm leading-none flex-shrink-0">⠿</span>' +
      '<div class="w-5 h-5 rounded-full flex-shrink-0 cursor-pointer border-2 border-transparent hover:border-blue-500 transition-all hover:scale-110" style="background:' + colorHex + '" data-action="color"></div>' +
      '<div class="flex-1 min-w-0 flex flex-col gap-0.5">' +
        '<div class="flex items-center gap-1 min-w-0">' +
          '<span class="truncate font-medium" data-action="edit" data-role="title">' + esc(t.title||'') + '</span>' +
          '<span class="cursor-pointer opacity-30 hover:opacity-100 text-gray-400 hover:text-blue-500 text-[11px] flex-shrink-0" data-action="edit">✎</span>' +
          pinBtn +
        '</div>' +
        '<div class="flex items-center gap-1.5 min-w-0">' +
          badge +
          (t.cwd ? '<span class="text-[11px] font-mono text-gray-400 truncate min-w-0">' + esc(t.cwd) + '</span>' : '') +
        '</div>' +
      '</div>' +
    '</div>' +
    (hasBars ? '<div class="flex items-start gap-5 pl-7 mt-1 flex-wrap">' + statsHtml + '</div>' : '')
  );
}

function attachEvents(row, t) {
  row.onclick = function(e) {
    if (e.target.closest('[data-action]')) return;
    post('/api/focus', {winId:t.winId});
  };
  row.addEventListener('click', function(e) {
    var el = e.target.closest('[data-action]');
    if (!el) return;
    e.stopPropagation();
    var a = el.dataset.action;
    if (a === 'color') showPalette(el, t.tty);
    else if (a === 'edit') makeEditable(row.querySelector('[data-role="title"]'), t.winId, t.tabId, t.tty);
    else if (a === 'pin') post('/api/title-mode', {tty:t.tty, mode:'manual', winId:t.winId, tabId:t.tabId, title:t.title});
    else if (a === 'unpin') post('/api/title-mode', {tty:t.tty, mode:'auto', winId:t.winId, tabId:t.tabId});
  });
  row.setAttribute('draggable', 'true');
  row.addEventListener('dragstart', onDragStart);
  row.addEventListener('dragover', onDragOver);
  row.addEventListener('drop', onDrop);
  row.addEventListener('dragend', onDragEnd);
}

function renderTabs(data) {
  if (_isDragging) return;
  _tabs = data;
  var now = Date.now();
  var colors = getColors();
  var list = document.getElementById('tabList');
  var vis = new Set(visibleTabs().map(function(t) { return t.tty; }));
  var allTtys = new Set(data.map(function(t) { return t.tty; }));

  var frontTty = null;
  for (var i = 0; i < data.length; i++) { if (data[i].frontWin && data[i].isActive) { frontTty = data[i].tty; break; } }
  if (!frontTty) frontTty = _lastActiveFrontTty;

  document.getElementById('tabCount').textContent = data.length;

  var prev = null;
  data.forEach(function(t, idx) {
    if (t.title !== _lastTitleChange['t_'+t.tty]) { _lastTitleChange['t_'+t.tty] = t.title; _lastTitleChange['ts_'+t.tty] = now; }
    var isThinking = (now - (_lastTitleChange['ts_'+t.tty]||0)) < 3000;
    var colorHex = colors[t.tty] || providerColor(t.model) || FALLBACK[stableHash(t.tty) % FALLBACK.length];
    var isFront = t.tty === frontTty;
    var isSelected = idx === _selectedIdx;
    var inner = rowHtml(t, colorHex, isThinking, isFront, isSelected);

    var row = list.querySelector('[data-tty="'+CSS.escape(t.tty)+'"]');
    if (!row) {
      row = document.createElement('div');
      row.className = 'tab-row bg-white border border-gray-200 rounded-lg px-3 py-2 cursor-pointer transition-all hover:border-blue-400 hover:shadow-md active:scale-[0.999]';
      row.dataset.tty = t.tty; row.dataset.winId = t.winId; row.dataset.tabId = t.tabId;
      list.appendChild(row);
    }
    row.classList.toggle('front', isFront);
    row.classList.toggle('selected', isSelected);
    row.style.display = _filterText && !vis.has(t.tty) ? 'none' : '';
    if (row.dataset.lastInner !== inner) { row.innerHTML = inner; row.dataset.lastInner = inner; attachEvents(row, t); }

    var expected = prev ? prev.nextSibling : list.firstChild;
    if (expected !== row) list.insertBefore(row, expected);
    prev = row;
  });

  Array.prototype.slice.call(list.children).forEach(function(r) {
    if (r.dataset.tty && !allTtys.has(r.dataset.tty)) r.remove();
  });
  _lastActiveFrontTty = frontTty;
}

// ── Drag-and-drop ─────────────────────────────────────────────────────────
function onDragStart(e) {
  _isDragging = true; _dragSrcTty = this.dataset.tty;
  this.classList.add('dragging'); e.dataTransfer.effectAllowed = 'move';
}
function onDragOver(e) {
  e.preventDefault(); e.dataTransfer.dropEffect = 'move';
  document.querySelectorAll('.drag-over').forEach(function(r) { r.classList.remove('drag-over'); });
  if (this.dataset.tty !== _dragSrcTty) this.classList.add('drag-over');
}
function onDrop(e) {
  e.preventDefault(); this.classList.remove('drag-over');
  var dst = this.dataset.tty;
  if (!dst || dst === _dragSrcTty) return;
  var si = _tabs.findIndex(function(t) { return t.tty === _dragSrcTty; });
  var di = _tabs.findIndex(function(t) { return t.tty === dst; });
  if (si < 0 || di < 0) return;
  var el = _tabs.splice(si, 1)[0];
  _tabs.splice(si < di ? di : di + 1, 0, el);
  var ttys = _tabs.map(function(t) { return t.tty; });
  saveOrder(ttys); post('/api/reorder', {ttyOrder:ttys}); renderTabs(_tabs);
}
function onDragEnd() {
  this.classList.remove('dragging');
  document.querySelectorAll('.drag-over').forEach(function(r) { r.classList.remove('drag-over'); });
  _isDragging = false; _dragSrcTty = null;
}

// ── Keyboard ──────────────────────────────────────────────────────────────
document.addEventListener('keydown', function(e) {
  var ae = document.activeElement;
  var editing = ae && (ae.tagName === 'INPUT' || ae.tagName === 'TEXTAREA' || ae.contentEditable === 'true');
  if (e.key === '/' && !editing) { e.preventDefault(); document.getElementById('filter').focus(); return; }
  if (e.key === 'Escape') {
    document.getElementById('filter').value = ''; _filterText = ''; _selectedIdx = -1;
    renderTabs(_tabs); document.getElementById('filter').blur(); return;
  }
  if (editing) return;
  var vis = visibleTabs();
  if (!vis.length) return;
  if (e.key === 'ArrowDown' || e.key === 'j') { e.preventDefault(); _selectedIdx = Math.min(_selectedIdx+1, vis.length-1); syncSelection(); }
  else if (e.key === 'ArrowUp' || e.key === 'k') { e.preventDefault(); _selectedIdx = Math.max(_selectedIdx-1, 0); syncSelection(); }
  else if (e.key === 'Tab' && !e.shiftKey) { e.preventDefault(); _selectedIdx = Math.min(_selectedIdx+1, vis.length-1); syncSelection(); }
  else if (e.key === 'Tab' && e.shiftKey) { e.preventDefault(); _selectedIdx = Math.max(_selectedIdx-1, 0); syncSelection(); }
  else if (e.key === 'Enter' && _selectedIdx >= 0 && vis[_selectedIdx]) { e.preventDefault(); post('/api/focus', {winId:vis[_selectedIdx].winId}); }
});

function syncSelection() {
  document.querySelectorAll('.tab-row').forEach(function(r) { r.classList.remove('selected'); });
  var vis = visibleTabs();
  if (_selectedIdx >= 0 && vis[_selectedIdx]) {
    var row = document.querySelector('[data-tty="'+CSS.escape(vis[_selectedIdx].tty)+'"]');
    if (row) { row.classList.add('selected'); row.scrollIntoView({block:'nearest'}); }
  }
}

// ── Spawn CWD persistence ─────────────────────────────────────────────────
(function() {
  var el = document.getElementById('spawnCwd');
  var saved = localStorage.getItem('spawnCwd');
  if (saved) el.value = saved;
  el.addEventListener('input', function() { localStorage.setItem('spawnCwd', this.value); });
})();

// ── Filter ────────────────────────────────────────────────────────────────
document.getElementById('filter').addEventListener('input', function() {
  _filterText = this.value.trim().toLowerCase(); _selectedIdx = -1; renderTabs(_tabs);
});

// ── SSE ───────────────────────────────────────────────────────────────────
var _backoff = 1000;
function connectSSE() {
  var es = new EventSource('/api/stream');
  es.onmessage = function(e) {
    _backoff = 1000;
    try {
      var data = JSON.parse(e.data);
      if (!Array.isArray(data)) return;
      if (_spawnAfterTty) {
        var newTtys = data.filter(function(t) { return !_prevTtys.has(t.tty); });
        if (newTtys.length) {
          var order = getOrder();
          if (!order.length) order = Array.prototype.slice.call(_prevTtys);
          var afterIdx = order.indexOf(_spawnAfterTty);
          newTtys.forEach(function(t, i) {
            afterIdx >= 0 ? order.splice(afterIdx + 1 + i, 0, t.tty) : order.push(t.tty);
          });
          saveOrder(order); post('/api/reorder', {ttyOrder: order});
          _spawnAfterTty = null;
        }
      }
      _prevTtys = new Set(data.map(function(t) { return t.tty; }));
      var order = getOrder();
      if (order.length) data.sort(function(a,b) {
        var ai = order.indexOf(a.tty), bi = order.indexOf(b.tty);
        return (ai>=0&&bi>=0)?ai-bi:(ai>=0)?-1:(bi>=0)?1:0;
      });
      renderTabs(data);
    } catch(err) { console.warn('SSE parse error', err); }
  };
  es.onerror = function() {
    es.close(); setTimeout(connectSSE, _backoff); _backoff = Math.min(_backoff*2, 30000);
  };
}
connectSSE();

})();
