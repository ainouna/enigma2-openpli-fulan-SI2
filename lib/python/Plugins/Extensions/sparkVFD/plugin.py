# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from ServiceReference import ServiceReference
from Components.ServiceList import ServiceList
from enigma import iPlayableService, iServiceInformation, iTimeshiftServicePtr, iRecordableService, eTimer, evfd, eDVBVolumecontrol, iFrontendInformation
from time import localtime, strftime, sleep
from Components.ServiceEventTracker import ServiceEventTracker
from Components.Console import Console
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from os import environ, statvfs
from Components.ActionMap import ActionMap
from Components.config import *
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.Language import language
from Components.Sources.StaticText import StaticText
from Tools.HardwareInfo import HardwareInfo
from Screens.Screen import Screen
import gettext
#Version 210327.1
stb = HardwareInfo().get_device_name()
lang = language.getLanguage()
environ['LANGUAGE'] = lang[:2]
gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain('enigma2')
gettext.bindtextdomain('VFD-Icons', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'SystemPlugins/VFD-Icons/locale/'))

def _(txt):
	t = gettext.dgettext('VFD-Icons', txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block

try:
	DisplayType = evfd.getInstance().getVfdType()
	if DisplayType != 4 and DisplayType != 8:
		DisplayType = None
except:
	DisplayType = None
DisplayTypevfd = DisplayType

if DisplayTypevfd is None:
	if stb.lower() != 'spark':
		DisplayType = None

config.plugins.vfdicon = ConfigSubsection()
if DisplayTypevfd == 8:  # VFD
	config.plugins.vfdicon.displayshow = ConfigSelection(default = "channel",
		choices = [
			("nothing", _("blank")),
			("channel_number", _("channel number")),
			("channel", _("channel name")),
			("channel_namenumber", _("channel number and name")),
			("time", _("time")),
			("date", _("date")),
			("day_date", _("day and date"))
			])
else:
	config.plugins.vfdicon.displayshow = ConfigSelection(default = "channel_namenumber",
		choices = [
			("nothing", _("blank")),
			("channel_number", _("channel number")),
			("channel", _("channel name")),
			("channel_namenumber", _("channel number and name")),
			("time", _("time")),
			("date", _("date")),
			("day_date", _("day and date"))
			])
if DisplayTypevfd == 8:  # VFD
	config.plugins.vfdicon.stbdisplayshow = ConfigSelection(default = "nothing",
		choices = [
			("nothing", _("nothing")),
			("date", _("date")),
			("day_date", _("day and date")),
			])
else:
	config.plugins.vfdicon.stbdisplayshow = ConfigSelection(default = "time",
		choices = [
			("nothing", _("nothing")),
			("time", _("time")),
			("date", _("date")),
			("time_date", _("time and date")),
			("day_date", _("day and date")),
			("time_day_date", _("time, day and date"))
			])
if DisplayTypevfd == 8:  # VFD
	config.plugins.vfdicon.contrast = ConfigSlider(default=5, limits=(0, 7))
	config.plugins.vfdicon.stbcontrast = ConfigSlider(default=3, limits=(0, 7))
config.plugins.vfdicon.uppercase = ConfigYesNo(default = True)
config.plugins.vfdicon.textscroll = ConfigSelection(default = "1",
	choices = [
		("0", _("no")),
		("1", _("once")),
		("2", _("continuous"))
		])
if DisplayTypevfd == 8:  # VFD
	config.plugins.vfdicon.textcenter = ConfigSelection(default = "0",
		choices = [
			("0", _("no")),
			("1", _("yes"))
			])
	config.plugins.vfdicon.showicons = ConfigSelection(default = "all",
		choices = [
			("none", _("none")),
			("partial", _("partial")),
			("all", _("all"))
			])
	config.plugins.vfdicon.hddicons = ConfigSelection(default = "hdd",
		choices = [
			("no", _("signal quality")),
			("hdd", _("on hdd")),
			("all mounts", _("on all mounts"))
			])
config.plugins.vfdicon.standbyredledon = ConfigYesNo(default = False)
config.plugins.vfdicon.dstandbyredledon = ConfigYesNo(default = False)
config.plugins.vfdicon.recredledon = ConfigSelection(default = "2",
	choices = [
		("0", _("off")),
		("1", _("on")),
		("2", _("blink"))
		])
config.plugins.vfdicon.extMenu = ConfigYesNo(default = True)

class ConfigVFDDisplay(Screen, ConfigListScreen):
	def __init__(self, session):
		self.icons_showicons = None
		Screen.__init__(self, session)
		self.skinName = ["Setup"]
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "SetupActions", "ColorActions"],
			{
				'left': self.keyLeft,
				'down': self.keyDown,
				'up': self.keyUp,
				'right': self.keyRight,
				"cancel": self.cancel,
				"ok": self.keySave,
				"green": self.keySave,
				"red": self.cancel,
			}, -2)
		self.cfglist = []
		ConfigListScreen.__init__(self, self.cfglist, session = session)
		if DisplayTypevfd == 8:  # VFD
			self.setTitle(_("VFD display configuration"))
		else:
			self.setTitle(_("LED display configuration"))
		self.createSetup()

	def createSetup(self):
		self.cfglist = []
		if DisplayTypevfd == 8:  # VFD
			self.cfglist.append(getConfigListEntry(_("Show on VFD display"), config.plugins.vfdicon.displayshow))
			self.cfglist.append(getConfigListEntry(_("Show on VFD display in standby"), config.plugins.vfdicon.stbdisplayshow))
			self.cfglist.append(getConfigListEntry(_("VFD brightness"), config.plugins.vfdicon.contrast))
			self.cfglist.append(getConfigListEntry(_("Standby brightness"), config.plugins.vfdicon.stbcontrast))
		else:
			self.cfglist.append(getConfigListEntry(_("Show on LED display"), config.plugins.vfdicon.displayshow))
			self.cfglist.append(getConfigListEntry(_("Show on LED display in standby"), config.plugins.vfdicon.stbdisplayshow))
		self.cfglist.append(getConfigListEntry(_("Uppercase letters only"), config.plugins.vfdicon.uppercase))
		self.cfglist.append(getConfigListEntry(_("Scroll text"), config.plugins.vfdicon.textscroll))
		if DisplayTypevfd == 8:  # VFD
			self.cfglist.append(getConfigListEntry(_("Center text"), config.plugins.vfdicon.textcenter))
			self.cfglist.append(getConfigListEntry(_("Show icons"), config.plugins.vfdicon.showicons))
			self.icons_showicons = config.plugins.vfdicon.showicons.value
			if self.icons_showicons == "all":
				self.cfglist.append(getConfigListEntry(_("Show HDD icons"), config.plugins.vfdicon.hddicons))
		self.cfglist.append(getConfigListEntry(_('Red LED on in standby'), config.plugins.vfdicon.standbyredledon))
		self.cfglist.append(getConfigListEntry(_('Red LED on in deep standby'), config.plugins.vfdicon.dstandbyredledon))
		self.cfglist.append(getConfigListEntry(_('Red LED during recording'), config.plugins.vfdicon.recredledon))
		self.cfglist.append(getConfigListEntry(_('Show this plugin in plugin menu'), config.plugins.vfdicon.extMenu))
		self["config"].list = self.cfglist
		self["config"].l.setList(self.cfglist)

	def newConfig(self):
		global DisplayType
		if DisplayTypevfd == 8:
			if self["config"].getCurrent()[1] == config.plugins.vfdicon.stbcontrast:
				Console().ePopen("fp_control -b " + str(config.plugins.vfdicon.stbcontrast.value))
			else:
				Console().ePopen("fp_control -b " + str(config.plugins.vfdicon.contrast.value))
		print "newConfig", self["config"].getCurrent()
		self.createSetup()

	def cancel(self):
		main(self)
		ConfigListScreen.keyCancel(self)

	def keySave(self):
		global DisplayType
		if DisplayTypevfd == 8:
			Console().ePopen("fp_control -b " + str(config.plugins.vfdicon.contrast.value))
			print "[VFD-Icons] set brightness", config.plugins.vfdicon.contrast.value
		if config.plugins.vfdicon.textscroll.value is not None:
			evfd.getInstance().vfd_set_SCROLL(int(config.plugins.vfdicon.textscroll.value))
		else:
			evfd.getInstance().vfd_set_SCROLL(1)
		print "[VFD-Icons] set text scroll", config.plugins.vfdicon.textscroll.value
		if DisplayTypevfd == 8:
			if config.plugins.vfdicon.textcenter.value == "1":
				evfd.getInstance().vfd_set_CENTER(True)
			else:
				evfd.getInstance().vfd_set_CENTER(False)
			print "[VFD-Icons] set text centering", config.plugins.vfdicon.textcenter.value
		main(self)
		ConfigListScreen.keySave(self)

	def keyLeft(self):
		self["config"].handleKey(KEY_LEFT)
		self.newConfig()

	def keyRight(self):
		self["config"].handleKey(KEY_RIGHT)
		self.newConfig()

	def keyDown(self):
		self['config'].instance.moveSelection(self['config'].instance.moveDown)
		self.newConfig()

	def keyUp(self):
		self['config'].instance.moveSelection(self['config'].instance.moveUp)
		self.newConfig()

