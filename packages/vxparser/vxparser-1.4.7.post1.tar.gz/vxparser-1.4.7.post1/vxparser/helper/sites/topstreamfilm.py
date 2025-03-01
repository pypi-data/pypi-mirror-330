# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugef\xc3\x83\xc2\xbcgt
# showValue: 48 Stunden
# showEntries: 6 Stunden
# showEpisodes: 4 Stunden
 
from helper.requestHandler import cRequestHandler
from helper.tools import cParser

SITE_IDENTIFIER = 'topstreamfilm'
SITE_NAME = 'Topstreamfilm'
SITE_ICON = 'topstreamfilm.png'

URL_MAIN = 'https://www.topstreamfilm.live'

URL_ALL = URL_MAIN + '/filme-online-sehen/'
URL_MOVIES = URL_MAIN + '/beliebte-filme-online/'
URL_KINO = URL_MAIN + '/kinofilme/'
URL_SERIES = URL_MAIN + '/serien/'
URL_SEARCH = URL_MAIN + '/?story=%s&do=search&subaction=search'


def load():
    ret = []
    ret.append({"site": SITE_IDENTIFIER, "url": URL_ALL, "typ": 1, "key": "showEntries", "title": "New Movies and Series"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_KINO, "typ": 1, "key": "showEntries", "title": "Current films in the cinema"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_MOVIES, "typ": 1, "key": "showEntries", "title": "Movies"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_SERIES, "typ": 2, "key": "showEntries", "title": "Series"})
    return ret


def showValue():
    folder = []
    oGuiElement = {}
    oRequest = cRequestHandler(URL_MAIN)
    oRequest.cacheTime = 60 * 60 * 48 # 48 Stunden
    sHtmlContent = oRequest.request()
    pattern = '>{0}</a>(.*?)</ul>'.format(params.getValue('Value'))
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if not isMatch:
        pattern = '>{0}</(.*?)</ul>'.format(params.getValue('Value'))
        isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        isMatch, aResult = cParser.parse(sHtmlContainer, 'href="([^"]+).*?>([^<]+)')
    if not isMatch: return

    for sUrl, sName in aResult:
        if sUrl.startswith('/'):
            sUrl = URL_MAIN + sUrl
        oGuiElement["url"] = sUrl
        oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        folder.append(oGuiElement)
    return folder


def showEntries(entryUrl=False, sSearchText=False):
    folder = []
    isTvshow = False
    if not entryUrl: return
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = 'TPostMv">.*?href="([^"]+).*?data-src="([^"]+).*?Title">([^<]+)(.*?)</li>'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch: return

    total = len(aResult)
    for sUrl, sThumbnail, sName, sDummy in aResult:
        if sName:
            sName = sName.split('- Der Film')[0].strip() # Name nach dem - abschneiden und Array [0] nutzen
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        isYear, sYear = cParser.parseSingleResult(sDummy, 'Year">([\d]+)</span>') # Release Jahr
        isDuration, sDuration = cParser.parseSingleResult(sDummy, 'time">([\d]+)') # Laufzeit
        if int(sDuration) <= int('70'): # Wenn Laufzeit kleiner oder gleich 70min, dann ist es eine Serie.
            isTvshow = True
        else:
            isTvshow = False
        if 'South Park: The End Of Obesity' in sName:
            isTvshow = False
        isQuality, sQuality = cParser.parseSingleResult(sDummy, 'Qlty">([^<]+)</span>') # Qualit\xc3\x83\xc2\xa4t
        isDesc, sDesc = cParser.parseSingleResult(sDummy, 'Description"><p>([^<]+)') # Beschreibung
        sThumbnail = URL_MAIN + sThumbnail
        oGuiElement = {}
        if isYear: oGuiElement["year"] = sYear
        if isDuration: oGuiElement["duration"] = sDuration
        if isQuality: oGuiElement["quality"] = sQuality
        if isDesc: if isDesc: oGuiElement["desc"] = sDesc
        oGuiElement["mediatype"] = 'tvshow' if isTvshow else 'movie'
        oGuiElement["thumb"] = sThumbnail
        oGuiElement["url"] = sUrl
        oGuiElement["total"] = total
        folder.append(oGuiElement)
    return folder


