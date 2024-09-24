installdir = $(pkglibdir)/python/Plugins/SystemPlugins

SUBDIRS = SoftwareManager PositionerSetup Satfinder \
	SkinSelector SatelliteEquipmentControl Videomode VideoTune Hotplug \
	DefaultServicesScanner DiseqcTester CommonInterfaceAssignment \
	FastScan OSDPositionSetup OSD3DSetup HdmiCEC VideoClippingSetup \
	VideoEnhancement NetworkWizard CableScan \
	SparkVFDControl SH4OSDAdjustment SH4BoosterControl VFD-Icons

if ! ENABLE_MINIMAL
SUBDIRS += WirelessLan
endif

if HAVE_TEMPFANCONTROL
SUBDIRS += TempFanControl
endif

if ENABLE_SPARK7162
SUBDIRS += SparkUnionTunerType
endif

install_PYTHON =	\
	__init__.py
