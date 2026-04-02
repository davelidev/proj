#!/usr/bin/env python3
import http.server, socketserver, os, json, urllib.parse, subprocess, signal, time, fnmatch
import http.server, socketserver, os, json, urllib.parse, subprocess, signal, time, fnmatch

PORT = 8099

def kill_process_on_port(port):
    try:
        result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        pids = result.stdout.strip().split("\n")
        for pid in pids:
            if pid: os.kill(int(pid), signal.SIGKILL)
        time.sleep(0.5)
    except: pass

def get_ignore_patterns():
    patterns = {'.git', 'node_modules', '__pycache__'}
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.add(line.rstrip('/'))
    return patterns

def is_ignored(path, patterns):
    parts = path.split(os.sep)
    for part in parts:
        if part in patterns: return True
        for p in patterns:
            if fnmatch.fnmatch(part, p): return True
    return False

def get_ignore_patterns():
    patterns = {'.git', 'node_modules', '__pycache__'}
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.add(line.rstrip('/'))
    return patterns

def is_ignored(path, patterns):
    parts = path.split(os.sep)
    for part in parts:
        if part in patterns: return True
        for p in patterns:
            if fnmatch.fnmatch(part, p): return True
    return False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Markdown Studio V12 - Pro Split</title>
    <script src="https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/dist/markdown-it.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.5.1/github-markdown.min.css">
    <style>
        :root { 
            --bg: #ffffff; --sidebar-bg: #f6f8fa; --border: #d0d7de; --hover: #f3f4f6; 
            --text: #57606a; --file-text: #24292f; --active: #0969da; --md-bg: #ffffff;
            --active-bg: rgba(9, 105, 218, 0.1);
            --sidebar-width: 280px;
        }

        /* THEMES */
        body.v12-github-dark { --bg: #0d1117; --sidebar-bg: #010409; --border: #30363d; --hover: #21262d; --text: #8b949e; --file-text: #c9d1d9; --active: #58a6ff; --md-bg: #0d1117; }
        body.v12-onedark-dark { --bg: #282c34; --sidebar-bg: #21252b; --border: #181a1f; --hover: #2c313a; --text: #abb2bf; --file-text: #abb2bf; --active: #61afef; --md-bg: #282c34; }
        body.v12-dracula-dark { --bg: #282a36; --sidebar-bg: #21222c; --border: #44475a; --hover: #44475a; --text: #f8f8f2; --file-text: #f8f8f2; --active: #ff79c6; --md-bg: #282a36; }
        /* THEMES */
        body.v12-github-dark { --bg: #0d1117; --sidebar-bg: #010409; --border: #30363d; --hover: #21262d; --text: #8b949e; --file-text: #c9d1d9; --active: #58a6ff; --md-bg: #0d1117; }
        body.v12-onedark-dark { --bg: #282c34; --sidebar-bg: #21252b; --border: #181a1f; --hover: #2c313a; --text: #abb2bf; --file-text: #abb2bf; --active: #61afef; --md-bg: #282c34; }
        body.v12-dracula-dark { --bg: #282a36; --sidebar-bg: #21222c; --border: #44475a; --hover: #44475a; --text: #f8f8f2; --file-text: #f8f8f2; --active: #ff79c6; --md-bg: #282a36; }

        /* LIGHT THEMES */
        body.v12-github-light { --bg: #ffffff; --sidebar-bg: #f6f8fa; --border: #d0d7de; --hover: #f3f4f6; --text: #57606a; --file-text: #24292f; --active: #0969da; --md-bg: #ffffff; }
        body.v12-onedark-light { --bg: #fafafa; --sidebar-bg: #f0f0f0; --border: #eaeaea; --hover: #e5e5e5; --text: #383a42; --file-text: #202227; --active: #4078f2; --md-bg: #fafafa; }
        body.v12-dracula-light { --bg: #ffffff; --sidebar-bg: #f9f9f9; --border: #e1e4e8; --hover: #f1f8ff; --text: #44475a; --file-text: #44475a; --active: #ff79c6; --md-bg: #ffffff; }
        body.v12-github-light { --bg: #ffffff; --sidebar-bg: #f6f8fa; --border: #d0d7de; --hover: #f3f4f6; --text: #57606a; --file-text: #24292f; --active: #0969da; --md-bg: #ffffff; }
        body.v12-onedark-light { --bg: #fafafa; --sidebar-bg: #f0f0f0; --border: #eaeaea; --hover: #e5e5e5; --text: #383a42; --file-text: #202227; --active: #4078f2; --md-bg: #fafafa; }
        body.v12-dracula-light { --bg: #ffffff; --sidebar-bg: #f9f9f9; --border: #e1e4e8; --hover: #f1f8ff; --text: #44475a; --file-text: #44475a; --active: #ff79c6; --md-bg: #ffffff; }

        body { background-color: var(--bg); color: var(--file-text) !important; margin: 0; display: flex; font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; height: 100vh; overflow: hidden; transition: background 0.2s; }
        
        #sidebar { width: var(--sidebar-width); height: 100vh; background-color: var(--sidebar-bg); border-right: 1px solid var(--border); display: flex; flex-direction: column; flex-shrink: 0; transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1); position: relative; z-index: 100; }
        body.collapsed-nav #sidebar { margin-left: calc(-1 * var(--sidebar-width)); }
        
        #resizer { width: 4px; cursor: col-resize; background: transparent; transition: background 0.2s; z-index: 150; margin-left: -2px; margin-right: -2px; flex-shrink: 0; }
        #resizer:hover, #resizer.resizing { background: var(--active); }
        body.collapsed-nav #resizer { display: none; }

        #sidebar-header { padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); gap: 8px; }
        #sidebar-header span { font-size: 11px; font-weight: 700; color: var(--text) !important; text-transform: uppercase; letter-spacing: 1px; flex-grow: 1; }
        
        .header-btn { font-size: 10px; background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 4px; padding: 2px 6px; cursor: pointer; outline: none; transition: all 0.2s; }
        .header-btn:hover { background: var(--hover); border-color: var(--active); color: var(--active); }

        #nav-toggle { background: var(--sidebar-bg); border-right: 1px solid var(--border); padding: 0 12px; cursor: pointer; color: var(--text); display: flex; align-items: center; justify-content: center; transition: background 0.2s; flex-shrink: 0; height: 36px; }
        #nav-toggle:hover { background: var(--hover); }
        #nav-toggle svg { width: 14px; height: 14px; }
        #nav-toggle .icon-close { display: flex; }
        #nav-toggle .icon-menu { display: none; }
        body.collapsed-nav #nav-toggle .icon-close { display: none; }
        body.collapsed-nav #nav-toggle .icon-menu { display: flex; }

        #theme-select { font-size: 10px; background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 4px; padding: 2px 4px; outline: none; cursor: pointer; }
        
        #sidebar-content { flex-grow: 1; overflow-y: auto; padding: 10px 0; }
        .node { user-select: none; }
        .folder-header { padding: 6px 12px; cursor: pointer; display: flex; align-items: center; font-size: 13px; font-weight: 600; color: var(--text) !important; }
        .folder-header:hover { background-color: var(--hover); }
        .chevron { width: 14px; height: 14px; margin-right: 6px; transition: transform 0.15s ease; fill: currentColor; color: var(--text) !important; }
        .node.collapsed > .folder-header .chevron { transform: rotate(0deg); }
        .node:not(.collapsed) > .folder-header .chevron { transform: rotate(90deg); }
        .children { padding-left: 14px; }
        .node.collapsed > .children { display: none; }
        
        .file-item { padding: 6px 12px 6px 32px; cursor: pointer; font-size: 13px; color: var(--file-text) !important; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-decoration: none; border-left: 2px solid transparent; }
        .file-item:hover { background-color: var(--hover); color: var(--active) !important; }
        .file-item.active { background-color: var(--active-bg) !important; color: var(--active) !important; border-left: 2px solid var(--active); }

        #main { flex-grow: 1; height: 100vh; overflow: hidden; background-color: var(--md-bg); position: relative; display: flex; flex-direction: column; }
        
        #panes-container { display: flex; flex-grow: 1; overflow: hidden; position: relative; }
        
        .split-container { display: flex; flex-grow: 1; min-width: 0; min-height: 0; }
        .split-container.horizontal { flex-direction: row; }
        .split-container.vertical { flex-direction: column; }
        
        .pane-wrapper { flex: 1; display: flex; min-width: 0; min-height: 0; position: relative; }
        
        .pane { flex: 1; display: flex; flex-direction: column; min-width: 0; min-height: 0; position: relative; box-sizing: border-box; }
        .pane.active { z-index: 10; }

        .pane-resizer { flex-shrink: 0; z-index: 100; background: transparent; transition: background 0.2s; }
        .pane-resizer.horizontal { width: 4px; cursor: col-resize; margin: 0 -2px; }
        .pane-resizer.vertical { height: 4px; cursor: row-resize; margin: -2px 0; }
        .pane-resizer:hover, .pane-resizer.resizing { background: var(--active); }

        .tabs-header { display: flex; background: var(--sidebar-bg); border-bottom: 1px solid var(--border); align-items: center; flex-shrink: 0; height: 37px; transition: opacity 0.2s; }
        .pane:not(.active) .tabs-header { opacity: 0.5; }

        .tabs-bar { display: flex; background: var(--sidebar-bg); overflow-x: auto; overflow-y: hidden; flex-grow: 1; min-height: 36px; scrollbar-width: thin; }
        .tabs-bar::-webkit-scrollbar { height: 3px; }
        .tabs-bar::-webkit-scrollbar-thumb { background: transparent; border-radius: 10px; }
        .tabs-bar:hover::-webkit-scrollbar-thumb { background: var(--border); }
        
        .tab { display: flex; align-items: center; padding: 0 16px; height: 36px; font-size: 12px; color: var(--text); border-right: 1px solid var(--border); cursor: pointer; white-space: nowrap; transition: background 0.2s, color 0.2s; position: relative; user-select: none; box-sizing: border-box; }
        .tab:hover { background: var(--hover); }
        .tab.active { background: var(--bg); color: var(--active); border-bottom: 2px solid var(--active); }
        .pane:not(.active) .tab.active { color: var(--text); border-bottom-color: transparent; }
        
        .tab-close { margin-left: 10px; opacity: 0.5; font-size: 14px; width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; border-radius: 4px; }
        .tab-close:hover { opacity: 1; background: var(--hover); }

        .pane-content { flex-grow: 1; overflow-y: auto; padding: 0; position: relative; }
        .markdown-body { box-sizing: border-box; min-width: 200px; max-width: 900px; margin: 0 auto; padding: 50px; background-color: transparent !important; color: var(--file-text) !important; }
        
        .drop-zone { position: absolute; pointer-events: none; background: var(--active-bg); border: 2px dashed var(--active); z-index: 200; display: none; align-items: center; justify-content: center; color: var(--active); font-weight: bold; }
        .pane.drag-over-right > .drop-zone.right { display: flex; top: 0; right: 0; bottom: 0; width: 50%; border-left-width: 2px; }
        .pane.drag-over-bottom > .drop-zone.bottom { display: flex; left: 0; right: 0; bottom: 0; height: 50%; border-top-width: 2px; }
        .pane.drag-over-left > .drop-zone.left { display: flex; top: 0; left: 0; bottom: 0; width: 50%; border-right-width: 2px; }
        .pane.drag-over-top > .drop-zone.top { display: flex; left: 0; right: 0; top: 0; height: 50%; border-bottom-width: 2px; }

        .status-badge { position: fixed; bottom: 20px; right: 20px; font-size: 11px; color: var(--text); background: var(--sidebar-bg); padding: 6px 12px; border-radius: 20px; border: 1px solid var(--border); backdrop-filter: blur(4px); z-index: 1000; }
        .status-pulse { display: inline-block; width: 8px; height: 8px; background: #238636; border-radius: 50%; margin-right: 8px; }
        .syncing .status-pulse { animation: pulse 0.5s infinite; background: var(--active); }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.2); } 100% { transform: scale(1); } }
    </style>
</head>
<body class="v12-github-dark">
<body class="v12-github-dark">
    <div id="sidebar">
        <div id="sidebar-header">
            <span>Explorer</span>
            <span>Explorer</span>
            <select id="theme-select" class="header-btn" onchange="setTheme(this.value)">
                <optgroup label="GitHub"><option value="v12-github-light">GitHub Light</option><option value="v12-github-dark">GitHub Dark</option></optgroup>
                <optgroup label="One Dark Pro"><option value="v12-onedark-light">One Dark Light</option><option value="v12-onedark-dark" selected>One Dark Dark</option></optgroup>
                <optgroup label="Dracula"><option value="v12-dracula-light">Dracula Light</option><option value="v12-dracula-dark">Dracula Dark</option></optgroup>
            </select>
        </div>
        <div id="sidebar-content"></div>
    </div>
    <div id="resizer"></div>
    <div id="main">
        <div id="panes-container"></div>
        <div class="status-badge" id="status"><span class="status-pulse"></span>Studio Active</div>
    </div>
    <script>
        const md = window.markdownit({ 
            html: true, linkify: true, typographer: true,
            highlight: (str, lang) => {
                if (lang && hljs.getLanguage(lang)) {
                    try { return '<pre><code class="hljs">' + hljs.highlight(str, { language: lang }).value + '</code></pre>'; } catch (__) {}
                }
                return '<pre><code class="hljs">' + md.utils.escapeHtml(str) + '</code></pre>';
            }
        });

        let activePaneId = "pane-1";
        let dragSourcePaneId = null;
        let layout = JSON.parse(localStorage.getItem('studio_layout_v12') || '{"type":"pane","id":"pane-1"}');
        let paneFiles = JSON.parse(localStorage.getItem('studio_pane_files_v12') || '{"pane-1":[]}');
        let paneCurrent = JSON.parse(localStorage.getItem('studio_pane_current_v12') || '{"pane-1":""}');
        
        let dependencies = {}; 
        let paneMTimes = {};
        let collapsedFolders = new Set(JSON.parse(localStorage.getItem('studio_collapsed_v12') || '[]'));
        const CHEVRON = `<svg class="chevron" viewBox="0 0 20 20"><path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/></svg>`;

        function setTheme(theme) {
            document.body.className = theme;
            localStorage.setItem('studio_theme_v12', theme);
            localStorage.setItem('studio_theme_v12', theme);
            const isDark = theme.includes('dark');
            const hlLink = document.querySelector('link[href*="highlight.js"]');
            if (hlLink) {
                hlLink.href = isDark 
                    ? "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css"
                    : "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css";
            }
        }

        function toggleSidebar() {
            const isCollapsed = document.body.classList.toggle('collapsed-nav');
            const isCollapsed = document.body.classList.toggle('collapsed-nav');
            localStorage.setItem('studio_nav_collapsed', isCollapsed);
        }

        function activatePane(paneId) {
            activePaneId = paneId;
            document.querySelectorAll('.pane').forEach(p => p.classList.toggle('active', p.id === paneId));
            updateSidebarHighlights();
        }

        function sanitizeLayout(node) {
            if (node.type === 'split') {
                node.children = node.children.map(child => sanitizeLayout(child)).filter(Boolean);
                if (node.children.length === 0) return null;
                if (node.children.length === 1) {
                    const child = node.children[0];
                    if (node.size) child.size = node.size;
                    return child;
                }
                return node;
            } else {
                const hasCurrent = paneCurrent[node.id];
                const hasPinned = (paneFiles[node.id] || []).length > 0;
                if (!hasCurrent && !hasPinned && node.id !== 'pane-1') return null;
                return node;
            }
        }

        async function init() {
            const savedTheme = localStorage.getItem('studio_theme_v12') || 'v12-github-dark';
            document.getElementById('theme-select').value = savedTheme; setTheme(savedTheme);
            if (localStorage.getItem('studio_nav_collapsed') === 'true') document.body.classList.add('collapsed-nav');
            const savedWidth = localStorage.getItem('studio_sidebar_width_v12') || '280px';
            document.documentElement.style.setProperty('--sidebar-width', savedWidth);
            initResizer();
            await fetchFiles();
            layout = sanitizeLayout(layout) || {"type":"pane","id":"pane-1"};
            renderLayout();
            setInterval(watch, 500);
            setInterval(fetchFiles, 5000);
        }

        function renderLayout() {
            const container = document.getElementById('panes-container');
            container.innerHTML = recursiveRender(layout, "root");
            const allPanes = findAllPanes(layout);
            allPanes.forEach(paneId => {
                const paneNum = paneId.replace('pane-', '');
                renderTabs(paneId);
                if (paneCurrent[paneId]) updateContent(paneCurrent[paneId], `content-${paneNum}`, paneId);
            });
            initPaneResizers();
            activatePane(activePaneId);
            saveState();

            function recursiveRender(node, path) {
                if (node.type === 'pane') {
                    const paneNum = node.id.replace('pane-', '');
                    const isFirst = node.id === 'pane-1';
                    return `<div id="${node.id}" class="pane" data-node-path="${path}" onclick="activatePane('${node.id}')" ondragover="handleDragOver(event, '${node.id}')" ondragleave="handleDragLeave(event, '${node.id}')" ondrop="handleDrop(event, '${node.id}')">
                        <div class="tabs-header">
                            ${isFirst ? `
                            <div id="nav-toggle" onclick="toggleSidebar()" title="Toggle Sidebar">
                                <svg class="icon-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
                                <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                            </div>` : ''}
                            <div id="tabs-${paneNum}" class="tabs-bar"></div>
                        </div>
                        <div class="pane-content"><article id="content-${paneNum}" class="markdown-body"></article></div>
                        <div class="drop-zone top">Split Top</div><div class="drop-zone bottom">Split Bottom</div>
                        <div class="drop-zone left">Split Left</div><div class="drop-zone right">Split Right</div>
                    </div>`;
                } else {
                    let html = `<div class="split-container ${node.direction}" data-node-path="${path}">`;
                    for (let i = 0; i < node.children.length; i++) {
                        const childPath = `${path}.children[${i}]`;
                        const child = node.children[i];
                        const size = child.size || 1;
                        html += `<div class="pane-wrapper" style="flex: ${size} 1 0%" data-node-path="${childPath}">
                            ${recursiveRender(child, childPath)}
                        </div>`;
                        if (i < node.children.length - 1) {
                            html += `<div class="pane-resizer ${node.direction}" data-parent-path="${path}" data-left-idx="${i}"></div>`;
                        }
                    }
                    html += `</div>`;
                    return html;
                }
            }
        }

        function initPaneResizers() {
            document.querySelectorAll('.pane-resizer').forEach(resizer => {
                resizer.addEventListener('mousedown', (e) => {
                    e.preventDefault();
                    const direction = resizer.classList.contains('horizontal') ? 'horizontal' : 'vertical';
                    const parentPath = resizer.getAttribute('data-parent-path');
                    const leftIdx = parseInt(resizer.getAttribute('data-left-idx'));
                    const prevWrapper = resizer.previousElementSibling;
                    const nextWrapper = resizer.nextElementSibling;
                    const startPos = direction === 'horizontal' ? e.clientX : e.clientY;
                    const prevStartSize = direction === 'horizontal' ? prevWrapper.offsetWidth : prevWrapper.offsetHeight;
                    const nextStartSize = direction === 'horizontal' ? nextWrapper.offsetWidth : nextWrapper.offsetHeight;
                    const combinedFlex = parseFloat(prevWrapper.style.flexGrow) + parseFloat(nextWrapper.style.flexGrow);
                    resizer.classList.add('resizing');
                    document.body.style.cursor = direction === 'horizontal' ? 'col-resize' : 'row-resize';
                    const onMouseMove = (moveEvent) => {
                        const currentPos = direction === 'horizontal' ? moveEvent.clientX : moveEvent.clientY;
                        const delta = currentPos - startPos;
                        const newPrevSize = Math.max(50, prevStartSize + delta);
                        const newNextSize = Math.max(50, nextStartSize - delta);
                        const totalSize = newPrevSize + newNextSize;
                        const prevFlex = (newPrevSize / totalSize) * combinedFlex;
                        const nextFlex = (newNextSize / totalSize) * combinedFlex;
                        prevWrapper.style.flexGrow = prevFlex;
                        nextWrapper.style.flexGrow = nextFlex;
                        const parentNode = getObjectByPath(layout, parentPath);
                        parentNode.children[leftIdx].size = prevFlex;
                        parentNode.children[leftIdx+1].size = nextFlex;
                    };
                    const onMouseUp = () => {
                        resizer.classList.remove('resizing');
                        document.body.style.cursor = '';
                        window.removeEventListener('mousemove', onMouseMove);
                        window.removeEventListener('mouseup', onMouseUp);
                        saveState();
                    };
                    window.addEventListener('mousemove', onMouseMove);
                    window.addEventListener('mouseup', onMouseUp);
                });
            });
        }

        function getObjectByPath(obj, path) {
            if (path === "root") return obj;
            return path.split('.').slice(1).reduce((acc, part) => {
                const match = part.match(/(\w+)\[(\d+)\]/);
                if (match) return acc[match[1]][parseInt(match[2])];
                return acc[part];
            }, obj);
        }

        function findAllPanes(node) {
            if (node.type === 'pane') return [node.id];
            return node.children.reduce((acc, child) => acc.concat(findAllPanes(child)), []);
        }

        function handleDragOver(e, paneId) {
            e.preventDefault();
            const el = document.getElementById(paneId);
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            el.classList.remove('drag-over-right', 'drag-over-bottom', 'drag-over-left', 'drag-over-top');
            if (dragSourcePaneId === paneId && (paneFiles[paneId] || []).length < 2) return;
            if (x > rect.width * 0.8) el.classList.add('drag-over-right');
            else if (x < rect.width * 0.2) el.classList.add('drag-over-left');
            else if (y > rect.height * 0.8) el.classList.add('drag-over-bottom');
            else if (y < rect.height * 0.2) el.classList.add('drag-over-top');
        }

        function handleDragLeave(e, paneId) {
            document.getElementById(paneId).classList.remove('drag-over-right', 'drag-over-bottom', 'drag-over-left', 'drag-over-top');
        }

        function handleDrop(e, paneId) {
            e.preventDefault();
            const el = document.getElementById(paneId);
            const file = e.dataTransfer.getData('text/plain');
            const sourcePaneId = e.dataTransfer.getData('source-pane');
            const isRight = el.classList.contains('drag-over-right');
            const isBottom = el.classList.contains('drag-over-bottom');
            const isLeft = el.classList.contains('drag-over-left');
            const isTop = el.classList.contains('drag-over-top');
            el.classList.remove('drag-over-right', 'drag-over-bottom', 'drag-over-left', 'drag-over-top');
            if (file) {
                if (isRight || isBottom || isLeft || isTop) {
                    if (sourcePaneId === paneId && (paneFiles[paneId]||[]).length < 2) {
                        loadFile(file, paneId, true); return;
                    }
                    const newPaneId = "pane-" + Date.now();
                    paneFiles[newPaneId] = [file]; paneCurrent[newPaneId] = file;
                    if (sourcePaneId) {
                        paneFiles[sourcePaneId] = paneFiles[sourcePaneId].filter(f => f !== file);
                        if (paneCurrent[sourcePaneId] === file) paneCurrent[sourcePaneId] = paneFiles[sourcePaneId][paneFiles[sourcePaneId].length-1] || "";
                        if ((paneFiles[sourcePaneId] || []).length === 0 && sourcePaneId !== 'pane-1') {
                            removePane(layout, sourcePaneId);
                            if (activePaneId === sourcePaneId) activePaneId = 'pane-1';
                        }
                    }
                    splitPane(layout, paneId, newPaneId, (isRight || isLeft) ? 'horizontal' : 'vertical', (isLeft || isTop));
                    renderLayout();
                } else {
                    loadFile(file, paneId, true);
                }
            }
            dragSourcePaneId = null;
        }

        function splitPane(root, targetId, newPaneId, direction, prepend) {
            const findParent = (node) => {
                if (node.type === 'split') {
                    const idx = node.children.findIndex(c => c.type === 'pane' && c.id === targetId);
                    if (idx !== -1 && node.direction === direction) {
                        const newNode = {type: 'pane', id: newPaneId, size: 1};
                        node.children.splice(prepend ? idx : idx + 1, 0, newNode); return true;
                    }
                    for (let child of node.children) if (findParent(child)) return true;
                }
                return false;
            };
            if (findParent(root)) return true;
            const wrapNode = (node) => {
                if (node.type === 'pane' && node.id === targetId) {
                    const oldNode = {...node}; const newNode = {type: 'pane', id: newPaneId, size: 1};
                    oldNode.size = 1; node.type = 'split'; node.direction = direction;
                    node.children = prepend ? [newNode, oldNode] : [oldNode, newNode];
                    delete node.id; return true;
                }
                if (node.type === 'split') { for (let child of node.children) if (wrapNode(child)) return true; }
                return false;
            };
            return wrapNode(root);
        }

        function initResizer() {
            const resizer = document.getElementById('resizer');
            let isResizing = false;
            resizer.addEventListener('mousedown', () => { isResizing = true; resizer.classList.add('resizing'); document.body.style.cursor = 'col-resize'; document.body.style.userSelect = 'none'; });
            document.addEventListener('mousemove', (e) => { if (!isResizing) return; const width = Math.max(150, Math.min(600, e.clientX)) + 'px'; document.documentElement.style.setProperty('--sidebar-width', width); localStorage.setItem('studio_sidebar_width_v12', width); });
            document.addEventListener('mouseup', () => { if (!isResizing) return; isResizing = false; resizer.classList.remove('resizing'); document.body.style.cursor = ''; document.body.style.userSelect = ''; });
        }

        function saveState() {
            localStorage.setItem('studio_layout_v12', JSON.stringify(layout));
            localStorage.setItem('studio_pane_files_v12', JSON.stringify(paneFiles));
            localStorage.setItem('studio_pane_current_v12', JSON.stringify(paneCurrent));
        }

        async function fetchFiles() {
            const res = await fetch('/files');
            const files = await res.json();
            const tree = { dirs: {}, files: [] };
            files.forEach(f => {
                const parts = f.split('/'); let curr = tree;
                for (let i = 0; i < parts.length - 1; i++) {
                    const dir = parts[i];
                    if (!curr.dirs[dir]) curr.dirs[dir] = { dirs: {}, files: [], path: parts.slice(0, i+1).join('/') };
                    curr = curr.dirs[dir];
                }
                curr.files.push({ name: parts[parts.length-1], path: f });
            });
            document.getElementById('sidebar-content').innerHTML = renderSidebarNode(tree);
        }

        function renderSidebarNode(node) {
            let html = '';
            Object.entries(node.dirs).sort().forEach(([name, dir]) => {
                const isCollapsed = collapsedFolders.has(dir.path) ? 'collapsed' : '';
                html += `<div class="node ${isCollapsed}" data-path="${dir.path}">
                    <div class="folder-header" onclick="toggleFolder('${dir.path}')">${CHEVRON} ${name}</div>
                    <div class="children">${renderSidebarNode(dir)}</div>
                </div>`;
            });
            node.files.sort((a,b) => a.name.localeCompare(b.name)).forEach(f => {
                const active = (f.path === paneCurrent[activePaneId]) ? 'active' : '';
                html += `<a class="file-item ${active}" data-path="${f.path}" draggable="true" ondragstart="event.dataTransfer.setData('text/plain', '${f.path}'); dragSourcePaneId = null;" ondragend="dragSourcePaneId = null;" onclick="loadFile('${f.path}', null, false, event)" ondblclick="loadFile('${f.path}', null, true, event)">${f.name}</a>`;
            });
            return html;
        }

        function toggleFolder(path) {
            const el = document.querySelector(`[data-path="${path}"]`);
            if (el.classList.toggle('collapsed')) collapsedFolders.add(path);
            else collapsedFolders.delete(path);
            localStorage.setItem('studio_collapsed_v12', JSON.stringify(Array.from(collapsedFolders)));
            localStorage.setItem('studio_collapsed_v12', JSON.stringify(Array.from(collapsedFolders)));
        }

        function renderTabs() {
            const tabsBar = document.getElementById('tabs-bar');
            tabsBar.innerHTML = openFiles.map(file => {
                const name = file.split('/').pop();
                const active = file === currentFile ? 'active' : '';
                return `<div class="tab ${active}" onclick="loadFile('${file}')">
                    ${name}
                    <span class="tab-close" onclick="closeTab('${file}', event)">×</span>
                </div>`;
            }).join('');
            localStorage.setItem('studio_open_files_v12', JSON.stringify(openFiles));
        }

        function closeTab(file, event) {
            event.stopPropagation();
            openFiles = openFiles.filter(f => f !== file);
            if (currentFile === file) {
                if (openFiles.length > 0) loadFile(openFiles[openFiles.length - 1]);
                else {
                    currentFile = "";
                    document.getElementById('content').innerHTML = "";
                    const url = new URL(window.location); url.searchParams.delete('file'); window.history.pushState({}, '', url);
                }
            }
            renderTabs();
        }

        function renderTabs(paneId) {
            const paneNum = paneId.replace('pane-', '');
            const tabsBar = document.getElementById(`tabs-${paneNum}`);
            if (!tabsBar) return;
            tabsBar.innerHTML = (paneFiles[paneId] || []).map(file => {
                const name = file.split('/').pop();
                const active = file === paneCurrent[paneId] ? 'active' : '';
                return `<div class="tab ${active}" draggable="true" ondragstart="event.dataTransfer.setData('text/plain', '${file}'); event.dataTransfer.setData('source-pane', '${paneId}'); dragSourcePaneId = '${paneId}';" ondragend="dragSourcePaneId = null;" onauxclick="if(event.button===1) closeTab('${file}', '${paneId}', event)" onclick="loadFile('${file}', '${paneId}', true, event)">
                    ${name}<span class="tab-close" onclick="closeTab('${file}', '${paneId}', event)">×</span>
                </div>`;
            }).join('');
        }

        function closeTab(file, paneId, event) {
            if (event) event.stopPropagation();
            paneFiles[paneId] = (paneFiles[paneId] || []).filter(f => f !== file);
            if (paneCurrent[paneId] === file) paneCurrent[paneId] = (paneFiles[paneId] || [])[(paneFiles[paneId] || []).length - 1] || "";
            if ((paneFiles[paneId] || []).length === 0 && paneId !== 'pane-1') {
                removePane(layout, paneId); renderLayout();
            } else {
                renderTabs(paneId); updateContent(paneCurrent[paneId], `content-${paneId.replace('pane-', '')}`, paneId);
            }
            saveState();
        }

        function removePane(node, paneId) {
            if (node.type === 'split') {
                const index = node.children.findIndex(child => child.type === 'pane' && child.id === paneId);
                if (index !== -1) {
                    const otherChild = node.children[1 - index];
                    Object.assign(node, otherChild); return true;
                }
                for (let child of node.children) if (removePane(child, paneId)) return true;
            }
            return false;
        }

        function loadFile(file, paneId, isPermanent, event) {
            if (event) event.stopPropagation();
            const targetPane = paneId || activePaneId;
            activatePane(targetPane);
            if (!paneFiles[targetPane]) paneFiles[targetPane] = [];
            if (isPermanent && !paneFiles[targetPane].includes(file)) paneFiles[targetPane].push(file);
            paneCurrent[targetPane] = file;
            updateSidebarHighlights(); renderTabs(targetPane);
            updateContent(file, `content-${targetPane.replace('pane-', '')}`, targetPane);
            saveState();
        }

        function updateSidebarHighlights() {
            document.querySelectorAll('.file-item').forEach(el => {
                const path = el.getAttribute('data-path');
                el.classList.toggle('active', path === paneCurrent[activePaneId]);
            });
        }

        async function getMTime(file) {
            const res = await fetch(`/mtime?file=${encodeURIComponent(file)}`);
            return res.ok ? await res.text() : null;
        }

        async function watch() {
            const allPanes = findAllPanes(layout);
            for (let paneId of allPanes) {
                const file = paneCurrent[paneId]; if (!file) continue;
                const t = await getMTime(file);
                if (t !== paneMTimes[paneId]) updateContent(file, `content-${paneId.replace('pane-', '')}`, paneId);
            }
            for (const path in dependencies) {
                const newMTime = await getMTime(path);
                if (newMTime !== dependencies[path]) {
                    allPanes.forEach(paneId => { if (paneCurrent[paneId]) updateContent(paneCurrent[paneId], `content-${paneId.replace('pane-', '')}`, paneId); });
                    return;
                }
            }
        }

        async function updateContent(file, targetId, paneKey) {
            const el = document.getElementById(targetId);
            if (!el) return;
            if (!file) { el.innerHTML = ""; return; }
            const status = document.getElementById('status');
            status.classList.add('syncing');
            try {
                const res = await fetch(`/content?file=${encodeURIComponent(file)}&t=${Date.now()}`);
                paneMTimes[paneKey] = res.headers.get('X-File-MTime');
                let text = await res.text();
                const regex = /```(\\w+)\\s*\\{\\{(.+?)\\}\\}\\s*```/g;
                let match;
                const newDeps = {}; const replacements = [];
                while ((match = regex.exec(text)) !== null) {
                    const [full, lang, path] = match;
                    const cleanPath = path.trim();
                    const fileRes = await fetch(`/read?file=${encodeURIComponent(cleanPath)}`);
                    const content = fileRes.ok ? await fileRes.text() : `// Error: Could not read ${cleanPath}`;
                    newDeps[cleanPath] = fileRes.headers.get('X-File-MTime');
                    replacements.push({ full, lang, content });
                }
                dependencies = {...dependencies, ...newDeps};
                for (const r of replacements) text = text.replace(r.full, "```" + r.lang + "\\n" + r.content + "\\n```");
                el.innerHTML = md.render(text);
            } catch (e) {}
            setTimeout(() => status.classList.remove('syncing'), 300);
            setTimeout(() => status.classList.remove('syncing'), 300);
        }
        window.onload = init;
    </script>
</body>
</html>
"""

class ReusableTCPServer(socketserver.TCPServer): allow_reuse_address = True

class MarkdownHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args): pass

    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
        if u.path == '/':
            self.send_response(200); self.send_header('Content-type', 'text/html'); self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        elif u.path == '/files':
            ignore_patterns = get_ignore_patterns()
            ignore_patterns = get_ignore_patterns()
            files = []
            for root, dirs, fnames in os.walk('.'):
                rel_root = os.path.relpath(root, '.')
                if rel_root != '.' and is_ignored(rel_root, ignore_patterns):
                    dirs[:] = []
                    continue
                rel_root = os.path.relpath(root, '.')
                if rel_root != '.' and is_ignored(rel_root, ignore_patterns):
                    dirs[:] = []
                    continue
                for f in fnames:
                    if f.endswith('.md'):
                        rel_path = os.path.relpath(os.path.join(root, f), '.')
                        if not is_ignored(rel_path, ignore_patterns): files.append(rel_path)
            self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps(sorted(files)).encode())
        elif u.path == '/content' or u.path == '/read':
                    if f.endswith('.md'):
                        rel_path = os.path.relpath(os.path.join(root, f), '.')
                        if not is_ignored(rel_path, ignore_patterns): files.append(rel_path)
            self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps(sorted(files)).encode())
        elif u.path == '/content' or u.path == '/read':
            fname = q.get('file', [""])[0]
            if os.path.exists(fname):
                self.send_response(200); self.send_header('X-File-MTime', str(os.path.getmtime(fname))); self.end_headers()
                self.send_response(200); self.send_header('X-File-MTime', str(os.path.getmtime(fname))); self.end_headers()
                with open(fname, 'rb') as f: self.wfile.write(f.read())
            else: self.send_error(404)
        elif u.path == '/mtime':
            fname = q.get('file', [""])[0]
            if os.path.exists(fname):
                self.send_response(200); self.send_header('Content-type', 'text/plain'); self.end_headers()
                self.wfile.write(str(os.path.getmtime(fname)).encode())
            else: self.send_error(404)
        elif u.path == '/mtime':
            fname = q.get('file', [""])[0]
            if os.path.exists(fname):
                self.send_response(200); self.send_header('Content-type', 'text/plain'); self.end_headers()
                self.wfile.write(str(os.path.getmtime(fname)).encode())
            else: self.send_error(404)
        else: super().do_GET()

if __name__ == '__main__':
    kill_process_on_port(PORT)
    print(f"\\n🚀 Markdown Studio V12 Active: http://localhost:{PORT}\\n")
    with ReusableTCPServer(("", PORT), MarkdownHandler) as httpd:
        httpd.serve_forever()
