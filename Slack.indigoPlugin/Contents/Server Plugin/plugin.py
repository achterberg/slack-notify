#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-

import indigo
import simplejson
import urlparse, httplib
import hashlib
from datetime import date
import os
import sys
import platform
import MultipartPostHandler
import urllib
import urllib2

# Globals
plugin_id = "com.bot.indigoplugin.slack"

class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = pluginPrefs.get("showDebugInfo", False)

    def __del__(self):
        indigo.PluginBase.__del__(self)

    def startup(self):
        self.debugLog(u"startup called")
        self.debugLog(u"Indigo log path: %s" % self.returnlogpath ()[0:-1] )

    def shutdown(self):
        self.debugLog(u"shutdown called")

    def returnlogpath(self):
        baseDir = r"/Library/Application Support/Perceptive Automation/Indigo %s/" % (int(indigo.server.version[0]) )
        fileDate = str(date.today())
        logPath = os.path.join(baseDir + 'Logs', fileDate + ' Events.txt ')
        return logPath

    def shorten(self, url):
        # http://taoofmac.com/space/blog/2009/08/10/2205
        # BITLY_TOKEN = 'addtoken'
        services = {
        # 'api-ssl.bitly': '/v3/shorten?access_token=%s&longUrl=' % BITLY_TOKEN,
        # 'api.tr.im':   '/api/trim_simple?url=',
        'tinyurl.com': '/api-create.php?url=',
        'is.gd':       '/api.php?longurl='
        }
        for shortener in services.keys():
            c = httplib.HTTPConnection(shortener)
            c.request("GET", services[shortener] + urllib.quote(url))
            r = c.getresponse()
            shorturl = r.read().strip()
            if ("DOCTYPE" not in shorturl) and ("http://" + urlparse.urlparse(shortener)[1] in shorturl):
                return shorturl
            else:
                continue
            # raise IOError

    def getChannelNames(self):
        slackToken = self.pluginPrefs['slacktoken'].strip()
        params = urllib.urlencode({'token': slackToken, 'pretty': 1})
        url = urllib.urlopen("https://slack.com/api/channels.list?%s" % params)
        url = url.geturl()

        self.debugLog(u"Channels URL: %s" % url)

        jc = urllib2.urlopen(url)
        channelString = jc.read()
        jcl = simplejson.loads(channelString)

        cList = []
        for i in jcl['channels']:
            x = i['name']
            if x not in cList:
                cList.append(x)

        oList = list(cList)

        deck = []
        for i in range(len(cList)):
            while True:
                card = (oList[i],cList[i])
                deck.append(card)
                break
        return deck

    def channelListGenerator(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.getChannelNames()

    def validatePrefsConfigUi(self, valuesDict):
        self.debugLog(u"validatePrefsConfigUi() method called")
        errorsDict = indigo.Dict()
        errorsFound = False

        if len(valuesDict[u'urltoken']) == 0:
            errorsDict[u'urltoken'] = u'The plugin requires a Slack webhook token.'
            errorsFound = True
        if " " in (valuesDict[u'urltoken']):
            errorsDict[u'urltoken'] = u'The Slack webhook token can not contain spaces.'
            errorsFound = True

        if len(valuesDict[u'slacktoken']) == 0:
            errorsDict[u'slacktoken'] = u'The plugin requires a Slack token.'
            errorsFound = True
        if " " in (valuesDict[u'slacktoken']):
            errorsDict[u'slacktoken'] = u'The Slack token can not contain spaces.'
            errorsFound = True

        if len(valuesDict[u'userid']) == 0:
            errorsDict[u'userid'] = u'The plugin requires a Slack user ID.'
            errorsFound = True
        if " " in (valuesDict[u'userid']):
            errorsDict[u'userid'] = u'The Slack user ID can not contain spaces.'
            errorsFound = True

        if errorsFound:
            return (False, valuesDict, errorsDict)
        else:
            return (True, valuesDict)

    def closedPrefsConfigUi (self, valuesDict, userCancelled):
        self.debugLog(u"closedPrefsConfigUi() method called")

        if userCancelled is True:
            self.debugLog(u"User cancelled updating preferences")

        if userCancelled is False:
            indigo.server.log (u"Slack Notify preferences were updated.")
            self.debug = valuesDict.get('showDebugInfo', False)

        if self.debug is True:
            self.debugLog(u"Debugging on")
            self.debugLog(unicode(u"Debugging set to: %s" % self.pluginPrefs[u"showDebugInfo"]))
        else:
            self.debugLog(u"Debugging off")

    def notify(self, pluginAction):
        # get pluginAction variables #################################################################
        if pluginAction.props['text'] is None or pluginAction.props['text'] == "":
            indigo.server.log(u"No text was entered.")
        else:
            txtInput = pluginAction.props['text'].strip()
            txtInput = txtInput.strip()
            while "%%v:" in txtInput:
                txtInput = self.substituteVariable(txtInput)
            self.debugLog(u"Text entered: %s" % txtInput)
            # fix issue with special characters
            theText = txtInput.encode('utf8')

        if pluginAction.props['imageurl'] is None or pluginAction.props['imageurl'] == "":
            self.debugLog(u"No image url was entered")
        else:
            imgInput = pluginAction.props['imageurl'].strip()
            shortURL = self.shorten(imgInput)
            imgInput = shortURL.strip()
            theImageURL = imgInput.encode('utf8')
            self.debugLog(u"Image URL: %s" % imgInput)

        theChannel = '#' + pluginAction.props['channel']
        theDM = '@' + pluginAction.props['directMessage'].strip()
        if theChannel == "" and theDM == "":
            indigo.server.log(u"Enter either a channel OR a DM to post to.")
        elif theChannel == "" and theDM:
            theChannel = theDM
        theUsername = pluginAction.props['username'].strip()
        theIcon = pluginAction.props['icon'].strip()
        theFilePath = pluginAction.props['filename']
        ##############################################################################################

        # get pluginPrefs variables ##################################################################
        URLtoken = self.pluginPrefs['urltoken'].strip()
        slackToken = self.pluginPrefs['slacktoken'].strip()
        userID = self.pluginPrefs['userid'].strip()
        ##############################################################################################

        # get Slack user variables ###################################################################
        params = urllib.urlencode({'token': slackToken, 'user': userID, 'pretty': 1})
        url = urllib.urlopen("https://slack.com/api/users.info?%s" % params)
        url = url.geturl()
        self.debugLog(u"URL for user variables: %s" % url)

        try:
            j = urllib2.urlopen(url)
            varstring = j.read()
            js = simplejson.loads(varstring)
            if js.get('ok') in [False]:
                raise Exception(js.get('error'))
                self.errorLog(u"False response getting user variables: %s" % js.get('error'))
            loadOK = js['ok']
            userID = js['user']['id']
            userName = '@' + js['user']['name']
            userDeleted = js['user']['deleted']
            userRealName = js['user']['real_name']
            userColor = js['user']['color']
            userEmail = js['user']['profile']['email']
            userIconURL = js['user']['profile']['image_24']
            self.debugLog(u"id: %s" % userID)
            self.debugLog(u"name: %s" % userName)
            self.debugLog(u"deleted: %s" % userDeleted)
            self.debugLog(u"real name: %s" % userRealName)
            self.debugLog(u"color: %s" % userColor)
            self.debugLog(u"email: %s" % userEmail)
            self.debugLog(u"icon: %s" % userIconURL)
            # j.close()
        except urllib2.HTTPError, e:
            js = {}
            self.errorLog(u"Unable to get Slack(var). HTTPError - %s" % unicode(e))
        except urllib2.URLError, e:
            js = {}
            self.errorLog(u"Unable to get Slack(var). URLError - %s" % unicode(e))
        except Exception, e:
            js = {}
            if "invalid literal for int() with base 16: ''" in e:
                self.errorLog(u"Unable to get Slack(var) Obscure bug in Python 2.5.")
            else:
                self.errorLog(u"Unable to get Slack(var). Exception - %s" % unicode(e))
        ##############################################################################################

        # attempt to get gravatar if Slack icon does not exist #######################################
        if userIconURL is None or userIconURL == "":
            email = userEmail
            default = "http://www.gravatar.com/avatar/c4ac5c1a595fe25bad7ddb2eb2d7c2f4?d=identicon"
            size = 16
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
            userIconURL = gravatar_url
            self.debugLog(u"User icon set to gravatar: %s" % userIconURL)
        else:
            self.debugLog(u"User icon url set to: %s" % userIconURL)
        ##############################################################################################

        # construct the file upload ##################################################################
        if theFilePath is None or theFilePath == "":
            self.debugLog(u"No file path was entered")
        else:
            theFilePath = theFilePath.strip()
            if os.path.isfile(theFilePath):
                opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
                params = { "token" : slackToken, "file" : open(theFilePath, "rb") }
                fileUploadURL = 'https://slack.com/api/files.upload?'
            else:
                indigo.server.log (u"Invalid path to the file.")
        ##############################################################################################

        # construct and attempt to send payload to Slack #############################################
        if theUsername is None or theUsername == "":
            theUsername = userName
            self.debugLog(u"Username set to %s (bot)" % userName)
        surl = 'https://hooks.slack.com/services/%s' % URLtoken
        self.debugLog(u"Slack payload url: %s" % surl)
        if pluginAction.props['imageurl'] is None or pluginAction.props['imageurl'] == "":
            if theChannel and theUsername and theText != "":
                data = 'payload={"channel": "%s", "username": "%s", "link_names":"1", "text": "%s", "icon_emoji": ":%s:"}'% (theChannel, theUsername, theText, theIcon)
        else:
            if theChannel and theUsername and theText and theImageURL != "":
            # if print all([theChannel, theUsername, theText, theImageURL]) == "True"
                data = 'payload={"channel": "%s", "username": "%s", "link_names":"1", "text": "%s", "icon_emoji": ":%s:","attachments":[{"fallback": "Image is attached", "image_url": "%s"}]}'% (theChannel, theUsername, theText, theIcon, theImageURL)
        self.debugLog(u"Slack payload: %s" % data)
        req = urllib2.Request(surl, data)

        if theFilePath != "":
            try:
                opener.open(fileUploadURL, params)
                res = opener.open(url, params).read()
                fileRes = simplejson.loads(res)
                if fileRes.get('ok') in [False]:
                        resError = fileRes["error"]
                        self.errorLog(u"Exiting: Message not sent. File not uploaded: %s" % resError)
                        # sys.exit()
                self.debugLog(u"File upload response: %s" % res)
            except urllib2.HTTPError, e:
                self.errorLog(u"File not uploaded. HTTPError - %s" % unicode(e))
            except urllib2.URLError, e:
                self.errorLog(u"File not uploaded. URLError - %s" % unicode(e))
            except Exception, e:
                if "invalid literal for int() with base 16: ''" in e:
                    self.errorLog(u"Exception: invalid literal for int() with base 16")
                else:
                    self.errorLog(u"Exception - %s" % unicode(e))
            else:
                indigo.server.log (u"File uploaded.")

        try:
            urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            self.errorLog(u"Message not sent. HTTPError - %s" % unicode(e))
        except urllib2.URLError, e:
            self.errorLog(u"Message not sent. URLError - %s" % unicode(e))
        except Exception, e:
            if "invalid literal for int() with base 16: ''" in e:
                self.errorLog(u"Exception: invalid literal for int() with base 16")
            else:
                self.errorLog(u"Exception - %s" % unicode(e))
                indigo.server.log (u"Message not sent.")
        else:
            indigo.server.log (u"Message sent.")
        ##############################################################################################
