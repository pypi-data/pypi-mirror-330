# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugef\xc3\x83\xc2\xbcgt
# showValue: 48 Stunden
# showEntries: 6 Stunden
# showEpisodes: 4 Stunden

from helper.requestHandler import cRequestHandler
from helper.tools import cParser

SITE_IDENTIFIER = 'einschalten'
SITE_NAME = 'Einschalten'
SITE_ICON = 'einschalten.png'

URL_MAIN = 'https://einschalten.in'
URL_NEW_MOVIES = URL_MAIN + '/movies'
URL_LAST_MOVIES = URL_MAIN + '/movies?order=added'
URL_COLLECTIONS = URL_MAIN + '/collections'
URL_SEARCH = URL_MAIN + '/search?query=%s'


def load(): # Menu structure of the site plugin
    ret = []
    ret.append({"site": SITE_IDENTIFIER, "url": URL_NEW_MOVIES, "typ": 1, "key": "showEntries", "title": "New Movies"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_COLLECTIONS, "typ": 1, "key": "showEntries", "title": "Collections"})
    return ret


def showEntries(entryUrl=False, sSearchText=False):
    folder = []
    if not entryUrl: return
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = 'class="group.*?href="([^"]+).*?title="([^"]+).*?img src="([^"]+).*?(.*?)</a>'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch: return

    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        isYear, sYear = cParser.parseSingleResult(sDummy, '</svg>\s([\d]+)</div>') # Release Jahr
        isCollections, aResult = cParser.parse(sUrl, '/collections')
        oGuiElement = {}
        if isYear: oGuiElement["year"] = sYear
        oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showCollections' if isCollections else 'showHosters'
        oGuiElement["thumb"] = sThumbnail
        oGuiElement["url"] = sUrl
        oGuiElement["mediatype"] = 'movie'
        oGuiElement["total"] = total
        folder.append(oGuiElement)
    return folder


def showCollections(sUrl=False, sSearchText=False):
    entryUrl = URL_MAIN + sUrl
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = 'class="group.*?href="([^"]+).*?title="([^"]+).*?img src="([^"]+).*?(.*?)</a>'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch: return
    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        isYear, sYear = cParser.parseSingleResult(sDummy, '</svg>\s([\d]+)</div>') # Release Jahr
        oGuiElement = {}
        if isYear: oGuiElement["year"] = sYear
        oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showHosters'
        oGuiElement["thumb"] = sThumbnail
        oGuiElement["url"] = sUrl
        oGuiElement["mediatype"] = 'movie'
        oGuiElement["total"] = total
        oGuiElement["desc"] = sDesc
        folder.append(oGuiElement)
    return folder


def showEntriesLast(entryUrl=False, sSearchText=False):
    if not entryUrl: return
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    sHtmlContent = oRequest.request()
    pattern = 'class="group.*?href="([^"]+).*?title="([^"]+).*?img src="([^"]+).*?(.*?)</a>'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch: return
    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        isYear, sYear = cParser.parseSingleResult(sDummy, '</svg>\s([\d]+)</div>') # Release Jahr
        oGuiElement = {}
        if isYear: oGuiElement["year"] = sYear
        oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showHosters'
        oGuiElement["thumb"] = sThumbnail
        oGuiElement["url"] = sUrl
        oGuiElement["mediatype"] = 'movie'
        oGuiElement["total"] = total
        oGuiElement["desc"] = sDesc
        folder.append(oGuiElement)
    return folder


def showHosters(entryUrl=False):
    hosters = []
    sUrl = URL_MAIN + '/api' + entryUrl + '/watch'
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = 'streamUrl":"([^"]+)'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch: return
    sQuality = '720p'
    for sUrl in aResult:
        sName = cParser.urlparse(sUrl)
        hoster = {'link': sUrl, 'name': sName, 'displayedName': '%s [I][%s][/I]' % (sName, sQuality), 'quality': sQuality, 'resolved': True}
        hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    return [{'streamUrl': sUrl, 'resolved': False}]


def search(sSearchText):
    find = showEntries(URL_SEARCH % cParser().quotePlus(sSearchText), sSearchText)
    if find:
        if len(find) > 0:
            return find
    return None