def showSeasons(entryUrl=False, sThumbnail=False):
    folder = []
    # Parameter laden
    if not entryUrl: return
    sUrl = entryUrl
    oRequest = cRequestHandler(sUrl)
    oRequest.cacheTime = 60 * 60 * 6 # HTML Cache Zeit 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<div class="tt_season">(.*)</ul>'
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        isMatch, aResult = cParser.parse(sHtmlContainer, '"#season-(\d+)')
    if not isMatch: return
    total = len(aResult)
    for sSeason in aResult:
        oGuiElement = {}
        oGuiElement["season"] = sSeason
        oGuiElement["mediatype"] = 'season'
        if sThumbnail: oGuiElement["thumb"] = sThumbnail
        oGuiElement["total"] = total
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showEpisodes'
        folder.append(oGuiElement)
    return folder


def showEpisodes(entryUrl=False, sThumbnail=False, sSeason=False, isDesc=False):
    folder = []
    # Parameter laden
    oRequest = cRequestHandler(entryUrl)
    oRequest.cacheTime = 60 * 60 * 4 # HTML Cache Zeit 4 Stunden
    sHtmlContent = oRequest.request()
    pattern = 'id="season-%s(.*?)</ul>' % sSeason
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        isMatch, aResult = cParser.parse(sHtmlContainer, 'data-title="Episode\s(\d+)')
    if not isMatch: return

    total = len(aResult)
    for sEpisode in aResult:
        oGuiElement = {}
        oGuiElement["key"] = 'showEpisodeHosters'
        if sThumbnail: oGuiElement["thumb"] = sThumbnail
        if sSeason: oGuiElement["season"] = sSeason
        if isDesc: oGuiElement["desc"] = isDesc
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["mediatype"] = 'episode'
        oGuiElement["e"] = str(sEpisode)
        oGuiElement["total"] = total
        folder.append(oGuiElement)
    return folder


def showEpisodeHosters(entryUrl=False, sSeason=False, sEpisode=False):
    hosters = []
    # Parameter laden
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = 'id="season-%s">(.*?)</ul>' % sSeason
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        pattern = '>%s</a>(.*?)</li>' % sEpisode
        isMatch, sHtmlLink = cParser.parseSingleResult(sHtmlContainer, pattern)
    if isMatch:
        isMatch, aResult = cParser().parse(sHtmlLink, 'data-link="([^"]+)')
    if isMatch:
        for sUrl in aResult:
            sName = cParser.urlparse(sUrl)
            if 'youtube' in sUrl:
                continue
            elif sUrl.startswith('//'):
                sUrl = 'https:' + sUrl
            hoster = {'link': sUrl, 'name': cParser.urlparse(sUrl)}
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def showHosters(entryUrl=False):
    hosters = []
    if not entryUrl: return
    sUrl = entryUrl
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = '"embed.*?src="([^"]+)'
    isMatch, hUrl = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        sHtmlContainer = cRequestHandler(hUrl).request()
        isMatch, aResult = cParser().parse(sHtmlContainer, 'data-link="([^"]+)')
    if isMatch:
        for sUrl in aResult:
            sName = cParser.urlparse(sUrl)
            if 'youtube' in sUrl:
                continue
            elif sUrl.startswith('//'):
                sUrl = 'https:' + sUrl
            hoster = {'link': sUrl, 'name': cParser.urlparse(sUrl)}
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    return [{'streamUrl': sUrl, 'resolved': False}]


def search(sSearchText):
    find = showEntries(URL_SEARCH % cParser.quotePlus(sSearchText), sSearchText)
    if find:
        if len(find) > 0:
            return find
    return None


def showSearch():
    sSearchText = cGui().showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    cGui().setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_SEARCH % cParser.quotePlus(sSearchText), oGui, sSearchText)