def opencfg(session, **kwargs):
		session.open(ConfigVFDDisplay)
		if DisplayType == 8:
			evfd.getInstance().vfd_write_string( "VFD SETUP" )

def LEDdisplaymenu(menuid, **kwargs):
	if menuid == "expert":
		if DisplayTypevfd == 8:  # VFD
			return [(_("VFD display"), opencfg, "led_display", 44)]
		else:
			return [(_("LED display"), opencfg, "led_display", 44)]
	else:
		return []


class VFDIcons:
	def __init__(self, session):
		self.session = session
		self.onClose = []
		print '[VFD-Icons] Start'
		self.VFD = False
		self.play = False
		self.record = False
		self.mp3Available = False
		self.standby = False
		global DisplayType
		if DisplayType == 8:
			self.VFD = True
			self.tuned = False
			self.timeshift = False
			self.isMuted = False
			self.usb = 0
			self.isMuted = False
			self.usb = 0
		self.timer = eTimer()
		self.timer.callback.append(self.timerEvent)
		self.timer.start(59998, False) # start one minute timer
		global dot
		dot = 0
		print '[VFD-Icons] Hardware displaytype:', DisplayType
		print '[VFD-Icons] VFD displaytype     :', DisplayTypevfd
		if DisplayType == 4:
			self.__event_tracker = ServiceEventTracker(screen = self,eventmap =
				{
					iPlayableService.evUpdatedInfo: self.UpdatedInfo,
					iPlayableService.evUpdatedEventInfo: self.__evUpdatedEventInfo,
					iPlayableService.evStart: self.__evStart
				})
			config.misc.standbyCounter.addNotifier(self.onEnterStandby, initial_call = False)
			session.nav.record_event.append(self.gotRecordEvent)
		elif DisplayType == 8:
			self.__event_tracker = ServiceEventTracker(screen = self,eventmap =
				{
					iPlayableService.evUpdatedInfo: self.UpdatedInfo,
					iPlayableService.evUpdatedEventInfo: self.__evUpdatedEventInfo,
					iPlayableService.evVideoSizeChanged: self.__evVideoSizeChanged,
					iPlayableService.evSeekableStatusChanged: self.__evSeekableStatusChanged,
					iPlayableService.evTunedIn: self.__evTunedIn,
					iPlayableService.evTuneFailed: self.__evTuneFailed,
					iPlayableService.evStart: self.__evStart
				})
			config.misc.standbyCounter.addNotifier(self.onEnterStandby, initial_call = False)
			session.nav.record_event.append(self.gotRecordEvent)
			try:
				from Plugins.SystemPlugins.Hotplug.plugin import hotplugNotifier
				hotplugNotifier.append(self.hotplugCB)
			except:
				pass
			self.dir = None
			self.mount = None
			self.firstmount = -1
			global hddUsed
			hddUsed = -1
			self.SetMount()
			if self.mount:
				self.firstmount = self.mount
			if self.standby == False:
				self.displayHddUsed()
		else:
			self.__event_tracker = ServiceEventTracker(screen = self,eventmap =
				{
					iPlayableService.evStart: self.writeName,
				})
		print '[VFD-Icons] Set text scrolling option'
		if config.plugins.vfdicon.textscroll.value is not None:
			evfd.getInstance().vfd_set_SCROLL(int(config.plugins.vfdicon.textscroll.value))
		else:
			evfd.getInstance().vfd_set_SCROLL(1)
		print '[VFD-Icons] End initialisation'

	def __evStart(self):
		print '[VFD-Icons] __evStart'
		if DisplayType == 8:
			self.__evSeekableStatusChanged()
