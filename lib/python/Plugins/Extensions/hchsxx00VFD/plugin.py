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
import os
#Version 221202.1
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
	if DisplayType != 22:
		DisplayType = None
except:
	DisplayType = None
DisplayTypevfd = DisplayType

if DisplayTypevfd is None:
	if stb.lower() == 'hchs8100' or stb.lower() == 'hchs9000':
		DisplayType = 22
	else:
		DisplayType = None

config.plugins.vfdicon = ConfigSubsection()
config.plugins.vfdicon.displayshow = ConfigSelection(default = "channel",
	choices = [
		("nothing", _("blank")),
		("channel number", _("channel number")),
		("channel", _("channel name")),
		("channel namenumber", _("channel number and name")),
		("date", _("date")),
		("day_date", _("day and date"))
		])
config.plugins.vfdicon.stbdisplayshow = ConfigSelection(default = "day_date",
	choices = [
		("nothing", _("nothing")),
		("blank", _("time")),
		("date", _("time and date")),
		("day_date", _("time, day and date"))
		])
config.plugins.vfdicon.contrast = ConfigSlider(default=5, limits=(0, 7))
config.plugins.vfdicon.stbcontrast = ConfigSlider(default=3, limits=(0, 7))
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
config.plugins.vfdicon.hddicons = ConfigSelection(default = "hdd",
	choices = [
		("no", _("signal quality")),
		("hdd", _("on hdd")),
		("all mounts", _("on all mounts"))
		])
