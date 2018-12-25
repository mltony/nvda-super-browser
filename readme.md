# nvda-super-browser
SuperBrowser is an add-on for NVDA that provides workarounds for some browse mode bugs in NVDA.

Caution: use it at your own risk. Don't use it if you don't understand what it is doing. 

## Background
When NVDA interacts with browsers, it sends focus events to the browser  every  time browse mode cursor moves. This results in certain bugs, such as:
* Rubber band effect in browse mode - when browse mode focus is sometimes pulled back to the previous location.
* Slowdown on large and JavaScript-heavy pages.
* Edit boxes and other form elements sporadically entering forms mode.
For more information see [NVDA issue 2039](https://github.com/nvaccess/nvda/issues/2039).

SuperBrowser provides a workaround for this issue.

## Keystrokes
* NVDA+8: cycle between SuperBrowser modes.
Superbrowser had three modes of operation:
* Browse mode moves system focus on: normal operation, the add-on is effectively disabled. This is default NVDA behavior.
*  Browse mode moves system focus off: NVDA doesn't send focus events to the browser. This fixes the rubber band effect and speeds up browse mode keystrokes response significantly. As a side effect, system focus will not always follow NVDA browse mode cursor, so when you press applications key (context menu) it will likely activate on a wrong element on the page.
* Browse mode moves system focus off plus focus hack: NVDA doesn't send focus events to the browser, plus an extra hack suppresses another code flow of sending focus events. In this mode edit boxes and other form elements never steal focus. In this mode many NVDA functions are effectively broken, so use with extreme caution.