#		... and do nothing else

	def __evUpdatedEventInfo(self):
		print '[VFD-Icons] __evUpdatedEventInfo'
#		... and do nothing else

	def UpdatedInfo(self):
		print '[VFD-Icons] __evUpdatedInfo'
		self.checkAudioTracks()
		self.writeName()
		self.showDTS()
		if DisplayType == 8:
			self.showCrypted()
			self.showDolby()
			self.showMP3()
			self.showMute()
			self.showTuned()
			self.showMute()

	def writeName(self):
		displayshow = config.plugins.vfdicon.displayshow.value
		if displayshow != "time" and displayshow != "date" and displayshow != "day_date":
			servicename = "        "
			if displayshow != "nothing":
				service = self.session.nav.getCurrentlyPlayingServiceOrGroup()
				if service:
					path = service.getPath()
					if path:
						self.play = True
						servicename = "PLAY"
						currPlay = self.session.nav.getCurrentService()
						if currPlay != None and self.mp3Available: # show the MP3 tag
							servicename = currPlay.info().getInfoString(iServiceInformation.sTagTitle) + " - " + currPlay.info().getInfoString(iServiceInformation.sTagArtist)
							if DisplayType == 8:
								Console().ePopen("fp_control -i 28 1 -i 27 0") #Radio icon on, TV off
						else: # show the file name
							self.service = self.session.nav.getCurrentlyPlayingServiceReference()
							if not self.service is None:
								service = self.service.toCompareString()
								servicename = ServiceReference(service).getServiceName().replace('\xc2\x87', '').replace('\xc2\x86', '').ljust(16)
							if DisplayType == 8:
								Console().ePopen("fp_control -i 27 1 -i 28 0") #TV icon on, Radio off
						if DisplayType == 8:
							Console().ePopen("fp_control -i 3 1") #play
							if config.plugins.vfdicon.hddicons.value == "no":
								self.displayHddUsedOff() #switch off signal strength
					else:
						if displayshow == "channel_number" or displayshow == "channel_namenumber":
							servicename = str(service.getChannelNum())
							if len(servicename) == 1:
								servicename = '000' + servicename
							elif len(servicename) == 2:
								servicename = '00' + servicename
							elif len(servicename) == 3:
								servicename = '0' + servicename
						if displayshow == "channel_namenumber":
							servicename = servicename + ' ' + ServiceReference(service).getServiceName()
						if displayshow == "channel":
							servicename = ServiceReference(service).getServiceName()
						if DisplayType == 8:
							Console().ePopen("fp_control -i 3 0") #play
							self.play = False
							#evaluate radio or tv
							if config.plugins.vfdicon.showicons.value == "all":
								if config.servicelist.lastmode.value == 'tv':
									Console().ePopen("fp_control -i 27 1 -i 28 0") #TV icon on, Radio off
								else:
									Console().ePopen("fp_control -i 28 1 -i 27 0") #Radio icon on, TV off
			if config.plugins.vfdicon.uppercase.value is not None:
				servicename = servicename.upper()
			evfd.getInstance().vfd_write_string(servicename[0:63])

	def showCrypted(self):
		if config.plugins.vfdicon.showicons.value != "none":
			service = self.session.nav.getCurrentService()
			if service:
				info = service.info()
				crypted = info.getInfo(iServiceInformation.sIsCrypted)
				if crypted == 1:
					Console().ePopen("fp_control -i 11 1") #Crypt
				else:
					Console().ePopen("fp_control -i 11 0")

	def checkAudioTracks(self):
		self.mp3Available = False
		service = self.session.nav.getCurrentService()
		self.dolbyAvailable = False
		self.DTSAvailable = False
		if service:
			audio = service.audioTracks()
			if audio:
				n = audio.getNumberOfTracks()
				for x in range(n):
					i = audio.getTrackInfo(x)
					description = i.getDescription();
					if description.find("MP3") != -1:
						self.mp3Available = True
					if description.find("AC3") != -1:
						self.dolbyAvailable = True
					if description.find("DTS") != -1:
						self.DTSAvailable = True

	def showDolby(self):
		if self.dolbyAvailable:
			Console().ePopen("fp_control -i 26 1") #AC-3
		else:
			Console().ePopen("fp_control -i 26 0")

	def showMP3(self):
		if self.mp3Available:
			Console().ePopen("fp_control -i 25 1") #MP3
		else:
			Console().ePopen("fp_control -i 25 0")

	def showDTS(self):
		if self.DTSAvailable or self.dolbyAvailable:
			Console().ePopen("fp_control -i 10 1") #Dolby
		else:
			Console().ePopen("fp_control -i 10 0")

	def showTuned(self):
		if config.plugins.vfdicon.showicons.value == "all":
			if self.tuned == True:
				service = self.session.nav.getCurrentService()
				if service is not None and self.play == False:
					info = service.info()
					TPdata = info and info.getInfoObject(iServiceInformation.sTransponderData)
					print "[VFD-Icons] Set SAT icon"
					Console().ePopen("fp_control -i 44 1 -i 45 0") #dot1 on, dot2 off
				self.showSignal()
			else:
				                             #TER,    SAT,    HD,     Timeshift,Dolby,MP3,    AC-3,   TS_DOT1 TS_CAB off, Alert on
				Console().ePopen("fp_control -i 37 0 -i 42 0 -i 14 0 -i 43 0 -i 10 0 -i 25 0 -i 26 0 -i 44 0 -i 45 0 -i 29 1")


	def showMute(self):
		if config.plugins.vfdicon.showicons.value != "none":
			self.isMuted = eDVBVolumecontrol.getInstance().isMuted()
			if self.isMuted:
				Console().ePopen("fp_control -i 8 1") #Mute
			else:
				Console().ePopen("fp_control -i 8 0")

	def showSignal(self):
		if (config.plugins.vfdicon.hddicons.value == "no" and config.plugins.vfdicon.showicons.value == "all" and self.play == False and self.standby == False):
			Console().ePopen("fp_control -i 30 0") #HDD grid off
			service = self.session.nav.getCurrentService()
			if service:
				info = service.info()
				feinfo = service.frontendInfo()
				SQ = feinfo and feinfo.getFrontendInfo(iFrontendInformation.signalQuality)
