#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xbmcaddon
import tvdbsimple as tvdb
from .utils import safe_get


ADDON = xbmcaddon.Addon()
tvdb.KEYS.API_KEY = 'd60d3c015fdb148931e8254c0e96f072'
tvdb.KEYS.API_TOKEN = ADDON.getSetting('token')


def filter_by_year(shows, year):
    """
    Filter a show by year

    :param shows: the list of shows from TVDB
    :param year: premiere year
    :return: a found show or None
    """
    for show in shows:
        firstAired = safe_get(show, 'firstAired', '')
        if firstAired and firstAired.startswith(str(year)):
            return show
    return None


def search_series_api(title):
    search = tvdb.Search()
    ret = None
    try:
        ret = search.series(title, language=ADDON.getSetting('language'))
    except:
        pass
    ADDON.setSetting('token', tvdb.KEYS.API_TOKEN)
    return ret


def get_series_details_api(id, all=True):
    show = tvdb.Series(id, language=ADDON.getSetting('language'))
    if all:
        try:
            show.info()
        except:
            return None
        try:
            show.actors()
        except:
            show.actors = []
    try:
        show.Images.fanart()
    except:
        show.Images.fanart = []
    try:
        show.Images.poster()
    except:
        show.Images.poster = []
    try:
        show.Images.series()
    except:
        show.Images.series = []
    try:
        show.Images.season()
    except:
        show.Images.season = []
    try:
        show.Images.seasonwide()
    except:
        show.Images.seasonwide = []
    ADDON.setSetting('token', tvdb.KEYS.API_TOKEN)
    return show


def get_series_episodes_api(id, language=None):
    ret = None
    if not language:
        language = ADDON.getSetting('language')
    showeps = tvdb.Series_Episodes(id, language=language)
    try:
        ret = showeps.all()
    except:
        pass
    ADDON.setSetting('token', tvdb.KEYS.API_TOKEN)
    return ret


def get_episode_details_api(id, language=None):
    if not language:
        language = ADDON.getSetting('language')
    ep = tvdb.Episode(id, language=language)
    try:
        ep.info()
    except:
        return None
    ADDON.setSetting('token', tvdb.KEYS.API_TOKEN)
    return ep