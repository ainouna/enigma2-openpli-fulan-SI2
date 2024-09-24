# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from ServiceReference import ServiceReference
from enigma import iPlayableService, eTimer, eServiceCenter, iServiceInformation, iRecordableService, eTimer, evfd, eDVBVolumecontrol, iFrontendInformation
from enigma import evfd
from time import localtime, strftime, sleep
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
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
import os
#Version 210807.1

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
	if DisplayType != 12:
		DisplayType = None
except:
	DisplayType = None
DisplayTypevfd = DisplayType

if DisplayTypevfd is None:
	if stb.lower() == 'ufs910' or stb.lower() == 'ufs912' or stb.lower() == 'ufs913' or stb.lower() == 'ufs922':
		DisplayType = 12
	else:
		DisplayType = None

config.plugins.vfdicon = ConfigSubsection()
config.plugins.vfdicon.displayshow = ConfigSelection(default = "channel",
	choices = [
		("nothing", _("blank")),
		("channel number", _("channel number")),
		("channel", _("channel name")),
		("channel namenumber", _("channel number and name")),
		("time", _("time")),
		("date", _("date")),
		("time_date", _("time and date")),
		("day_date", _("day and date"))
		])
config.plugins.vfdicon.stbshow = ConfigSelection(default = "time_date",
	choices = [
		("nothing", _("nothing")),
		("time", _("time")),
		("date", _("date")),
		("time_date", _("time and date")),
		("day_date", _("day and date"))
		])
config.plugins.vfdicon.contrast = ConfigSlider(default=4, limits=(0, 7))
config.plugins.vfdicon.stbcontrast = ConfigSlider(default=2, limits=(0, 7))
config.plugins.vfdicon.uppercase = ConfigYesNo(default=False)
config.plugins.vfdicon.textscroll = ConfigSelection(default = "1",
	choices = [
		("0", _("no")),
		("1", _("once")),
		("2", _("continuous"))
		])
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
config.plugins.vfdicon.standbyredledon = ConfigSlider(default=2, limits=(0, 7))
config.plugins.vfdicon.ledbright = ConfigSlider(default=5, limits=(0, 7))
config.plugins.vfdicon.fanspeed = ConfigSlider(default=4, limits=(0, 15))
config.plugins.vfdicon.extMenu = ConfigYesNo(default=True)

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
		self.setTitle(_("VFD display configuration"))
		self.createSetup()

	def createSetup(self):
		self.cfglist = []
		self.cfglist.append(getConfigListEntry(_("Show on VFD display"), config.plugins.vfdicon.displayshow))
		self.cfglist.append(getConfigListEntry(_("Show on VFD display in standby"), config.plugins.vfdicon.stbshow))
		if DisplayType == 12:
			self.cfglist.append(getConfigListEntry(_("VFD brightness"), config.plugins.vfdicon.contrast))
			self.cfglist.append(getConfigListEntry(_("Standby brightness"), config.plugins.vfdicon.stbcontrast))
		self.cfglist.append(getConfigListEntry(_("Uppercase letters only"), config.plugins.vfdicon.uppercase))
		self.cfglist.append(getConfigListEntry(_("Scroll text"), config.plugins.vfdicon.textscroll))
		self.cfglist.append(getConfigListEntry(_("Center text"), config.plugins.vfdicon.textcenter))
		self.cfglist.append(getConfigListEntry(_("Show icons"), config.plugins.vfdicon.showicons))
		self.icons_showicons = config.plugins.vfdicon.showicons.value
		self.cfglist.append(getConfigListEntry(_("Fan speed"), config.plugins.vfdicon.fanspeed))
		if DisplayType == 12:
			self.cfglist.append(getConfigListEntry(_('Stby LED brightness'), config.plugins.vfdicon.standbyredledon))
			self.cfglist.append(getConfigListEntry(_('LED brightness'), config.plugins.vfdicon.ledbright))
	        self.cfglist.append(getConfigListEntry(_('Show this plugin in plugin menu'), config.plugins.vfdicon.extMenu))
		self["config"].list = self.cfglist
		self["config"].l.setList(self.cfglist)

	def newConfig(self):
		global DisplayType
		if DisplayType == 12:
			if self["config"].getCurrent()[1] == config.plugins.vfdicon.stbcontrast:
				Console().ePopen("fp_control -b " + str(config.plugins.vfdicon.stbcontrast.value))
			elif self["config"].getCurrent()[1] == config.plugins.vfdicon.standbyredledon:
				Console().ePopen("fp_control -l 3 " + str(config.plugins.vfdicon.standbyredledon.value))
			else:
				Console().ePopen("fp_control -b " + str(config.plugins.vfdicon.contrast.value))
				print ""
				b = str(config.plugins.vfdicon.ledbright.value)
				Console().ePopen("fp_control -led" + b)
		if self["config"].getCurrent()[1] == config.plugins.vfdicon.fanspeed:
			Console().ePopen("fp_control -sf " + str(((config.plugins.vfdicon.fanspeed.value + 1) * 16) - 1))
		print "newConfig", self["config"].getCurrent()
		self.createSetup()

	def cancel(self):
		main(self)
		b = str(config.plugins.vfdicon.ledbright.value)
		Console().ePopen("fp_control -led" + b)
		ConfigListScreen.keyCancel(self)

	def keySave(self):
		global DisplayType
		if DisplayType == 12:
			print "[VFD-Icons] set LED brightness", config.plugins.vfdicon.ledbright.value
			b = str(config.plugins.vfdicon.ledbright.value)
			Console().ePopen("fp_control -led" + b)
			print "[VFD-Icons] set display brightness", config.plugins.vfdicon.contrast.value
			Console().ePopen("fp_control -b " + str(config.plugins.vfdicon.contrast.value))
		if config.plugins.vfdicon.textscroll.value is not None:
			evfd.getInstance().vfd_set_SCROLL(int(config.plugins.vfdicon.textscroll.value))
		else:
			evfd.getInstance().vfd_set_SCROLL(1)
		print "[VFD-Icons] set text scroll", config.plugins.vfdicon.textscroll.value
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
		evfd.getInstance().vfd_write_string( "VFD SETUP" )