#				SQdB = feinfo and feinfo.getFrontendInfo(iFrontendInformation.signalQualitydB)
#				snr = feinfo and feinfo.getFrontendInfo(iFrontendInformation.snrValue)
				signal = (SQ * 86) / 0xFFFF
				self.showSize(signal)

	def showTimer(self):
		if config.plugins.vfdicon.showicons.value == "all":
			# check if timers are set
			next_rec_time = -1
			next_rec_time = self.session.nav.RecordTimer.getNextRecordingTime()
			if next_rec_time > 0:
				Console().ePopen("fp_control -i 33 1") #Timer
			else:
				Console().ePopen("fp_control -i 33 0")

	def timerEvent(self):
		if self.standby == False:
			self.showSignal()
			self.showMute() #update mute icon
			self.showTimer() #update timer icon
			if (self.record == True and config.plugins.vfdicon.recredledon.value):
				Console().ePopen("fp_control -l 0 " + str(config.plugins.vfdicon.recredledon.value))
			if config.plugins.vfdicon.showicons.value == "all":
				if (self.record == True or self.timeshift == True): # if recording or timeshifting, display a rotating disc
					self.displayHddUsed() # update HDD display
					if self.disc == 1:
						Console().ePopen("fp_control -i 40 0")
					if self.disc == 2:
						Console().ePopen("fp_control -i 39 0")
					if self.disc == 3:
						Console().ePopen("fp_control -i 38 0 -i 40 1")
	#				if self.disc == 4:
	#					Console().ePopen("fp_control -i 40 1")
					if self.disc == 4:
						Console().ePopen("fp_control -i 39 1")
					if self.disc == 5:
						Console().ePopen("fp_control -i 38 1")
					self.disc += 1 # indicate next state
					if self.disc == 6:
						self.disc = 1
		if self.record == False and self.timeshift == False:
	 		if self.standby == False:
				disptype = config.plugins.vfdicon.displayshow.value
			else:
				disptype = config.plugins.vfdicon.stbdisplayshow.value
			self.writeDate(disptype)

	def __evVideoSizeChanged(self):
		if config.plugins.vfdicon.showicons.value != "none":
			service = self.session.nav.getCurrentService()
			if service:
				info = service.info()
				height = info.getInfo(iServiceInformation.sVideoHeight)
				if config.plugins.vfdicon.showicons.value == "all":
					if config.plugins.vfdicon.hddicons.value == "no":
						if height > 720: #set FULL symbol
							Console().ePopen("fp_control -i 22 1")
						else:
							Console().ePopen("fp_control -i 22 0")
				if height > 576: #set HD icon
					Console().ePopen("fp_control -i 14 1")
				else:
					Console().ePopen("fp_control -i 14 0")

	def __evSeekableStatusChanged(self):
		if config.plugins.vfdicon.showicons.value == "all":
			if not os.path.exists('/proc/stb/lcd/symbol/timeshift'):
				service = self.session.nav.getCurrentService()
				if service:
					if self.play == False:
						ts = service and service.timeshift()