config.plugins.vfdicon.standbyredledon = ConfigYesNo(default=False)
config.plugins.vfdicon.dstandbyredledon = ConfigYesNo(default=False)
config.plugins.vfdicon.recredledon = ConfigSelection(default = "0",
	choices = [
		("0", _("off")),
		("1", _("on")),
		("2", _("blink"))
		])
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
		self.cfglist.append(getConfigListEntry(_("Show on VFD display in standby"), config.plugins.vfdicon.stbdisplayshow))
		if DisplayType == 22:
			self.cfglist.append(getConfigListEntry(_("VFD brightness"), config.plugins.vfdicon.contrast))
			self.cfglist.append(getConfigListEntry(_("Standby brightness"), config.plugins.vfdicon.stbcontrast))
		self.cfglist.append(getConfigListEntry(_("Uppercase letters only"), config.plugins.vfdicon.uppercase))
		self.cfglist.append(getConfigListEntry(_("Scroll text"), config.plugins.vfdicon.textscroll))
		self.cfglist.append(getConfigListEntry(_("Center text"), config.plugins.vfdicon.textcenter))
		self.cfglist.append(getConfigListEntry(_("Show icons"), config.plugins.vfdicon.showicons))
		self.icons_showicons = config.plugins.vfdicon.showicons.value
		if self.icons_showicons == "all":
			self.cfglist.append(getConfigListEntry(_("Show HDD icons"), config.plugins.vfdicon.hddicons))
	        self.cfglist.append(getConfigListEntry(_('Show this plugin in plugin menu'), config.plugins.vfdicon.extMenu))
		self["config"].list = self.cfglist
		self["config"].l.setList(self.cfglist)

	def newConfig(self):
		global DisplayType
		if DisplayType == 22:
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
		if DisplayType == 22:
			Console().ePopen("fp_control -b " + str(config.plugins.vfdicon.contrast.value))
			print "[VFD-Icons] set brightness", config.plugins.vfdicon.contrast.value
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
		self.timeshift = False
		self.disc = 0
		self.standby = False
		self.usb = 0
		self.mp3Available = False
		self.dolbyAvailable = False
		self.DTSAvailable = False
		self.timer = eTimer()
		self.timer.callback.append(self.timerEvent)
		self.timer.start(60000, False) # start one minute timer
		global DisplayType
		global hddUsed
		print '[VFD-Icons] Hardware displaytype:', DisplayType
		print '[VFD-Icons] VFD displaytype     :', DisplayTypevfd
		if DisplayType == 22:
			self.__event_tracker = ServiceEventTracker(screen = self,eventmap =
				{
					iPlayableService.evUpdatedInfo: self.UpdatedInfo,
					iPlayableService.evUpdatedEventInfo: self.__evUpdatedEventInfo,
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
		print "[VFD_Icons] Set text centering option"
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
		if DisplayType == 22:
			self.showDolby()

	def writeName(self):
		if config.plugins.vfdicon.displayshow.value != "date" and config.plugins.vfdicon.displayshow.value != "day_date":
			servicename = "        "
			if config.plugins.vfdicon.displayshow.value != "nothing":
				service = self.session.nav.getCurrentlyPlayingServiceOrGroup()
				if service:
					path = service.getPath()
					if path:
						self.play = True
						servicename = "PLAY"
						currPlay = self.session.nav.getCurrentService()
						if currPlay != None and self.mp3Available: # show the MP3 tag
							servicename = currPlay.info().getInfoString(iServiceInformation.sTagTitle) + " - " + currPlay.info().getInfoString(iServiceInformation.sTagArtist)
							Console().ePopen("fp_control -i 20 1 -i 19 0") # Radio icon on, TV off
						else: # show the file name
							self.service = self.session.nav.getCurrentlyPlayingServiceReference()
							if not self.service is None:
								service = self.service.toCompareString()
								servicename = ServiceReference(service).getServiceName().replace('\xc2\x87', '').replace('\xc2\x86', '').ljust(16)
								Console().ePopen("fp_control -i 19 1 -i 20 0") # TV icon on, Radio off
						if config.plugins.vfdicon.hddicons.value == "no":
							self.displayHddUsedOff() #switch off signal strength						
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
						#evaluate radio or tv
						if config.plugins.vfdicon.showicons.value == "all":
							if config.servicelist.lastmode.value == 'tv':
								Console().ePopen("fp_control -i 19 1 -i 20 0") # TV icon on, Radio off
							else:
								Console().ePopen("fp_control -i 20 1 -i 19 0") # Radio icon on, TV off
			if config.plugins.vfdicon.uppercase.value == "true":
				servicename = servicename.upper()
			evfd.getInstance().vfd_write_string(servicename[0:63])
			if config.plugins.vfdicon.showicons.value == "all":
				if config.plugins.vfdicon.hddicons.value != "no":
					global hddUsed
					hddUsed = -1  #force hdd display
					self.displayHddUsed()

	def checkAudioTracks(self):
		self.mp3Available = False
		self.dolbyAvailable = False
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
						if description.find("MP3") != -1:
							self.mp3Available = True
						if description.find("AC3") != -1:
							self.dolbyAvailable = True
						if description.find("DTS") != -1:
							self.DTSAvailable = True

	def showDolby(self):
		if self.dolbyAvailable:
			Console().ePopen("fp_control -i 21 1") # Dolby
		else:
			Console().ePopen("fp_control -i 21 0")

	def showSignal(self):
		if (config.plugins.vfdicon.hddicons.value == "no" and config.plugins.vfdicon.showicons.value == "all" and self.play == False and self.standby == False):
			Console().ePopen("fp_control -i 24 0") # HDD grid off
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
				Console().ePopen("fp_control -i 23 1") # Timer
			else:
				Console().ePopen("fp_control -i 23 0")

	def timerEvent(self):
		if self.standby == False:
			self.showSignal()
			self.showTimer() #update timer icon
			if config.plugins.vfdicon.showicons.value == "all":
				if (self.record == True or self.timeshift == True): # if recording or timeshifting, display a rotating disc
					self.displayHddUsed() # update HDD display
					Console().ePopen("fp_control -i 36 1") # Spinner
		if self.record == False and self.timeshift == False:
	 		if self.standby == False:
				disptype = config.plugins.vfdicon.displayshow.value
			else:
				disptype = config.plugins.vfdicon.stbdisplayshow.value
			self.writeDate(disptype)

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
							Console().ePopen("fp_control -i 36 1") # Spinner
						else:
							self.timeshift = False
							if self.record == False:
								Console().ePopen("fp_control -i 36 0") # Spinner

	def gotRecordEvent(self, service, event):
		if config.plugins.vfdicon.showicons.value != 'none':
			if event in (iRecordableService.evEnd, iRecordableService.evStart, None):
				recs = self.session.nav.getRecordings()
				nrecs = len(recs)
				if nrecs > 0: #one recording active
					self.record = True
					Console().ePopen("fp_control -i 18 1") # REC on
#					self.discOn()
				else: # no recording active
					Console().ePopen("fp_control -i 18 0") # REC off
#					if self.timeshift == False:
#						self.discOff()
					self.RecordEnd()

	def RecordEnd(self):
		if self.record:
			self.record = False
			self.session.nav.record_event.remove(self.gotRecordEvent)
			self.showTimer() #update timer icon

	def discOn(self):
		if config.plugins.vfdicon.showicons.value == "all":
#			self.timer.stop() # stop minute timer
			Console().ePopen("fp_control -i 36 1") # Spinner on
#			self.timer.start(2000, False) # start two second timer

	def discOff(self):
		if config.plugins.vfdicon.showicons.value == "all":
#			self.timer.stop() # stop two second timer
			Console().ePopen("fp_control -i 36 0") #spinner off
#			self.timer.start(60000, False) # start minute timer

	def writeDate(self, disp):
		if disp == "date" or disp == "day_date":
			tm = localtime()
			if disp == "day_date":
				date = strftime("%a", tm)[0:2] + strftime(" %d-%m", tm)
			else:
				date = strftime("%d-%m-%y", tm)
			evfd.getInstance().vfd_write_string(date[0:8])

	def onLeaveStandby(self):
		self.standby = False
		global DisplayType
		if DisplayType == 22:
			evfd.getInstance().vfd_set_brightness(config.plugins.vfdicon.contrast.value)
			print "[VFD-Icons] set brightness", config.plugins.vfdicon.contrast.value
			self.timerEvent()
			Console().ePopen("fp_control -i 22 0") # Standby
			if config.plugins.vfdicon.showicons.value == "all":
				global hddUsed
				hddUsed = -1  #force hdd display
				self.displayHddUsed()
			print "[VFD-Icons] set icons on Leave Standby"

	def onEnterStandby(self, configElement):
		from Screens.Standby import inStandby
		inStandby.onClose.append(self.onLeaveStandby)
		global DisplayType
		if DisplayType == 8:
			Console().ePopen("fp_control -i 35 0") #clear all VFD icons
			Console().ePopen("fp_control -i 22 1") #Standby
			if config.plugins.vfdicon.stbdisplayshow.value == "nothing":
				evfd.getInstance().vfd_set_light(0)
			else:
				evfd.getInstance().vfd_set_brightness(config.plugins.vfdicon.stbcontrast.value)
			print "[VFD-Icons] set standby brightness", config.plugins.vfdicon.stbcontrast.value
		if config.plugins.vfdicon.stbdisplayshow.value == "date" or config.plugins.vfdicon.stbdisplayshow.value == "day_date":
			self.writeDate(config.plugins.vfdicon.stbdisplayshow.value)
		else:
			evfd.getInstance().vfd_clear_string()
		self.standby = True
		print "[VFD-Icons] set display & icons on Enter Standby"

	def hotplugCB(self, dev, media_state):
		if config.plugins.vfdicon.showicons.value == "all":
			if dev.__contains__('sda') or dev.__contains__('sdb') or dev.__contains__('sdc'):
#				if media_state == "add" or media_state == "change":
				if media_state == "add":
					self.usb = 1
					if config.plugins.vfdicon.hddicons.value == "all mounts":
						self.displayHddUsedOff() # signal hot plug
						self.mount = None # force remount
						self.SetMount() # determine mount
						if self.firstmount == -1 and self.mount:
							self.firstmount = self.mount
						self.displayHddUsed() # and display size
				if media_state == "remove":
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
				print "[VFD-Icons] HDD free space:", 100 - ((f.f_blocks - f.f_bavail) * 100 / f.f_blocks), "%"
				return (f.f_blocks - f.f_bavail) * 100 / f.f_blocks
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
						Console().ePopen("fp_control -i 24 1")  #HDD frame on
						self.showSize(used)  #and show HDD
						print "[VFD-Icons] HDD mount point:", self.mount, ", used icons:", used/10
		else:
			self.displayHddUsedOff()

	def showSize(self, size):
		if size >= 5:
			Console().ePopen("fp_control -i 25 1")  #HDD1
		else:
			Console().ePopen("fp_control -i 25 0")
		if size >= 15:
			Console().ePopen("fp_control -i 26 1")  #HDD2
		else:
			Console().ePopen("fp_control -i 26 0")
		if size >= 25:
			Console().ePopen("fp_control -i 27 1")  #HDD3
		else:
			Console().ePopen("fp_control -i 27 0")
		if size >= 35:
			Console().ePopen("fp_control -i 28 1")  #HDD4
		else:
			Console().ePopen("fp_control -i 28 0")
		if size >= 45:
			Console().ePopen("fp_control -i 29 1")  #HDD5
		else:
			Console().ePopen("fp_control -i 29 0")
		if size >= 55:
			Console().ePopen("fp_control -i 30 1")  #HDD6
		else:
			Console().ePopen("fp_control -i 30 0")
		if size >= 65:
			Console().ePopen("fp_control -i 31 1")  #HDD7
		else:
			Console().ePopen("fp_control -i 31 0")
		if size >= 75:
			Console().ePopen("fp_control -i 32 1")  #HDD8
		else:
			Console().ePopen("fp_control -i 32 0")
		if size >= 85:
			Console().ePopen("fp_control -i 33 1")  #HDD9
		else:
			Console().ePopen("fp_control -i 33 0")
		if size >= 95:
			Console().ePopen("fp_control -i 34 1")  #HDDA
		else:
			Console().ePopen("fp_control -i 34 0")

	def displayHddUsedOff(self): #switch off hdd display
		Console().ePopen("fp_control -i 34 0 -i 33 0 -i 32 0 -i 31 0 -i 30 0 -i 29 0 -i 28 0 -i 27 0 -i 26 0 -i 25 0 -i 24 0")

VFDIconsInstance = None

def main(session, **kwargs):
	global VFDIconsInstance
	global DisplayType
	global hddUsed
	if VFDIconsInstance is None:
		VFDIconsInstance = VFDIcons(session)
	if DisplayType == 22:
		if config.plugins.vfdicon.displayshow.value == "date" or config.plugins.vfdicon.displayshow.value == "day_date":
			sleep(1)
			VFDIconsInstance.timerEvent()
		else:
			if config.plugins.vfdicon.showicons.value == "none":
				Console().ePopen("fp_control -i 35 0")		
			elif config.plugins.vfdicon.hddicons.value != "no":
				hddUsed = -1
				VFDIconsInstance.displayHddUsed()
		VFDIconsInstance.UpdatedInfo()
	else:
		VFDIconsInstance.writeName()

def Plugins(**kwargs):
	l = [PluginDescriptor(
		name = _("VFD display"),
		description = _("VFD display configuration"),
		where = PluginDescriptor.WHERE_MENU,
		fnc = VFDdisplaymenu),
		PluginDescriptor(
		name = _("VFD-Icons"),
		description = _("VFD-Icons for Homecast HS8100/9000"),
		where = PluginDescriptor.WHERE_SESSIONSTART,
		fnc = main)]
	if config.plugins.vfdicon.extMenu.value:
		l.append(PluginDescriptor(
			name = _("VFD display"),
			description = _("VFD display configuration for Homecast HS8100/9000"),
			where = PluginDescriptor.WHERE_PLUGINMENU,
			icon = _("vfddisplay.png"),
			fnc = opencfg))
	return l
