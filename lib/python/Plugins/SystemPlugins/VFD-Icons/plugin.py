# -*- coding: utf-8 -*-
from translit import translify

from Components.ActionMap import ActionMap
from Components.config import config, ConfigSlider, ConfigSubsection, \
	getConfigListEntry, ConfigSelection
from Components.ConfigList import ConfigListScreen
from Components.ServiceEventTracker import ServiceEventTracker
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Tools.Directories import fileExists

from ServiceReference import ServiceReference
from enigma import iPlayableService, iServiceInformation, iRecordableService, \
	eDVBVolumecontrol, eTimer, evfd

from os import statvfs
from time import localtime, strftime, sleep

try:
	DisplayType = evfd.getInstance().getVfdType()
	print "[VFD Display] DisplayType", DisplayType
	if DisplayType != 8:
		DisplayType = None
except:
	DisplayType = None

config.plugins.vfdicon = ConfigSubsection()
config.plugins.vfdicon.displayshow = ConfigSelection(default = "channel",
	choices = [("channel", _("channel")), ("channel number",
		_("channel number")), ("clock", _("clock")), ("blank", _("blank"))])
config.plugins.vfdicon.stbdisplayshow = ConfigSelection(default = "clock",
	choices = [("clock", _("clock")), ("blank", _("blank"))])
if DisplayType:
	config.plugins.vfdicon.contrast = ConfigSlider(default=6, limits=(0, 7))
	config.plugins.vfdicon.stbcontrast = ConfigSlider(default=2, limits=(0, 7))
	config.plugins.vfdicon.hddicons = ConfigSelection(default = "hdd",
		choices = [("hdd", _("hdd")), ("all mounts", _("all mounts"))])

class ConfigVFDDisplay(Screen, ConfigListScreen):
	def __init__(self, session):
		global DisplayType
		Screen.__init__(self, session)
		self.skinName = ["Setup"]
		self.setTitle(_("VFD display configuration"))
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.keySave,
				"green": self.keySave,
				"red": self.cancel,
			}, -2)
		cfglist = []
		cfglist.append(getConfigListEntry(_("Show on VFD display"),
			config.plugins.vfdicon.displayshow))
		cfglist.append(getConfigListEntry(_("Show on VFD in standby"),
			config.plugins.vfdicon.stbdisplayshow))
		if DisplayType:
			cfglist.append(getConfigListEntry(_("VFD brightness"),
				config.plugins.vfdicon.contrast))
			cfglist.append(getConfigListEntry(_("VFD in standby"),
				config.plugins.vfdicon.stbcontrast))
			cfglist.append(getConfigListEntry(_("Show on hdd icons"),
				config.plugins.vfdicon.hddicons))
		ConfigListScreen.__init__(self, cfglist)

	def cancel(self):
		main(self)
		ConfigListScreen.keyCancel(self)

	def keySave(self):
		if DisplayType:
			evfd.getInstance().vfd_set_brightness(config.plugins.vfdicon.contrast.value)
			print "[VFD Display] set brightness", config.plugins.vfdicon.contrast.value
		main(self)
		ConfigListScreen.keySave(self)

def opencfg(session, **kwargs):
		session.open(ConfigVFDDisplay)
		evfd.getInstance().vfd_write_string( "VFD SETUP" )

def VFDdisplay(menuid, **kwargs):
	if menuid == "system":
		return [(_("VFD Display"), opencfg, "vfd_display", 44)]
	else:
		return []