#						if ts and ts.isTimeshiftEnabled() > 0:
						if ts and ts.isTimeshiftActive() > 0:
							self.timeshift = True
							Console().ePopen("fp_control -i 43 1") #Timeshift
							self.discOn()
						else:
							self.timeshift = False
							Console().ePopen("fp_control -i 43 0") #Timeshift icon off
							if self.record == False:
								self.discOff()

	def gotRecordEvent(self, service, event):
		if event in (iRecordableService.evEnd, iRecordableService.evStart, None):
			led = config.plugins.vfdicon.recredledon.value
			recs = self.session.nav.getRecordings()
			nrecs = len(recs)
			if nrecs > 0: #one or more recordings active
				self.record = True
				if config.plugins.vfdicon.showicons.value != 'none' and DisplayType == 8:
					if nrecs > 1: #two or more recordings active
						Console().ePopen("fp_control -i 7 1 -i 15 1") #REC1+2 on
					elif nrecs > 0: #one recording active
						self.record = True
						Console().ePopen("fp_control -i 7 1 -i 15 0") #REC1 on, REC2 off
						self.discOn()
					else: # no recording active
						Console().ePopen("fp_control -i 7 0 -i 15 0 -l 0 0") #REC1, REC2 & LED off
						if self.timeshift == False:
							self.discOff()
					self.RecordEnd()
				if (self.record == True and config.plugins.vfdicon.recredledon.value):
					Console().ePopen("fp_control -l 0 " + str(config.plugins.vfdicon.recredledon.value))
					if led == "2":
						self.timer.stop() # stop minute timer
						self.timer.start(2000, False) # start two second timer
					if led == "1":
						Console().ePopen("fp_control -l 0 1") #Red LED on
			else:
				self.timer.stop() # stop 2 second timer
				if self.standby == True:
					if config.plugins.vfdicon.standbyredledon.value:
						Console().ePopen("fp_control -l 0 1") #Red LED on
					if stbdisplayshow == "time":
						self.timer.start(1000, False) # start second timer
				else:
					Console().ePopen("fp_control -l 0 0") # red LED off
					self.timer.start(59998, False) # start minute timer
				self.record = False
				self.session.nav.record_event.remove(self.gotRecordEvent)

	def RecordEnd(self):
		if self.record:
			self.record = False
			self.session.nav.record_event.remove(self.gotRecordEvent)
			self.showTimer() #update timer icon

	def discOn(self):
		if config.plugins.vfdicon.showicons.value == "all":
			self.timer.stop() # stop minute timer
			Console().ePopen("fp_control -i 40 1 -i 39 1 -i 38 1 -i 41 1")
			self.disc = 1 #start rotating the display disc
			self.timer.start(2000, False) # start two second timer

	def discOff(self):
		if config.plugins.vfdicon.showicons.value == "all":
			self.timer.stop() # stop two second timer
			self.disc = 0 #stop rotating the display disc
			Console().ePopen("fp_control -i 40 0 -i 39 0 -i 38 0 -i 41 0")
			self.timer.start(60000, False) # start minute timer

	def __evTunedIn(self):
		self.tuned = True
		Console().ePopen("fp_control -i 42 0 -i 37 0 -i 29 0") #SAT, TER + Alert off
		if config.plugins.vfdicon.hddicons.value == "no":
			self.displayHddUsedOff()

	def __evTuneFailed(self):
		self.tuned = False
		if config.plugins.vfdicon.hddicons.value == "no":
			self.displayHddUsedOff()

	def timerEvent(self):
		global dot
		if self.standby == False:
			disptype = config.plugins.vfdicon.displayshow.value
		else:
			disptype = config.plugins.vfdicon.stbdisplayshow.value
			if self.VFD == False:
				if config.plugins.vfdicon.stbdisplayshow.value == "time":
					if dot == 0:
						dot = 1
					else:
						dot = 0
		if self.record == True and config.plugins.vfdicon.recredledon.value:
			Console().ePopen("fp_control -l 0 " + str(config.plugins.vfdicon.recredledon.value))
		self.writeDate(disptype)

	def writeDate(self, disp):
		if DisplayType == 8:
			if disp == "date" or disp == "day_date":
				tm = localtime()
				if disp == "day_date":
					date = strftime("%a", tm)[0:2] + strftime(" %d-%m", tm)
				else:
					date = strftime("%d-%m-%y", tm)
				evfd.getInstance().vfd_write_string(date[0:8])
		else:
			global dot
			if disp == "time" or disp == "date" or disp == "time_date" or disp == "day_date" or disp == "time_day_date":
				tm = localtime()
				time = strftime("%H%M", tm)
				date = strftime("%a", tm)[0:2] + strftime("%d-%m", tm) # day_date
				if disp == "time_day_date":
					date = time + date
				if disp == "date":
					date = strftime("%d%m-%y", tm)
				if disp == "time":
					date = strftime("%H.%M", tm)
					if self.standby == True and dot == 0:
						date = time
				Console().ePopen("fp_control -t " + date[0:8])
 
	def onLeaveStandby(self):
		if config.plugins.vfdicon.stbdisplayshow.value == "time":
			self.timer.stop() # stop second timer
			self.timer.start(59998, False) # start minute timer
			Console().ePopen("fp_control -l 0 0") #Red LED off
		self.standby = False
		global DisplayType
		if DisplayType == 8:
			evfd.getInstance().vfd_set_brightness(config.plugins.vfdicon.contrast.value)
			print "[VFD-Icons] set brightness", config.plugins.vfdicon.contrast.value
			self.timerEvent()
			Console().ePopen("fp_control -i 36 0 -l 0 0") #Standby & Red LED off
			if config.plugins.vfdicon.showicons.value == "all":
				global hddUsed
				hddUsed = -1 #force hdd display
				self.displayHddUsed()
				if self.usb == 1:
					Console().ePopen("fp_control -i 13 1") #USB
				else:
					Console().ePopen("fp_control -i 13 0")
			print "[VFD-Icons] set icons on Leave Standby"

	def onEnterStandby(self, configElement):
		from Screens.Standby import inStandby
		inStandby.onClose.append(self.onLeaveStandby)
		global DisplayType
		if DisplayType == 4:
			if config.plugins.vfdicon.standbyredledon.value:
				Console().ePopen("fp_control -l 0 1") #Red LED on
			stbdisplayshow = config.plugins.vfdicon.stbdisplayshow.value
			dot = 1
		if DisplayType == 8:
			if stbdisplayshow == "time" and self.record == False:
				self.timer.stop() # stop minute timer
				self.timer.start(1000, False) # start second timer
			Console().ePopen("fp_control -i 46 0") #clear all VFD icons
			Console().ePopen("fp_control -i 36 1") #Standby
			if config.plugins.vfdicon.stbdisplayshow.value == "nothing":
				evfd.getInstance().vfd_set_light(0)
