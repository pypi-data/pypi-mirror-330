# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugefÃ¼gt
    #showGenre:     48 Stunden
    #showYears:     48 Stunden
    #showEntries:    6 Stunden
    #showEpisodes:   4 Stunden

from helper.requestHandler import cRequestHandler
from helper.tools import cParser

SITE_IDENTIFIER = 'xcine'
SITE_NAME = 'xCine'
SITE_ICON = 'xcinetop.png'

URL_MAIN = 'https://xcine.click/'
URL_NEW = URL_MAIN + 'kinofilme-online/'
URL_KINO = URL_MAIN + 'aktuelle-kinofilme-im-kino/'
URL_MOVIES = URL_MAIN + 'kinofilme-online'
URL_ANIMATION = URL_MAIN + 'animation/'
URL_SERIES = URL_MAIN + 'serienstream-deutsch/'
URL_SEARCH = URL_MAIN + 'index.php?do=search&subaction=search&story=%s&titleonly=3'


def load():
    ret = []
    ret.append({"site": SITE_IDENTIFIER, "url": URL_NEW, "typ": 1, "key": "showEntries", "title": "New"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_KINO, "typ": 1, "key": "showEntries", "title": "Current films in the cinema"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_MOVIES, "typ": 1, "key": "showEntries", "title": "Movies"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_ANIMATION, "typ": 1, "key": "showEntries", "title": "Animated Films"})
    ret.append({"site": SITE_IDENTIFIER, "url": URL_SERIES, "typ": 2, "key": "showEntries", "title": "Series"})
    return ret


def showEntries(entryUrl=False, sSearchText=False):
    folder = []
    isTvshow = False
    if not entryUrl: return
    oRequest = cRequestHandler(entryUrl, ignoreErrors=True)
    oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    iPage = 1
    oRequest = cRequestHandler(entryUrl + 'page/' + str(iPage) if iPage > 0 else entryUrl, ignoreErrors=True)
    sHtmlContent = oRequest.request()
    pattern = 'item__link.*?href="([^"]+).*?<img src="([^"]+).*?alt="([^"]+).*?(.*?)</span>\s+<span>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch: return


    total = len(aResult)
    for sUrl, sThumbnail, sName, sDummy in aResult:
        if sSearchText and not cParser.search(sSearchText, sName): continue
        # Abfrage der voreingestellten Sprache
        sLanguage = 1
        if (sLanguage == '1' and 'English*' in sName): continue # Deutsch
        if (sLanguage == '2' and not 'English*' in sName): continue # English
        elif sLanguage == '3': continue # Japanisch
        isQuality, sQuality = cParser.parseSingleResult(sDummy, 'movie-item__label">([^<]+)')  # QualitÃ¤t
        isInfoEpisode, sInfoEpisode = cParser.parseSingleResult(sDummy, 'ep-num">e.([\d]+)')  # Episodenanzahl
        isYear, sYear = cParser.parseSingleResult(sDummy, 'meta ws-nowrap">\s+<span>([\d]+)')  # Release Jahr
        #isTvshow, aResult = cParser.parse(sName, '\s+-\s+Staffel\s+\d+')
        isTvshow = True if 'taffel' in sName else False
        if sThumbnail[0] == '/': sThumbnail = sThumbnail[1:]
        oGuiElement = {}
        if isTvshow:
            if ' - Staffel ' in sName:
                oGuiElement["name"] = sName.split(' - ')[0]
                s = sName.split('Staffel ')[1]
                oGuiElement["s"] = s.split(' ')[0]
            elif '- Staffel ' in sName:
                oGuiElement["name"] = sName.split('- ')[0]
                s = sName.split('Staffel ')[1]
                oGuiElement["s"] = s.split(' ')[0]
            elif ' Staffel ' in sName:
                oGuiElement["name"] = sName.split(' Staffel ')[0]
                s = sName.split(' Staffel ')[1]
                oGuiElement["s"] = s.split(' ')[0]
            else: oGuiElement["name"] = sName
        else: oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showEpisodes' if isTvshow else 'showHosters'
        oGuiElement["thumb"] = URL_MAIN + sThumbnail
        oGuiElement["url"] = sUrl
        # oGuiElement["p2"] = sName
        oGuiElement["mediatype"] = 'season' if isTvshow else 'movie'
        oGuiElement["total"] = total
        if isYear: oGuiElement["year"] = sYear
        folder.append(oGuiElement)
    return folder


def showEpisodes(entryUrl=False):
    folder = []
    if not entryUrl: return
    oRequest = cRequestHandler(entryUrl)
    oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    sHtmlContent = oRequest.request()
    isMatch, aResult = cParser.parse(sHtmlContent, '"><a href="#">([^<]+)')
    if not isMatch: return

    isDesc, sDesc = cParser.parseSingleResult(sHtmlContent, '"description"[^>]content="([^"]+)')
    total = len(aResult)
    for sName in aResult:
        oGuiElement = {}
        oGuiElement["name"] = sName
        oGuiElement["site"] = SITE_IDENTIFIER
        oGuiElement["key"] = 'showHosters'
        oGuiElement["url"] = entryUrl
        oGuiElement["p2"] = sName
        oGuiElement["e"] = sName.split(' ')[1]
        oGuiElement["mediatype"] = 'episode'
        oGuiElement["total"] = total
        if isDesc: oGuiElement["desc"] = sDesc
        folder.append(oGuiElement)
    return folder


def showHosters(entryUrl=False, episode=False):
    hosters = []
    if not entryUrl: return
    sUrl = entryUrl
    sHtmlContent = cRequestHandler(sUrl).request()
    if episode:
        pattern = '>{0}<.*?</ul></li>'.format(episode)
        isMatch, sHtmlContent = cParser.parseSingleResult(sHtmlContent, pattern)
    isMatch, aResult = cParser().parse(sHtmlContent, 'link="([^"]+)')
    if isMatch:
        for sUrl in aResult:
            sName = cParser.urlparse(sUrl)
            if 'youtube' in sUrl: continue
            elif 'vod' in sUrl: continue
            elif sUrl.startswith('//'): sUrl = 'https:' + sUrl
            hoster = {'link': sUrl, 'name': cParser.urlparse(sUrl)}
            hosters.append(hoster)
    if hosters: hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    return [{'streamUrl': sUrl, 'resolved': False}]


def search(sSearchText):
    oGui = False
    find = showEntries(URL_SEARCH % cParser.quotePlus(sSearchText), sSearchText)
    if find:
        if len(find) > 0:
            return find
    return None