def VFDdisplaymenu(menuid, **kwargs):
	if menuid == "expert":
		return [(_("VFD display"), opencfg, "vfd_display", 44)]
	else:
		return []

class VFDIcons:
	def __init__(self, session):
		self.session = session
		self.onClose = []
		print '[VFD-Icons] Start'
		self.play = False
		self.record = False
		self.standby = False
		self.usb = 0
		self.dolbyAvailable = False
		self.mp3Available = False
		self.DTSAvailable = False
		self.timer = eTimer()
		self.timer.callback.append(self.timerEvent)
		self.timer.start(4999, False) # start vife second timer
		Console().ePopen("fp_control -i 17 0")
		b = str(config.plugins.vfdicon.ledbright.value)
		Console().ePopen("fp_control -led" + b)
		global DisplayType
		print '[VFD-Icons] Hardware displaytype:', DisplayType
		print '[VFD-Icons] VFD displaytype     :', DisplayTypevfd
		if DisplayType == 12:
			self.__event_tracker = ServiceEventTracker(screen = self,eventmap =
				{
					iPlayableService.evUpdatedInfo: self.UpdatedInfo,
					iPlayableService.evUpdatedEventInfo: self.__evUpdatedEventInfo,
					iPlayableService.evVideoSizeChanged: self.__evVideoSizeChanged,
					iPlayableService.evSeekableStatusChanged: self.__evSeekableStatusChanged,
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
		print "[VFD-Icons] Set text centering option"
		if config.plugins.vfdicon.textcenter.value == "1":
			evfd.getInstance().vfd_set_CENTER(True)
		else:
			evfd.getInstance().vfd_set_CENTER(False)
		print '[VFD-Icons] End initialisation'

	def __evStart(self):
		print '[VFD-Icons] __evStart'
		self.__evSeekableStatusChanged()

	def __evUpdatedEventInfo(self):
		print '[VFD-Icons] __evUpdatedEventInfo'
#		... and do nothing else

	def UpdatedInfo(self):
		print '[VFD-Icons] __evUpdatedInfo'
		self.checkAudioTracks()
		self.writeName()
		self.showDTS()
		if DisplayType == 12:
			self.showCrypted()
			self.showDolby()
			self.showMP3()
			self.showMute()

	def writeName(self):
		if (config.plugins.vfdicon.displayshow.value != "date" and config.plugins.vfdicon.displayshow.value != "day_date"
			and config.plugins.vfdicon.displayshow.value != "time_date" and config.plugins.vfdicon.displayshow.value != "time"):
			servicename = "        "
			if config.plugins.vfdicon.displayshow.value != "nothing":
				service = self.session.nav.getCurrentlyPlayingServiceOrGroup()
				if service:
					path = service.getPath()
					if path:
						self.play = True
						servicename = "Play"
						currPlay = self.session.nav.getCurrentService()
						if currPlay != None and self.mp3Available: # show the MP3 tag
							servicename = currPlay.info().getInfoString(iServiceInformation.sTagTitle) + " - " + currPlay.info().getInfoString(iServiceInformation.sTagArtist)
							Console().ePopen("fp_control -i 7 1") #Radio icon on, TV off
						else: # show the file name
							Console().ePopen("fp_control -i 7 0") #Radio icon off
							self.service = self.session.nav.getCurrentlyPlayingServiceReference()
							if not self.service is None:
								service = self.service.toCompareString()
#								servicename = ServiceReference(service).getServiceName().replace('\xc2\x87', '').replace('\xc2\x86', '').ljust(63)
								servicename = ServiceReference(service).getServiceName().replace('\xc2\x87', '').replace('\xc2\x86', '')
						Console().ePopen("fp_control -i 11 1") #play, file
					else:
						if config.plugins.vfdicon.displayshow.value == "channel number": #show the channel number
							servicename = str(service.getChannelNum())
							if len(servicename) == 1:
								servicename = '000' + servicename
							elif len(servicename) == 2:
								servicename = '00' + servicename
							elif len(servicename) == 3:
								servicename = '0' + servicename
						elif config.plugins.vfdicon.displayshow.value == "channel namenumber": #show the channel number & name
							servicename = str(service.getChannelNum()) + ' ' + ServiceReference(service).getServiceName()
						else:
							servicename = ServiceReference(service).getServiceName() #show the channel name
						self.play = False
						Console().ePopen("fp_control -i 11 0") #play, file off
						#evaluate radio or tv
						if config.plugins.vfdicon.showicons.value == "all":
							if config.servicelist.lastmode.value == 'tv':
								Console().ePopen("fp_control -i 7 0") #Radio off
							else:
								Console().ePopen("fp_control -i 7 1") #Radio icon on
			if config.plugins.vfdicon.uppercase.value == True:
				servicename = servicename.upper()
			servicename = servicename.replace('  ', ' ')
			evfd.getInstance().vfd_write_string(servicename[0:63])

	def showCrypted(self):
		if config.plugins.vfdicon.showicons.value != "none":
			service = self.session.nav.getCurrentService()
			if service:
				info = service.info()
				crypted = info.getInfo(iServiceInformation.sIsCrypted)
				if crypted == 1:
					Console().ePopen("fp_control -i 4 1")
				else:
					Console().ePopen("fp_control -i 4 0")

	def checkAudioTracks(self):
		self.dolbyAvailable = False
		self.mp3Available = False
		self.DTSAvailable = False
		if config.plugins.vfdicon.showicons.value != "none":
			service = self.session.nav.getCurrentService()
			if service:
				audio = service.audioTracks()
				if audio:
					n = audio.getNumberOfTracks()
					for x in range(n):
						i = audio.getTrackInfo(x)
						description = i.getDescription();
						if description.find("AC3") != -1:
							self.dolbyAvailable = True
						if description.find("MP3") != -1:
							self.mp3Available = True
						if description.find("DTS") != -1:
							self.DTSAvailable = True

	def showDolby(self):
		if self.dolbyAvailable:
			Console().ePopen("fp_control -i 8 1") #Dolby
		else:
			Console().ePopen("fp_control -i 8 0")

	def showMP3(self):
		if self.mp3Available:
			Console().ePopen("fp_control -i 6 1") #MP3
		else:
			Console().ePopen("fp_control -i 6 0")

	def showDTS(self):
		if self.DTSAvailable:
			Console().ePopen("fp_control -i 8 1") #DTS (dolby)
		else:
			Console().ePopen("fp_control -i 8 0")

	def showMute(self):
		if config.plugins.vfdicon.showicons.value != "none":
			self.isMuted = eDVBVolumecontrol.getInstance().isMuted()
			if self.isMuted:
				Console().ePopen("fp_control -i 10 1") #Mute
			else:
				Console().ePopen("fp_control -i 10 0")

	def showTimer(self):
		if config.plugins.vfdicon.showicons.value == "all":
			# check if timers are set
			next_rec_time = -1
			next_rec_time = self.session.nav.RecordTimer.getNextRecordingTime()
			if next_rec_time > 0:
				Console().ePopen("fp_control -i 16 1") #Timer
			else:
				Console().ePopen("fp_control -i 16 0")

	def timerEvent(self):
		self.showTimer() #update timer icon
		if self.standby == False:
			self.showMute() #update mute icon
		if self.record == False:
	 		if self.standby == False:
				disptype = config.plugins.vfdicon.displayshow.value
			else:
				disptype = config.plugins.vfdicon.stbshow.value
			self.writeDate(disptype)

	def __evUpdatedEventInfo(self):
		print "[__evUpdatedEventInfo]"

	def getSeekState(self):
		service = self.session.nav.getCurrentService()
		if service is None:
			return False
		seek = service.seek()
		if seek is None:
			return False
		return seek.isCurrentlySeekable()

	def __evSeekableStatusChanged(self):
		print "[__evSeekableStatusChanged]"
		if self.getSeekState():
			evfd.getInstance().vfd_set_icon(11, True)
		else:
			evfd.getInstance().vfd_set_icon(11, False)

	def __evVideoSizeChanged(self):
		if config.plugins.vfdicon.showicons.value != "none":
			service = self.session.nav.getCurrentService()
		if service:
			info=service.info()
			height = info.getInfo(iServiceInformation.sVideoHeight)
			if height > 576 : #set HD symbol
				evfd.getInstance().vfd_set_icon(2, True)
			else:
				evfd.getInstance().vfd_set_icon(2, False)

	def gotRecordEvent(self, service, event):
		if config.plugins.vfdicon.showicons.value != 'none':
			if event in (iRecordableService.evEnd, iRecordableService.evStart, None):
				recs = self.session.nav.getRecordings()
				nrecs = len(recs)
				if nrecs > 0: #recording active
					self.record = True
					evfd.getInstance().vfd_set_icon(15, True)
				else:
					evfd.getInstance().vfd_set_icon(15, False)
					self.RecordEnd()

	def RecordEnd(self):
		if self.record:
			self.record = False
			self.session.nav.record_event.remove(self.gotRecordEvent)
			self.showTimer() #update timer icon

	def writeDate(self, disp): #TODO: replace with case
		if disp == "date" or disp == "day_date" or disp == "time" or disp == "time_date" or disp == "nothing":
			tm = localtime()
			if disp == "day_date":
				date = strftime("%a", tm) + strftime(" %d-%m-%Y", tm)
			elif disp == "date":
				date = strftime("%d %b %Y", tm) 
			elif disp == "time_date":
				date = strftime("%d %b %H:%M:%S", tm) 
			elif disp == "time":
				date = strftime("      %H:%M:%S", tm)
			elif disp == "nothing":
				date = "            "
			evfd.getInstance().vfd_write_string(date[0:16])

	def onLeaveStandby(self):
		self.standby = False
		global DisplayType
		if stb.lower() == 'ufs922':
			Console().ePopen("fp_control -l 3 0") # standby LED off
		self.timer.stop() # stop one second timer
		evfd.getInstance().vfd_write_string("                ")
		self.timer.start(4999, False) # start five second timer
		print "[VFD-Icons] minute timer started"
		if DisplayType == 12:
			evfd.getInstance().vfd_set_brightness(config.plugins.vfdicon.contrast.value)
			print "[VFD-Icons] set brightness", config.plugins.vfdicon.contrast.value
			self.timerEvent()
			b = str(config.plugins.vfdicon.ledbright.value)
			Console().ePopen("fp_control -led" + b)
			if config.plugins.vfdicon.showicons.value == "all":
				global hddUsed
				hddUsed = -1 #force hdd display
				self.displayHddUsed()
				if self.usb == 1:
					Console().ePopen("fp_control -i 1 1") #USB
				else:
					Console().ePopen("fp_control -i 1 0")
			print "[VFD-Icons] set icons on Leave Standby"

	def onEnterStandby(self, configElement):
		from Screens.Standby import inStandby
		inStandby.onClose.append(self.onLeaveStandby)
		global DisplayType
		if DisplayType == 12:
			Console().ePopen("fp_control -i 17 0") #clear all VFD icons
			print "[VFD-Icons] set display & icons on Enter Standby"
			if config.plugins.vfdicon.stbshow.value == "nothing":
				evfd.getInstance().vfd_set_light(0)
			else:
				evfd.getInstance().vfd_set_brightness(config.plugins.vfdicon.stbcontrast.value)
			print "[VFD-Icons] set standby brightness", config.plugins.vfdicon.stbcontrast.value
			if config.plugins.vfdicon.standbyredledon.value and stb.lower() == 'ufs922':
				Console().ePopen("fp_control -l 3 " + str(config.plugins.vfdicon.standbyredledon.value)) #Red LED on
		if (config.plugins.vfdicon.stbshow.value == "time" or config.plugins.vfdicon.stbshow.value == "time_date"):
			self.timer.stop() # stop minute timer
			self.timer.start(999, False) # start one second timer
			print "[VFD-Icons] second timer started"
		if (config.plugins.vfdicon.stbshow.value == "date" or config.plugins.vfdicon.stbshow.value == "day_date" or config.plugins.vfdicon.stbshow.value == "time" or config.plugins.vfdicon.stbshow.value == "time_date"):
			self.writeDate(config.plugins.vfdicon.stbshow.value)
		else:
			evfd.getInstance().vfd_clear_string()
		self.standby = True

	def hotplugCB(self, dev, media_state):
		if config.plugins.vfdicon.showicons.value == "all":
			if dev.__contains__('sdb') or dev.__contains__('sdc'):
#				if media_state == "add" or media_state == "change":
				if media_state == "add":
					Console().ePopen("fp_control -i 1 1") #USB
					self.usb = 1
					self.mount = None # force remount
					self.SetMount() # determine mount
					if self.firstmount == -1 and self.mount:
						self.firstmount = self.mount
					self.displayHddUsed() # and display icon
				if media_state == "remove":
					Console().ePopen("fp_control -i 1 0") #USB
					self.usb = 0
					if self.firstmount != -1:
						self.mount = self.firstmount
					else:
						self.mount = None
					self.displayHddUsed() # and display icon

	def SetMount(self):
		dir = config.usage.instantrec_path.value[:-1]
		if dir == "<default":
			dir = config.usage.default_path.value[:-1]
		if not self.mount or self.dir != dir:
			if not self.mount:
				self.dir = dir
#				print "[VFD-Icons] SetMount", dir
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

	def FindMountDir(self, dir):
		mounts = open("/proc/mounts", 'r')
		for line in mounts:
			result = line.strip().split()
			if result[1].startswith(dir):
				mounts.close()
				return result[1]
		mounts.close()
		return None

	def displayHddUsed(self):
		global hddUsed
		if config.plugins.vfdicon.showicons.value == "all":
			if self.mount == None:
				Console().ePopen("fp_control -i 3 0")
			else:
				Console().ePopen("fp_control -i 3 1") #HDD on
				print "[VFD-Icons] HDD mount point:", self.mount
		else:
			self.displayHddUsedOff()

VFDIconsInstance = None

def main(session, **kwargs):
	# Create Instance if none present, show Dialog afterwards
	global VFDIconsInstance
	if VFDIconsInstance is None:
		VFDIconsInstance = VFDIcons(session)

def Plugins(**kwargs):
	l = [PluginDescriptor(
		name = _("VFD display"),
		description = _("VFD display configuration"),
		where = PluginDescriptor.WHERE_MENU,
		fnc = VFDdisplaymenu),
		PluginDescriptor(
		name = _("VFD-Icons"),
		description = _("VFD-Icons for Kathrein UFS9XX"),
		where = PluginDescriptor.WHERE_SESSIONSTART,
		fnc = main)]
	if config.plugins.vfdicon.extMenu.value:
		l.append(PluginDescriptor(
			name = _("VFD display"),
			description = _("VFD configuration for Kathrein UFS9XX"),
			where = PluginDescriptor.WHERE_PLUGINMENU,
			icon = _("vfddisplay.png"),
			fnc = opencfg))
	return l