#				Console().ePopen("fp_control -L 0")
			else:
				evfd.getInstance().vfd_set_brightness(config.plugins.vfdicon.stbcontrast.value)
			print "[VFD-Icons] set standby brightness", config.plugins.vfdicon.stbcontrast.value
		if stbdisplayshow == "time" or stbdisplayshow == "date" or stbdisplayshow == "day_date":
			self.writeDate(stbdisplayshow)
		else:
			evfd.getInstance().vfd_clear_string()
		self.standby = True
		print "[VFD-Icons] set display on Enter Standby"

	def hotplugCB(self, dev, media_state):
		if config.plugins.vfdicon.showicons.value == "all":
			if dev.__contains__('sda') or dev.__contains__('sdb') or dev.__contains__('sdc'):
#				if media_state == "add" or media_state == "change":
				if media_state == "add":
					Console().ePopen("fp_control -i 13 1")
					self.usb = 1
					if config.plugins.vfdicon.hddicons.value == "all mounts":
						self.displayHddUsedOff() # signal hot plug
						self.mount = None # force remount
						self.SetMount() # determine mount
						if self.firstmount == -1 and self.mount:
								self.firstmount = self.mount
						self.displayHddUsed() # and display size
				if media_state == "remove":
					Console().ePopen("fp_control -i 13 0")
					self.usb = 0
					if config.plugins.vfdicon.hddicons.value == "all mounts":
						if self.firstmount != -1:
							self.mount = self.firstmount
						else:
							self.mount = None
						if not self.mount:
							self.displayHddUsedOff()
						else:
							self.displayHddUsed() # and display size

	def SetMount(self):
		if config.plugins.vfdicon.hddicons.value == "all mounts":
			dir = config.usage.instantrec_path.value[:-1]
			if dir == "<default":
				dir = config.usage.default_path.value[:-1]
			if not self.mount or self.dir != dir:
				if not self.mount:
					self.dir = dir
