# -*- coding: UTF-8 -*-
#A part of the SuperBrowser addon for NVDA
#Copyright (C) 2018 Tony Malykh
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.

import addonHandler
import api
import bisect
import browseMode
import config
import compoundDocuments
import controlTypes
import ctypes
import eventHandler
import globalPluginHandler
import gui
import json
import NVDAHelper
from NVDAObjects.window import winword
import operator
import re
import sayAllHandler
from scriptHandler import script, willSayAllResume
import speech
import struct
import textInfos
import tones
import types
import ui
import wx

def myAssert(condition):
    if not condition:
        raise RuntimeError("Assertion failed")

hackLevel = 0
backup = None

class FakeNVDAObject:
    """This class is a wrapper around NVDA object class.
    It forwards all the method calls and attributes to the object it wraps, except for .setFocus() and .scrollIntoView(), which it simply ignores."""
    def __init__(self, obj):
        self.obj = obj

    def setFocus(self):
        pass

    def __getattr__(self, name):
        if name in ["setFocus", "scrollIntoView"]:
            return lambda : None
        func = getattr(self.obj, name)
        if type(func) == types.MethodType:
            return  lambda *args, **kwargs: func( *args, **kwargs)
        else:
            return  lambda *args, **kwargs: func(self.obj, *args, **kwargs)

def intercept():
    def makeInterceptFunc(targetFunc):
        def wrapperFunc(self, info, reason=controlTypes.REASON_CARET):
            global hackLevel
            if hackLevel >= 1:
                nonFocusableInfo = info.copy()
                nonFocusableInfo.focusableNVDAObjectAtStart = FakeNVDAObject(nonFocusableInfo.focusableNVDAObjectAtStart)
                nonFocusableInfo.NVDAObjectAtStart = FakeNVDAObject(nonFocusableInfo.NVDAObjectAtStart)
                info = nonFocusableInfo
            return targetFunc(self, info, reason)
        return wrapperFunc
    browseMode.BrowseModeDocumentTreeInterceptor._set_selection = makeInterceptFunc(browseMode.BrowseModeDocumentTreeInterceptor._set_selection)
    
    if False:
        def makeInterceptFunc2(targetFunc):
            def wrapperFunc(self,obj=None):
                global focusFollows
                if not focusFollows:
                    if not obj:
                        obj=self.currentNVDAObject
                    if obj:
                        obj = FakeNVDAObject(obj)
                return targetFunc(self, obj)
            return wrapperFunc
        browseMode.BrowseModeTreeInterceptor._activatePosition = makeInterceptFunc2(browseMode.BrowseModeTreeInterceptor._activatePosition)

        def makeInterceptFunc3(targetFunc):
            def wrapperFunc(self):
                global focusFollows
                if not focusFollows:
                    tones.beep(500, 50)
                    raise Exception("ASDF")
                return targetFunc(self)
            return wrapperFunc
        compoundDocuments.CompoundTextInfo.updateCaret = makeInterceptFunc3(compoundDocuments.CompoundTextInfo.updateCaret)
        compoundDocuments.CompoundTextInfo.updateSelection = makeInterceptFunc3(compoundDocuments.CompoundTextInfo.updateSelection)
    
    origFunc = eventHandler.doPreGainFocus
    def myfunc(obj,sleepMode=False):
        global hackLevel
        if hackLevel >= 2:
            return
        result = origFunc(obj,sleepMode)
        return result
    eventHandler.doPreGainFocus = myfunc
    
    
intercept()
addonHandler.initTranslation()
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("SuperBrowser")


    @script(description='Toggle focus follows browse mode.', gestures=['kb:NVDA+8'])
    def script_toggleFocusFollowsBrowseMode(self, gesture):
        global hackLevel
        hackLevel = (hackLevel + 1) % 3
        if hackLevel == 0:
            msg = _("Browse mode moves system focus on")
        elif hackLevel == 1:
            msg = _("Browse mode moves system focus off")
        else:
            msg = _("Browse mode moves system focus off plus focus hack")
        ui.message(msg)
