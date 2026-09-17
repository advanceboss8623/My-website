* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #fff;
    color: #202124;
    transition: background 0.2s, color 0.2s;
}

/* Browser */

.browser {
    width: 100%;
    background: #dee1e6;
}

/* Tabs */

.tabs {
    height: 40px;
    display: flex;
    align-items: flex-end;
    padding-left: 8px;
    gap: 5px;
}

.tab {
    height: 34px;
    width: 230px;
    background: #f1f3f4;
    border-radius: 10px 10px 0 0;
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 10px;
    font-size: 14px;
}

.tab.active {
    background: #fff;
}

.tab-icon {
    font-size: 13px;
}

.tab span {
    flex: 1;
}

.close-tab {
    border: none;
    background: transparent;
    font-size: 18px;
    cursor: pointer;
    border-radius: 50%;
}

.close-tab:hover {
    background: #ddd;
}

.new-tab {
    border: none;
    background: transparent;
    font-size: 25px;
    width: 35px;
    height: 34px;
    cursor: pointer;
    border-radius: 50%;
}

.new-tab:hover {
    background: #c8ccd1;
}

/* Toolbar */

.toolbar {
    height: 52px;
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 6px 10px;
}

.nav-button,
.menu-button {
    border: none;
    background: transparent;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    font-size: 22px;
    cursor: pointer;
}

.nav-button:hover,
.menu-button:hover {
    background: #c8ccd1;
}

/* Address bar */

.address-form {
    flex: 1;
    height: 38px;
    background: #f1f3f4;
    border-radius: 22px;
    display: flex;
    align-items: center;
    padding: 0 14px;
}

.lock {
    font-size: 20px;
    margin-right: 8px;
}

.address-form input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    font-size: 15px;
}

.star {
    border: none;
    background: transparent;
    font-size: 22px;
    cursor: pointer;
}

/* Menu */

.menu {
    display: none;
    position: absolute;
    right: 15px;
    top: 90px;
    background: white;
    width: 180px;
    border-radius: 10px;
    padding: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    z-index: 10;
}

.menu.show {
    display: block;
}

.menu button {
    width: 100%;
    padding: 12px;
    border: none;
    background: transparent;
    text-align: left;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
}

.menu button:hover {
    background: #f1f3f4;
}

/* New Tab */

.new-tab-page {
    min-height: calc(100vh - 92px);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 100px;
}

.google-logo {
    font-size: 82px;
    font-weight: 500;
    letter-spacing: -5px;
    margin-bottom: 30px;
}

.blue {
    color: #4285f4;
}

.red {
    color: #ea4335;
}

.yellow {
    color: #fbbc05;
}

.green {
    color: #34a853;
}

/* Google search */

.google-search {
    width: min(600px, 90%);
    height: 50px;
    border: 1px solid #dfe1e5;
    border-radius: 25px;
    display: flex;
    align-items: center;
    padding: 0 15px;
    box-shadow: 0 1px 6px rgba(32,33,36,0.15);
}

.google-search:focus-within {
    box-shadow: 0 1px 8px rgba(32,33,36,0.25);
}

.search-icon {
    font-size: 22px;
    margin-right: 10px;
}

.google-search input {
    flex: 1;
    height: 100%;
    border: none;
    outline: none;
    font-size: 16px;
}

.mic {
    border: none;
    background: transparent;
    cursor: pointer;
    font-size: 18px;
}

.search-button {
    margin-left: 10px;
    border: none;
    background: #f8f9fa;
    padding: 9px 15px;
    border-radius: 5px;
    cursor: pointer;
}

.search-button:hover {
    background: #e8eaed;
}

/* Shortcuts */

.shortcuts {
    display: flex;
    gap: 20px;
    margin-top: 45px;
    flex-wrap: wrap;
    justify-content: center;
}

.shortcut {
    width: 100px;
    height: 100px;
    border: none;
    background: transparent;
    border-radius: 10px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.shortcut:hover {
    background: #f1f3f4;
}

.shortcut-icon {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 22px;
    font-weight: bold;
    background: #f1f3f4;
}

.youtube {
    color: #ff0000;
}

.google {
    color: #4285f4;
}

.wiki {
    color: #000;
}

.github {
    color: #333;
}

/* Footer */

footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 40px;
    background: #f1f3f4;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    font-size: 13px;
}


/* Dark mode */

body.dark {
    background: #202124;
    color: #e8eaed;
}

body.dark .browser {
    background: #292a2d;
}

body.dark .tab {
    background: #292a2d;
    color: #e8eaed;
}

body.dark .tab.active {
    background: #202124;
}

body.dark .address-form {
    background: #3c4043;
}

body.dark .address-form input {
    color: white;
}

body.dark .google-search {
    border-color: #5f6368;
    background: #303134;
}

body.dark .google-search input {
    background: transparent;
    color: white;
}

body.dark .shortcut:hover {
    background: #303134;
}

body.dark .shortcut-icon {
    background: #303134;
    color: white;
}

body.dark footer {
    background: #292a2d;
}

body.dark .menu {
    background: #292a2d;
    color: white;
}

body.dark .menu button {
    color: white;
}

body.dark .menu button:hover {
    background: #3c4043;
}