#					print "[VFD-Icons] SetMount", dir
					self.mount = self.FindMountDir(dir)
				if not self.mount:
					self.mount = self.FindMountDir('/autofs/sdc1')
				if not self.mount:
					self.mount = self.FindMountDir('/autofs/sdb1')
				if not self.mount:
					self.mount = self.FindMountDir('/autofs/sda1')
				if not self.mount:
					self.mount = self.FindMountDir('/media/hdd')
				if not self.mount:
					self.mount = self.FindMountDir('/hdd')
		elif not self.mount:
			self.mount = self.FindMountDir('/media/hdd')
			if not self.mount:
				self.mount = self.FindMountDir('/hdd')

	def FindMountDir(self, dir):
		mounts = open("/proc/mounts", 'r')
		for line in mounts:
			result = line.strip().split()
			if result[1].startswith(dir):
				mounts.close()
				return result[1]
		mounts.close()
		return None

	def FindMountDev(self, dev):
		mounts = open("/proc/mounts", 'r')
		for line in mounts:
			result = line.strip().split()
			if result[0].startswith(dev):
				mounts.close()
				return result[1]
		mounts.close()
		return None

	def CheckUsed(self):
		if self.mount:
			try:
				f = statvfs(self.mount)
			except:
				print "statvfs failed"
				self.mount = None
				self.SetMount()
				if self.mount:
					try:
						f = statvfs(self.mount)
					except:
						self.mount = None