class VFDIcons:
	def __init__(self, session):
		global DisplayType
		self.session = session
		self.onClose = []
		self.timer = eTimer()
		self.timer.callback.append(self.timerEvent)
		if DisplayType:
			self.record = False
			self.dir = None
			self.mount = None
			self.usb = 0
			self.hddUsed = 0
			self.isMuted = 0
			self.__event_tracker = ServiceEventTracker(screen = self,eventmap =
				{
					iPlayableService.evUpdatedInfo: self.UpdatedInfo,
					iPlayableService.evVideoSizeChanged: self.__evVideoSizeChanged,
					iPlayableService.evSeekableStatusChanged: self.__evSeekableStatusChanged,
					iPlayableService.evTunedIn: self.__evTunedIn,
					iPlayableService.evTuneFailed: self.__evTuneFailed,
				})
			config.misc.standbyCounter.addNotifier(self.onEnterStandby,
				initial_call = False)
			session.nav.record_event.append(self.gotRecordEvent)
			try:
				from Plugins.SystemPlugins.Hotplug.plugin import hotplugNotifier
				hotplugNotifier.append(self.hotplugCB)
			except:
				pass
		else:
			self.__event_tracker = ServiceEventTracker(screen = self,eventmap =
				{
					iPlayableService.evStart: self.WriteName,
				})

	def UpdatedInfo(self):
		self.WriteName()
		self.showIcons()

	def WriteName(self):
		if config.plugins.vfdicon.displayshow.value != "clock":
			servicename = "        "
			if config.plugins.vfdicon.displayshow.value != "blank":
				service = self.session.nav.getCurrentlyPlayingServiceOrGroup()
				if service:
					path = service.getPath()
					if path:
						servicename = "PLAY"
					else:
						if config.plugins.vfdicon.displayshow.value == "channel number":
							servicename = str(service.getChannelNum())
						else:
							servicename = ServiceReference(service).getServiceName()
							if not DisplayType:
								servicename = translify(servicename)
			print "[VFD Display] text ", servicename[0:20]
			evfd.getInstance().vfd_write_string(servicename[0:20])

	def timerEvent(self):
		if config.plugins.vfdicon.displayshow.value == "clock" or DisplayType:
			tm = localtime()
			if DisplayType:
				self.displayHddUsed()
			if config.plugins.vfdicon.displayshow.value == "clock":
				servicename = strftime("%H%M", tm)
				evfd.getInstance().vfd_write_string(servicename[0:4])
			self.timer.startLongTimer(60-tm.tm_sec)

	def __evVideoSizeChanged(self):
		service = self.session.nav.getCurrentService()
		if service:
			info = service.info()
			height = info.getInfo(iServiceInformation.sVideoHeight)
			if height > 576: #set HD symbol
				evfd.getInstance().vfd_set_icon(14, True)
				print "[VFD Display] Set HD icon"
			else:
				evfd.getInstance().vfd_set_icon(14, False)
				print "[VFD Display] Disable HD icon"

	def __evSeekableStatusChanged(self):
		service = self.session.nav.getCurrentService()
		if service:
			seek = service.seek()
			if seek:
				evfd.getInstance().vfd_set_icon(43, True)
				print "[VFD Display] Set Timeshift icon"
			else:
				evfd.getInstance().vfd_set_icon(43, False)
				print "[VFD Display] Disable Timeshift icon"

	def __evTunedIn(self):
		print "[VFD Display] Set Tuned icon"
		evfd.getInstance().vfd_set_icon(44, True)
		evfd.getInstance().vfd_set_icon(29, False)

	def __evTuneFailed(self):
		print "[VFD Display] Tune Failed disable icons"
		evfd.getInstance().vfd_set_icon(44, False)
		evfd.getInstance().vfd_set_icon(14, False)
		evfd.getInstance().vfd_set_icon(43, False)
		evfd.getInstance().vfd_set_icon(29, True)
		evfd.getInstance().vfd_set_icon(25, False)
		evfd.getInstance().vfd_set_icon(26, False)
		evfd.getInstance().vfd_set_icon(42, False)
		evfd.getInstance().vfd_set_icon(37, False)
		evfd.getInstance().vfd_set_icon(45, False)

	def showIcons(self):
		service = self.session.nav.getCurrentService()
		if service:
			info = service.info()
			crypted = info.getInfo(iServiceInformation.sIsCrypted)
			if crypted == 1:
				evfd.getInstance().vfd_set_icon(11, True)
				print "[VFD Display] Set crypt icon"
			else:
				evfd.getInstance().vfd_set_icon(11, False)
				print "[VFD Display] Disable crypt icon"
			audio = service.audioTracks()
			if audio:
				try:
					n = audio.getNumberOfTracks()
					for x in range(n):
						i = audio.getTrackInfo(x)
						description = i.getDescription();
						if "MP3" in description:
							evfd.getInstance().vfd_set_icon(25, True)
							print "[VFD Display] Set MP3 icon"
						else:
							evfd.getInstance().vfd_set_icon(25, False)
							print "[VFD Display] Disable MP3 icon"
						if "AC3" in description:
							evfd.getInstance().vfd_set_icon(26, True)
							print "[VFD Display] Set AC3 icon"
						else:
							evfd.getInstance().vfd_set_icon(26, False)
							print "[VFD Display] Disable AC3 icon"
						if "DTS" in description:
							evfd.getInstance().vfd_set_icon(10, True)
							print "[VFD Display] Set DTS icon"
						else:
							evfd.getInstance().vfd_set_icon(10, False)
							print "[VFD Display] Disable DTS icon"
				except:
					evfd.getInstance().vfd_set_icon(26, False)
					evfd.getInstance().vfd_set_icon(25, False)
					evfd.getInstance().vfd_set_icon(10, False)
					print "[VFD Display] Disable audio icons on error"

	def onLeaveStandby(self):
		evfd.getInstance().vfd_set_brightness(config.plugins.vfdicon.contrast.value)
		print "[VFD Display] set brightness", config.plugins.vfdicon.contrast.value
		self.mount = None
		self.hddUsed = 0
		self.timerEvent()
		evfd.getInstance().vfd_set_icon(16, False)
		evfd.getInstance().vfd_set_icon(36, False)
		evfd.getInstance().vfd_set_icon(13, self.usb)
		print "[VFD Display] set icons on Leave Standby"

	def onEnterStandby(self, configElement):
		from Screens.Standby import inStandby
		inStandby.onClose.append(self.onLeaveStandby)
		self.timer.stop()
		evfd.getInstance().vfd_set_brightness(config.plugins.vfdicon.stbcontrast.value)
		print "[VFD Display] set brightness", config.plugins.vfdicon.stbcontrast.value
		evfd.getInstance().vfd_clear_icons()
		evfd.getInstance().vfd_set_icon(36, True)
		if config.plugins.vfdicon.stbdisplayshow.value == "blank":
			evfd.getInstance().vfd_clear_string()
		print "[VFD Display] set icons on Enter Standby"

	def gotRecordEvent(self, service, event):
		if event in (iRecordableService.evEnd, iRecordableService.evStart, None):
			recs = len(self.session.nav.getRecordings())
			if recs > 0:
				self.record = True
				evfd.getInstance().vfd_set_icon(7, True)
				print "[VFD Display] Set Rec icon"
			else:
				evfd.getInstance().vfd_set_icon(7, False)
				print "[VFD Display] Disable Rec icon"
				self.RecordEnd()

	def RecordEnd(self):
		if self.record:
			self.record = False
			self.session.nav.record_event.remove(self.gotRecordEvent)

	def hotplugCB(self, dev, media_state):
		if dev.startswith('/dev/sd'):
			if media_state == "1":
				evfd.getInstance().vfd_set_icon(13, True)
				print "[VFD Display] Set hotplud icon"
				self.usb = 1
			else:
				evfd.getInstance().vfd_set_icon(13, False)
				print "[VFD Display] Disable hotplud icon"
				self.usb = 0
			self.mount = None
			self.displayHddUsed()

	def SetMount(self):
		if config.plugins.vfdicon.hddicons.value == "all mounts":
			dir = config.usage.instantrec_path.value[:-1]
			if dir == "<default":
				dir = config.usage.default_path.value[:-1]
			if not self.mount or self.dir != dir:
				self.dir = dir
				self.mount = self.FindMountDir(dir)
				if not self.mount:
					self.mount = self.FindMountDir('/media/hdd')
				if not self.mount:
					self.mount = self.FindMountDev('/media/')
		elif not self.mount:
			self.mount = self.FindMountDir('/media/hdd')

	def FindMountDir(self, dir):
		mounts = open("/proc/mounts", 'r')
		for line in mounts:
			result = line.strip().split()
			if result[1] == dir:
				mounts.close()
				return dir
		mounts.close()
		return None

	def FindMountDev(self, dir):
		mounts = open("/proc/mounts", 'r')
		for line in mounts:
			result = line.strip().split()
			if result[1].startswith(dir):
				mounts.close()
				return result[1]
		mounts.close()
		return None

	def CheckSize(self):
		if self.mount:
			try:
				f = statvfs(self.mount)
			except:
				self.mount = None
				self.SetMount()
				if self.mount:
					try:
						f = statvfs(self.mount)
					except:
						self.mount = None
		if self.mount:
			return (f.f_blocks - f.f_bavail)*9/f.f_blocks
		else:
			return 0

	def displayHddUsed(self):
		isMuted = eDVBVolumecontrol.getInstance().isMuted()
		if self.isMuted != isMuted:
			self.isMuted = isMuted
			evfd.getInstance().vfd_set_icon(8, isMuted)
			print "[VFD Display] Mute icon", isMuted
		self.SetMount()
		if self.mount:
			used = self.CheckSize()
			print "[VFD Display] HDD used", self.mount, used
			if self.hddUsed != used:
				self.hddUsed = used
				evfd.getInstance().vfd_set_icon(30, True)
				if used >= 1:
					evfd.getInstance().vfd_set_icon(24,True)
				else:
					evfd.getInstance().vfd_set_icon(24,False)
				if used >= 2:
					evfd.getInstance().vfd_set_icon(23,True)
				else:
					evfd.getInstance().vfd_set_icon(23,False)
				if used >= 3:
					evfd.getInstance().vfd_set_icon(21,True)
				else:
					evfd.getInstance().vfd_set_icon(21,False)
				if used >= 4:
					evfd.getInstance().vfd_set_icon(20,True)
				else:
					evfd.getInstance().vfd_set_icon(20,False)
				if used >= 5:
					evfd.getInstance().vfd_set_icon(19,True)
				else:
					evfd.getInstance().vfd_set_icon(19,False)
				if used >= 6:
					evfd.getInstance().vfd_set_icon(18,True)
				else:
					evfd.getInstance().vfd_set_icon(18,False)
				if used >= 7:
					evfd.getInstance().vfd_set_icon(17,True)
				else:
					evfd.getInstance().vfd_set_icon(17,False)
				if used >= 8:
					evfd.getInstance().vfd_set_icon(16,True)
				else:
					evfd.getInstance().vfd_set_icon(16,False)
				if used == 9:
					evfd.getInstance().vfd_set_icon(22, True)
				print "[VFD Display] HDD used icon", used

VFDIconsInstance = None

def main(session, **kwargs):
	global VFDIconsInstance, DisplayType
	if VFDIconsInstance is None:
		VFDIconsInstance = VFDIcons(session)
	if config.plugins.vfdicon.displayshow.value == "clock" or DisplayType:
		sleep(1)
		VFDIconsInstance.timerEvent()
	if config.plugins.vfdicon.displayshow.value != "clock":
		if DisplayType:
			VFDIconsInstance.UpdatedInfo()
		else:
			VFDIconsInstance.WriteName()

def Plugins(**kwargs):
	return [
	PluginDescriptor(name = _("VFD Display"),
		description = _("VFD display config"), where = PluginDescriptor.WHERE_MENU,
		fnc = VFDdisplay),
	PluginDescriptor(where = PluginDescriptor.WHERE_SESSIONSTART, fnc = main )]
