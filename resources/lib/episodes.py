#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xbmcplugin
import xbmcgui
import sys
from . import tvdb
from .utils import log
from .ratings import ratings


HANDLE = int(sys.argv[1])

# add the episodes of a series to the list


def get_series_episodes(id, settings):
    log(f'Find episodes of tvshow with id {id}')
    episodes = tvdb.get_series_episodes_api(id, settings)
    if not episodes:
        xbmcplugin.setResolvedUrl(
            HANDLE, False, xbmcgui.ListItem(offscreen=True))
        return
    for ep in episodes:
        liz = xbmcgui.ListItem(ep['episodeName'], offscreen=True)
        details = {'title': ep['episodeName'],
                   'aired': ep['firstAired']
                   }
        if (settings.getSettingBool('absolutenumber') == True):
            details['season'] = 1
            details['episode'] = ep['absoluteNumber']
        elif (settings.getSettingBool('dvdorder') == True):
            details['season'] = ep['dvdSeason']
            details['episode'] = ep['dvdEpisodeNumber']
        else:
            details['season'] = ep['airedSeason']
            details['episode'] = ep['airedEpisodeNumber']
        liz.setInfo('video', details)
        xbmcplugin.addDirectoryItem(handle=HANDLE, url=str(
            ep['id']), listitem=liz, isFolder=True)
    xbmcplugin.setResolvedUrl(handle=HANDLE, succeeded=True, listitem=liz)

# get the details of the found episode


def get_episode_details(id, images_url: str, settings):
    log(f'Find info of episode with id {id}')
    ep = tvdb.get_episode_details_api(id, settings)
    if not ep:
        xbmcplugin.setResolvedUrl(
            HANDLE, False, xbmcgui.ListItem(offscreen=True))
        return
    liz = xbmcgui.ListItem(ep.episodeName, offscreen=True)
    details = {'title': ep.episodeName,
               'plot': ep.overview,
               'plotoutline': ep.overview,
               'credits': ep.writers,
               'cast': ep.guestStars,
               'director': ep.directors,
               'premiered': ep.firstAired,
               'aired': ep.firstAired,
               'mediatype': 'episode'
               }

    if ep.airsAfterSeason and ep.airsAfterSeason >= 0:
        details['sortseason'] = 10000
        details['sortepisode'] = ep.airsAfterSeason
    elif ep.airsBeforeSeason and ep.airsBeforeSeason >= 0:
        details['sortepisode'] = ep.airsBeforeSeason
        details['sortseason'] = ep.airsBeforeEpisode

    if (settings.getSettingBool('absolutenumber') == True):
        details['season'] = 1
        details['episode'] = ep.absoluteNumber
    elif (settings.getSettingBool('dvdorder') == True):
        details['season'] = ep.dvdSeason
        details['episode'] = ep.dvdEpisodeNumber
    else:
        details['season'] = ep.airedSeason
        details['episode'] = ep.airedEpisodeNumber

    liz.setInfo('video', details)

    ratings(liz, ep, True, settings)

    if ep.imdbId:
        liz.setUniqueIDs({'tvdb': ep.id, 'imdb': ep.imdbId}, 'tvdb')
    else:
        liz.setUniqueIDs({'tvdb': ep.id}, 'tvdb')

    if ep.filename:
        liz.addAvailableArtwork(images_url+ep.filename)
    xbmcplugin.setResolvedUrl(handle=HANDLE, succeeded=True, listitem=liz)