#			print "[CheckUsed] Mountpoint       :", self.mount
#			if self.mount != None:
#				print "[CheckUsed] Total blocks     :", f.f_blocks
#				print "[CheckUsed] Free blocks      :", f.f_bavail
#			if f.f_blocks != 0:
#				print "[CheckUsed] Free/Used space  :", f.f_bavail * 100 / f.f_blocks, "/", (f.f_blocks - f.f_bavail) * 100 / f.f_blocks, "%"
		if self.mount:
			if f.f_blocks == 0:
				return 0
			else:
				return (f.f_blocks - f.f_bavail) * 90 / f.f_blocks
		else:
			return 0

	def displayHddUsed(self):
		global hddUsed
		if config.plugins.vfdicon.showicons.value == "all":
			if config.plugins.vfdicon.hddicons.value != "no":
				if self.mount == None:
					self.displayHddUsedOff() #HDD display off
				else:
					used = self.CheckUsed()
					if hddUsed != used: # if previous size different 
						hddUsed = used # save current size
						Console().ePopen("fp_control -i 30 1") #HDD grid on
						self.showSize(used) #and show HDD
						print "[VFD-Icons] HDD mount point:", self.mount, ", used icons:", used/10
		else:
			self.displayHddUsedOff()

	def showSize(self, size):
		if size >= 10:
			Console().ePopen("fp_control -i 24 1") #HDD1
		else:
			Console().ePopen("fp_control -i 24 0")
		if size >= 20:
			Console().ePopen("fp_control -i 23 1") #HDD2
		else:
			Console().ePopen("fp_control -i 23 0")
		if size >= 30:
			Console().ePopen("fp_control -i 21 1") #HDD3
		else:
			Console().ePopen("fp_control -i 21 0")
		if size >= 40:
			Console().ePopen("fp_control -i 20 1") #HDD4
		else:
			Console().ePopen("fp_control -i 20 0")
		if size >= 50:
			Console().ePopen("fp_control -i 19 1") #HDD5
		else:
			Console().ePopen("fp_control -i 19 0")
		if size >= 60:
			Console().ePopen("fp_control -i 18 1") #HDD6
		else:
			Console().ePopen("fp_control -i 18 0")
		if size >= 70:
			Console().ePopen("fp_control -i 17 1") #HDD7
		else:
			Console().ePopen("fp_control -i 17 0")
		if size >= 80:
			Console().ePopen("fp_control -i 16 1") #HDD8
		else:
			Console().ePopen("fp_control -i 16 0")
		if config.plugins.vfdicon.hddicons.value != "no":
			if size < 87:
				Console().ePopen("fp_control -i 22 0 -i 29 0")
			else:
				Console().ePopen("fp_control -i 22 1 -i 29 1") #HDD full (+ Alert)

	def displayHddUsedOff(self): #switch off hdd display
		Console().ePopen("fp_control -i 16 0 -i 17 0 -i 18 0 -i 19 0 -i 20 0 -i 21 0 -i 23 0 -i 24 0 -i 30 0")
		if config.plugins.vfdicon.hddicons.value != "no":
			Console().ePopen("fp_control -i 22 0 -i 29 0") #HDD Full, Alert off

VFDIconsInstance = None

def main(session, **kwargs):
	global VFDIconsInstance
	global DisplayType
	if VFDIconsInstance is None:
		VFDIconsInstance = VFDIcons(session)
	if DisplayType == 4 or DisplayType == 8:
		displayshow = config.plugins.vfdicon.displayshow.value
		if displayshow == "time" or displayshow == "date" or displayshow == "day_date" or displayshow == "time_day_date":
			sleep(1)
			VFDIconsInstance.timerEvent()
		else:
			VFDIconsInstance.writeName()

def Plugins(**kwargs):
	l = [PluginDescriptor(
		name = _("Front panel display"),
		description = _("Front panel display configuration"),
		where = PluginDescriptor.WHERE_MENU,
		fnc = LEDdisplaymenu),
		PluginDescriptor(
		name = _("VFD-Icons"),
		description = _("Front panel display control Spark"),
		where = PluginDescriptor.WHERE_SESSIONSTART,
		fnc = main)]
	if config.plugins.vfdicon.extMenu.value:
		l.append(PluginDescriptor(
			name = _("Front panel display"),
			description = _("Front panel display configuration for Spark"),
			where = PluginDescriptor.WHERE_PLUGINMENU,
			icon = _("leddisplay.png"),
			fnc = opencfg))
	return l
