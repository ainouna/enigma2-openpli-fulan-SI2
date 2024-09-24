AC_INIT([enigma2],[4],[forum@openpli.org])
AM_INIT_AUTOMAKE([dist-bzip2 no-define tar-pax -Wno-portability])
AC_CONFIG_HEADERS([enigma2_config.h])

# Silent rules are available since 1.11, but older versions
# are still in use. So don't use them unconditionally.
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

AC_USE_SYSTEM_EXTENSIONS
AC_SYS_LARGEFILE

AC_PROG_CC
AC_PROG_CXX
m4_ifdef([LT_INIT], [LT_INIT], [AC_PROG_LIBTOOL])
AC_CONFIG_MACRO_DIR([m4])
AC_OPENMP()

AC_PATH_PROG(MSGFMT, msgfmt, AC_MSG_ERROR(Could not find msgfmt))

AM_PATH_PYTHON
AX_PYTHON_DEVEL
AX_PKG_SWIG
AX_SWIG_ENABLE_CXX
AX_SWIG_PYTHON
AX_PTHREAD

TUXBOX_APPS_DVB

AM_CONDITIONAL(HAVE_GIT_DIR, test -d "$srcdir/.git")
AM_CONDITIONAL(HAVE_FAKE_GIT_DIR, test -f "$srcdir/.git/last_commit_info")

AC_ARG_WITH(gstversion,
	AS_HELP_STRING([--with-gstversion],[use gstreamer version (major.minor)]),
	[GST_MAJORMINOR=$withval],[GST_MAJORMINOR=1.0])

AC_ARG_ENABLE(run_from_usb,
	[  --enable-run_from_usb      enable run_from_usb stuff],
	[AC_DEFINE(ENABLE_RUN_FROM_USB, 1, [enable run_from_usb stuff])])
AM_CONDITIONAL(ENABLE_RUN_FROM_USB, test "$enable_run_from_usb" = "yes")
if test "$run_from_usb" = "yes"; then
	AC_DEFINE(ENABLE_RUN_FROM_USB, 1, [enable run_from_usb stuff])
fi

AC_ARG_ENABLE(tf7700,
	[  --enable-tf7700            enable tf7700 stuff],
	[AC_DEFINE(ENABLE_TF7700, 1, [enable tf7700 stuff])])
AM_CONDITIONAL(ENABLE_TF7700, test "$enable_tf7700" = "yes")
if test "$enable_tf7700" = "yes"; then
	AC_DEFINE(ENABLE_TF7700, 1, [enable tf7700 stuff])
fi

AC_ARG_ENABLE(cuberevo_250hd,
	[  --enable-cuberevo_250hd    enable cuberevo_250d stuff],
	[AC_DEFINE(ENABLE_CUBEREVO_250HD, 1, [enable cuberevo_250hd stuff])])
AM_CONDITIONAL(ENABLE_CUBEREVO_250HD, test "$enable_cuberevo_250hd" = "yes")
if test "$enable_cuberevo_250hd" = "yes"; then
	AC_DEFINE(ENABLE_CUBEREVO_250HD, 1, [enable cuberevo_250hd stuff])
fi

AC_ARG_ENABLE(cuberevo_2000hd,
	[  --enable-cuberevo_2000hd   enable cuberevo_2000hd stuff],
	[AC_DEFINE(ENABLE_CUBEREVO_2000HD, 1, [enable cuberevo_2000hd stuff])])
AM_CONDITIONAL(ENABLE_CUBEREVO_2000HD, test "$enable_cuberevo_2000hd" = "yes")
if test "$enable_cuberevo_2000hd" = "yes"; then
	AC_DEFINE(ENABLE_CUBEREVO_2000HD, 1, [enable cuberevo_2000hd stuff])
fi

AC_ARG_ENABLE(cuberevo_3000hd,
	[  --enable-cuberevo_3000hd   enable cuberevo_3000hd stuff],
	[AC_DEFINE(ENABLE_CUBEREVO_3000HD, 1, [enable cuberevo_3000hd stuff])])
AM_CONDITIONAL(ENABLE_CUBEREVO_3000HD, test "$enable_cuberevo_3000hd" = "yes")
if test "$enable_cuberevo_3000hd" = "yes"; then
	AC_DEFINE(ENABLE_CUBEREVO_3000HD, 1, [enable cuberevo_3000hd stuff])
fi

AC_ARG_ENABLE(cuberevo_9500hd,
	[  --enable-cuberevo_9500hd   enable cuberevo_9500hd stuff],
	[AC_DEFINE(ENABLE_CUBEREVO_9500HD, 1, [enable cuberevo_9500hd stuff])])
AM_CONDITIONAL(ENABLE_CUBEREVO_9500HD, test "$enable_cuberevo_9500hd" = "yes")
if test "$enable_cuberevo_9500hd" = "yes"; then
	AC_DEFINE(ENABLE_CUBEREVO_9500HD, 1, [enable cuberevo_9500hd stuff])
fi

AC_ARG_ENABLE(cuberevo_mini,
	[  --enable-cuberevo_mini     enable cuberevo_mini stuff],
	[AC_DEFINE(ENABLE_CUBEREVO_MINI, 1, [enable cuberevo_mini stuff])])
AM_CONDITIONAL(ENABLE_CUBEREVO_MINI, test "$enable_cuberevo_mini" = "yes")
if test "$enable_cuberevo_mini" = "yes"; then
	AC_DEFINE(ENABLE_CUBEREVO_MINI, 1, [enable cuberevo_mini stuff])
fi

AC_ARG_ENABLE(cuberevo_mini2,
	[  --enable-cuberevo_mini2    enable cuberevo_mini2 stuff],
	[AC_DEFINE(ENABLE_CUBEREVO_MINI2, 1, [enable cuberevo_mini2 stuff])])
AM_CONDITIONAL(ENABLE_CUBEREVO_MINI2, test "$enable_cuberevo_mini2" = "yes")
if test "$enable_cuberevo_mini2" = "yes"; then
	AC_DEFINE(ENABLE_CUBEREVO_MINI2, 1, [enable cuberevo_mini2 stuff])
fi

AC_ARG_ENABLE(cuberevo_mini_fta,
	[  --enable-cuberevo_mini_fta enable cuberevo_mini_fta stuff],
	[AC_DEFINE(ENABLE_CUBEREVO_MINI_FTA, 1, [enable cuberevo_mini_fta stuff])])
AM_CONDITIONAL(ENABLE_CUBEREVO_MINI_FTA, test "$enable_cuberevo_mini_fta" = "yes")
if test "$enable_cuberevo_mini_fta" = "yes"; then
	AC_DEFINE(ENABLE_CUBEREVO_MINI_FTA, 1, [enable cuberevo_mini_fta stuff])
fi

AC_ARG_ENABLE(cuberevo,
	[  --enable-cuberevo          enable cuberevo stuff],
	[AC_DEFINE(ENABLE_CUBEREVO, 1, [enable cuberevo stuff])])
AM_CONDITIONAL(ENABLE_CUBEREVO, test "$enable_cuberevo" = "yes")
if test "$enable_cuberevo" = "yes"; then
	AC_DEFINE(ENABLE_CUBEREVO, 1, [enable cuberevo stuff])
fi

AC_ARG_ENABLE(spark,
	[  --enable-spark             enable spark stuff],
	[AC_DEFINE(ENABLE_SPARK, 1, [enable spark stuff])])
AM_CONDITIONAL(ENABLE_SPARK, test "$enable_spark" = "yes")
if test "$enable_spark" = "yes"; then
	AC_DEFINE(ENABLE_SPARK, 1, [enable spark stuff])
fi

AC_ARG_ENABLE(spark7162,
	[  --enable-spark7162         enable spark7162 stuff],
	[AC_DEFINE(ENABLE_SPARK7162, 1, [enable spark7162 stuff])])
AM_CONDITIONAL(ENABLE_SPARK7162, test "$enable_spark7162" = "yes")
if test "$enable_spark7162" = "yes"; then
	AC_DEFINE(ENABLE_SPARK7162, 1, [enable spark stuff])
fi

AC_ARG_ENABLE(hs9510,
	[  --enable-hs9510            enable hs9510 stuff],
	[AC_DEFINE(ENABLE_HS9510, 1, [enable hs9510 stuff])])
AM_CONDITIONAL(ENABLE_HS9510, test "$enable_hs9510" = "yes")
if test "$enable_hs9510" = "yes"; then
	AC_DEFINE(ENABLE_HS9510, 1, [enable hs9510 stuff])
fi

AC_ARG_ENABLE(hs8200,
	[  --enable-hs8200            enable hs8200 stuff],
	[AC_DEFINE(ENABLE_HS8200, 1, [enable hs8200 stuff])])
AM_CONDITIONAL(ENABLE_HS8200, test "$enable_hs8200" = "yes")
if test "$enable_hs8200" = "yes"; then
	AC_DEFINE(ENABLE_HS8200, 1, [enable hs8200 stuff])
fi

AC_ARG_ENABLE(fs9000,
	[  --enable-fs9000            enable fs9000 stuff],
[AC_DEFINE(ENABLE_FS9000, 1, [enable fs9000 stuff])])

AM_CONDITIONAL(ENABLE_FS9000, test "$enable_fs9000" = "yes")
if test "$enable_fs9000" = "yes"; then
	AC_DEFINE(ENABLE_FS9000, 1, [enable fs9000 stuff])
fi

AC_ARG_ENABLE(hs7110,
	[  --enable-hs7110            enable hs7110 stuff],
[AC_DEFINE(ENABLE_HS7110, 1, [enable hs7110 stuff])])

AM_CONDITIONAL(ENABLE_HS7110, test "$enable_hs7110" = "yes")
if test "$enable_hs7110" = "yes"; then
	AC_DEFINE(ENABLE_HS7110, 1, [enable hs7110 stuff])
fi

AC_ARG_ENABLE(hs7119,
	[  --enable-hs7119            enable hs7119 stuff],
[AC_DEFINE(ENABLE_HS7119, 1, [enable hs7119 stuff])])

AM_CONDITIONAL(ENABLE_HS7119, test "$enable_hs7119" = "yes")
if test "$enable_hs7119" = "yes"; then
	AC_DEFINE(ENABLE_HS7119, 1, [enable hs7119 stuff])
fi

AC_ARG_ENABLE(hs7420,
	[  --enable-hs7420            enable hs7420 stuff],
	[AC_DEFINE(ENABLE_HS7420, 1, [enable hs7420 stuff])])
AM_CONDITIONAL(ENABLE_HS7420, test "$enable_hs7420" = "yes")
if test "$enable_hs7420" = "yes"; then
	AC_DEFINE(ENABLE_HS7420, 1, [enable hs7420 stuff])
fi

AC_ARG_ENABLE(hs7429,
	[  --enable-hs7429            enable hs7429 stuff],
	[AC_DEFINE(ENABLE_HS7429, 1, [enable hs7429 stuff])])
AM_CONDITIONAL(ENABLE_HS7429, test "$enable_hs7429" = "yes")
if test "$enable_hs7429" = "yes"; then
	AC_DEFINE(ENABLE_HS7429, 1, [enable hs7429 stuff])
fi

AC_ARG_ENABLE(hs7810a,
	[  --enable-hs7810a           enable hs7810a stuff],
	[AC_DEFINE(ENABLE_HS7810A, 1, [enable hs7810a stuff])])
AM_CONDITIONAL(ENABLE_HS7810A, test "$enable_hs7810a" = "yes")
if test "$enable_hs7810a" = "yes"; then
	AC_DEFINE(ENABLE_HS7810A, 1, [enable hs7810a stuff])
fi

AC_ARG_ENABLE(hs7819,
	[  --enable-hs7819            enable hs7819 stuff],
	[AC_DEFINE(ENABLE_HS7819, 1, [enable hs7819 stuff])])
AM_CONDITIONAL(ENABLE_HS7819, test "$enable_hs7819" = "yes")
if test "$enable_hs7819" = "yes"; then
	AC_DEFINE(ENABLE_HS7819, 1, [enable hs7819 stuff])
fi

AC_ARG_ENABLE(ufs910,
	[  --enable-ufs910            enable ufs910 stuff],
	[AC_DEFINE(ENABLE_UFS910, 1, [enable ufs910 stuff])])
AM_CONDITIONAL(ENABLE_UFS910, test "$enable_ufs910" = "yes")
if test "$enable_ufs910" = "yes"; then
	AC_DEFINE(ENABLE_UFS910, 1, [enable ufs910 stuff])
fi

AC_ARG_ENABLE(ufs910,
	[  --enable-ufs910            enable ufs910 stuff],
	[AC_DEFINE(ENABLE_UFS910, 1, [enable ufs910 stuff])])
AM_CONDITIONAL(ENABLE_UFS910, test "$enable_ufs910" = "yes")
if test "$enable_ufs910" = "yes"; then
	AC_DEFINE(ENABLE_UFS910, 1, [enable ufs910 stuff])
fi

AC_ARG_ENABLE(ufs912,
	[  --enable-ufs912            enable ufs912 stuff],
	[AC_DEFINE(ENABLE_UFS912, 1, [enable ufs912 stuff])])
AM_CONDITIONAL(ENABLE_UFS912, test "$enable_ufs912" = "yes")
if test "$enable_ufs912" = "yes"; then
	AC_DEFINE(ENABLE_UFS912, 1, [enable ufs912 stuff])
fi

AC_ARG_ENABLE(ufs913,
	[  --enable-ufs913            enable ufs913 stuff],
	[AC_DEFINE(ENABLE_UFS913, 1, [enable ufs913 stuff])])
AM_CONDITIONAL(ENABLE_UFS913, test "$enable_ufs913" = "yes")
if test "$enable_ufs913" = "yes"; then
	AC_DEFINE(ENABLE_UFS913, 1, [enable ufs913 stuff])
fi

AC_ARG_ENABLE(ufs922,
	[  --enable-ufs922            enable ufs922 stuff],
	[AC_DEFINE(ENABLE_UFS922, 1, [enable ufs922 stuff])])
AM_CONDITIONAL(ENABLE_UFS922, test "$enable_ufs922" = "yes")
if test "$enable_ufs922" = "yes"; then
	AC_DEFINE(ENABLE_UFS922, 1, [enable ufs922 stuff])
fi

AC_ARG_ENABLE(ufc960,
	[  --enable-ufc960            enable ufc960 stuff],
	[AC_DEFINE(ENABLE_UFC960, 1, [enable ufc960 stuff])])
AM_CONDITIONAL(ENABLE_UFC960, test "$enable_ufc960" = "yes")
if test "$enable_ufc960" = "yes"; then
	AC_DEFINE(ENABLE_UFC960, 1, [enable ufc960 stuff])
fi

AC_ARG_ENABLE(adb_box,
	[  --adb_box                  enable adb_box stuff],
	[AC_DEFINE(ENABLE_ADB_BOX, 1, [enable adb_box stuff])])
AM_CONDITIONAL(ENABLE_ADB_BOX, test "$enable_adb_box" = "yes")
if test "$enable_adb_box" = "yes"; then
	AC_DEFINE(ENABLE_ADB_BOX, 1, [enable adb_box stuff])
fi

AC_ARG_ENABLE(vitamin_hd5000,
	[  --enable-vitamin_hd5000    enable vitamin_hd5000 stuff],
	[AC_DEFINE(ENABLE_VITAMIN_HD5000, 1, [enable vitamin_hd5000 stuff])])
AM_CONDITIONAL(ENABLE_VITAMIN_HD5000, test "$enable_vitamin_hd5000" = "yes")
if test "$enable_vitamin_hd5000" = "yes"; then
	AC_DEFINE(ENABLE_VITAMIN_HD5000, 1, [enable vitamin_hd5000 stuff])
fi

AC_ARG_ENABLE(hl101,
	[  --enable-hl101             enable hl101 stuff],
	[AC_DEFINE(ENABLE_HL101, 1, [enable hl101 stuff])])
AM_CONDITIONAL(ENABLE_HL101, test "$enable_hl101" = "yes")
if test "$enable_hl101" = "yes"; then
	AC_DEFINE(ENABLE_HL101, 1, [enable hl101 stuff])
fi

AC_ARG_ENABLE(vip1_v1,
	[  --enable-vip1_v1           enable vip1_v1 stuff],
	[AC_DEFINE(ENABLE_VIP1_V1, 1, [enable vip1_v1 stuff])])
AM_CONDITIONAL(ENABLE_VIP1_V1, test "$enable_vip1_v1" = "yes")
if test "$enable_vip1_v1" = "yes"; then
	AC_DEFINE(ENABLE_VIP1_V1, 1, [enable vip1_v1 stuff])
fi

AC_ARG_ENABLE(vip1_v2,
	[  --enable-vip1_v2           enable vip1_v2 stuff],
	[AC_DEFINE(ENABLE_VIP1_V2, 1, [enable vip1_v2 stuff])])
AM_CONDITIONAL(ENABLE_VIP1_V2, test "$enable_vip1_v2" = "yes")
if test "$enable_vip1_v2" = "yes"; then
	AC_DEFINE(ENABLE_VIP1_V2, 1, [enable vip1_v2 stuff])
fi

AC_ARG_ENABLE(vip2,
	[  --enable-vip2              enable vip2 stuff],
	[AC_DEFINE(ENABLE_VIP2, 1, [enable vip2 stuff])])
AM_CONDITIONAL(ENABLE_VIP2, test "$enable_vip2" = "yes")
if test "$enable_vip2" = "yes"; then
	AC_DEFINE(ENABLE_VIP2, 1, [enable vip2 stuff])
fi

AC_ARG_ENABLE(pace7241,
	[  --enable-pace7241          enable pace7241 stuff],
	[AC_DEFINE(ENABLE_PACE7241, 1, [enable pace7241 stuff])])
AM_CONDITIONAL(ENABLE_PACE7241, test "$enable_pace7241" = "yes")
if test "$enable_pace7241" = "yes"; then
	AC_DEFINE(ENABLE_PACE7241, 1, [enable pace7241 stuff])
fi

AC_ARG_ENABLE(opt9600,
	[  --enable-opt9600           enable opt9600 stuff],
	[AC_DEFINE(ENABLE_OPT9600, 1, [enable opt9600 stuff])])
AM_CONDITIONAL(ENABLE_OPT9600, test "$enable_opt9600" = "yes")
if test "$enable_opt9600" = "yes"; then
	AC_DEFINE(ENABLE_OPT9600, 1, [enable opt9600 stuff])
fi

AC_ARG_ENABLE(opt9600mini,
	[  --enable-opt9600mini       enable opt9600mini stuff],
	[AC_DEFINE(ENABLE_OPT9600MINI, 1, [enable opt9600mini stuff])])
AM_CONDITIONAL(ENABLE_OPT9600MINI, test "$enable_opt9600mini" = "yes")
if test "$enable_opt9600mini" = "yes"; then
	AC_DEFINE(ENABLE_OPT9600MINI, 1, [enable opt9600mini stuff])
fi

AC_ARG_ENABLE(opt9600prima,
	[  --enable-opt9600prima      enable opt9600prima stuff],
	[AC_DEFINE(ENABLE_OPT9600PRIMA, 1, [enable opt9600prima stuff])])
AM_CONDITIONAL(ENABLE_OPT9600PRIMA, test "$enable_opt9600prima" = "yes")
if test "$enable_opt9600prima" = "yes"; then
	AC_DEFINE(ENABLE_OPT9600PRIMA, 1, [enable opt9600prima stuff])
fi

AC_ARG_ENABLE(atemio520,
	[  --enable-atemio520         enable atemio520 stuff],
	[AC_DEFINE(ENABLE_ATEMIO520, 1, [enable atemio520 stuff])])
AM_CONDITIONAL(ENABLE_ATEMIO520, test "$enable_atemio520" = "yes")
if test "$enable_atemio520" = "yes"; then
	AC_DEFINE(ENABLE_ATEMIO520, 1, [enable atemio520 stuff])
fi

AC_ARG_ENABLE(hchs8100,
	[  --enable-hchs8100          enable hchs8100 stuff],
	[AC_DEFINE(ENABLE_HCHS8100, 1, [enable hchs8100 stuff])])
AM_CONDITIONAL(ENABLE_HCHS8100, test "$enable_hchs8100" = "yes")
if test "$enable_hchs8100" = "yes"; then
	AC_DEFINE(ENABLE_HCHS8100, 1, [enable hchs8100 stuff])
fi

AC_ARG_ENABLE(minimal,
	[  --enable-minimal          enable minimal config],
	[AC_DEFINE(ENABLE_MINIMAL, 1, [enable minimal config])])
if test "$enable_minimal" = "yes"; then
	AC_DEFINE(ENABLE_MINIMAL, 1, [enable minimal config])
fi
AM_CONDITIONAL(ENABLE_MINIMAL, test "$enable_minimal" = "yes")

dnl versions of plugins-base

AC_ARG_WITH(libeplayer3,
	AS_HELP_STRING([--with-libeplayer3],[use libeplayer3 as player engine support, yes or no]),
	[with_libeplayer3=$withval],[with_libeplayer3=no])
if test "$with_libeplayer3" = "yes"; then
	PKG_CHECK_MODULES(LIBXINE, libeplayer3)
	AC_DEFINE([ENABLE_LIBEPLAYER3],[1],[Define to 1 if you have libeplayer3])
fi
AM_CONDITIONAL(ENABLE_LIBEPLAYER3, test "$with_libeplayer3" = "yes")

AC_ARG_ENABLE(mediafwgstreamer,
	[  --enable-mediafwgstreamer      enable gstreamer as player engine supportt],
	[AC_DEFINE(ENABLE_MEDIAFWGSTREAMER,1,[enable gstreamer as player engine support])])

AM_CONDITIONAL(ENABLE_MEDIAFWGSTREAMER,test "$enable_mediafwgstreamer" = "yes")
if test "$enable_mediafwgstreamer" = "yes"; then
	AC_DEFINE(ENABLE_MEDIAFWGSTREAMER,1,[include gstreamer as player engine support])
fi

if test "$enable_mediafwgstreamer" = "yes"; then
	PKG_CHECK_MODULES(GSTREAMER, gstreamer-$GST_MAJORMINOR gstreamer-pbutils-$GST_MAJORMINOR)
	PKG_CHECK_MODULES(BASE, [freetype2 fribidi gstreamer-$GST_MAJORMINOR gstreamer-pbutils-$GST_MAJORMINOR libdvbsi++ libpng libxml-2.0 sigc++-2.0 libssl libcrypto])
else
	PKG_CHECK_MODULES(BASE, [freetype2 fribidi glib-2.0 libdvbsi++ libpng libxml-2.0 sigc++-2.0 libssl libcrypto])
fi

PKG_CHECK_MODULES(TUXTXT, tuxbox-tuxtxt)
PKG_CHECK_MODULES(BASE, [freetype2 fribidi glib-2.0 libdvbsi++ libpng libxml-2.0 sigc++-2.0 libssl libcrypto])
PKG_CHECK_MODULES(LIBDDVD, libdreamdvd, HAVE_LIBDDVD="yes", HAVE_LIBDDVD="no")
AM_CONDITIONAL(HAVE_LIBDDVD, test "$HAVE_LIBDDVD" = "yes")
PKG_CHECK_MODULES(AVAHI, avahi-client)

AC_CHECK_LIB([udfread], [udfread_init])
AC_CHECK_LIB([dl], [dlopen], [LIBDL_LIBS="-ldl"], [AC_MSG_ERROR([Could not find libdl])])
AC_SUBST(LIBDL_LIBS)
AC_CHECK_LIB([jpeg], [jpeg_set_defaults], [LIBJPEG_LIBS="-ljpeg"], [AC_MSG_ERROR([Could not find libjpeg])])
AC_SUBST(LIBJPEG_LIBS)
AC_CHECK_LIB([ungif], [DGifOpen], [LIBGIF_LIBS="-lungif"], [AC_CHECK_LIB([gif], [DGifOpen], [LIBGIF_LIBS="-lgif"], [AC_MSG_ERROR([Could not find libgif or libungif])])])
AC_SUBST(LIBGIF_LIBS)

AC_ARG_WITH(crashlogemail,
	[  --with-crashlogemail=crash log email address],
	[CRASHLOGEMAIL="$withval"],[CRASHLOGEMAIL="the OpenPLi forum"])
AC_SUBST(CRASHLOGEMAIL)
AC_DEFINE_UNQUOTED(CRASH_EMAILADDR,"$CRASHLOGEMAIL",[crash log email address])

AC_ARG_WITH(boxtype,
	[  --with-boxtype=NAME box type [[none,dm7025,dm800...]]],
	[BOXTYPE="$withval"],[BOXTYPE="dm800"])
AC_SUBST(BOXTYPE)
AC_DEFINE_UNQUOTED(BOXTYPE,"$BOXTYPE",[box type])

AM_CONDITIONAL(DREAMBOX, test `echo "$BOXTYPE" | cut -b 1-2` == "dm")
AM_CONDITIONAL(HAVE_TEMPFANCONTROL, test "$BOXTYPE" == dm8000 -o "$BOXTYPE" == dm800se -o "$BOXTYPE" == dm500hd)
if test `echo "$BOXTYPE" | cut -b 1-2` == "dm"; then
	AC_DEFINE(DREAMBOX, 1, [Dreambox hardware])
	AC_DEFINE(KEY_PLAY_ACTUALLY_IS_KEY_PLAYPAUSE, 1,[define when rc sends a KEY_PLAY event for its KEY_PLAYPAUSE key])
fi

AC_ARG_WITH(textlcd,
	AC_HELP_STRING([--with-textlcd], [use ascii based lcd, yes or no]),
	[[withtextlcd=$withval]],
	[[withtextlcd=no]]
)
if test x"$withtextlcd" != xno ; then
	AC_DEFINE(HAVE_TEXTLCD, 1,[Define when using an ascii based lcd device])
fi
AM_CONDITIONAL(HAVE_TEXTLCD, test x"$withtextlcd" != xno)

AC_ARG_WITH(7segment,
	AC_HELP_STRING([--with-7segment], [use 7 segment lcd, yes or no]),
	[[TEXTSKIN="7segment"]],
	[[TEXTSKIN="default"]]
)
AC_SUBST(TEXTSKIN)

if test `echo "$BOXTYPE" | cut -b 1-7` == "mbmicro"; then
	AC_DEFINE(FORCE_NO_BLENDING_ACCELERATION, 1,[define when the framebuffer acceleration does not have alphablending support, though the autodetection might indicate that it does])
	AC_DEFINE(FORCE_NO_FILL_ACCELERATION, 1,[define when the framebuffer acceleration does not have fill support])
	AC_DEFINE(FORCE_ADVANCED_REMOTE, 1,[define to fixup the input device identification when the remote control is actually an 'advanced' remote (with play/forward/rewind keys)])
	AC_DEFINE(KEY_PLAY_ACTUALLY_IS_KEY_PLAYPAUSE, 1,[define when rc sends a KEY_PLAY event for its KEY_PLAYPAUSE key])
fi

AC_ARG_WITH(graphlcd,
	AC_HELP_STRING([--with-graphlcd], [use GraphLCD color display, yes or no]),
	[[withgraphlcd=$withval]],
	[[withgraphlcd=no]]
)
if test x"$withgraphlcd" != xno ; then
	AC_DEFINE(HAVE_GRAPHLCD, 1,[Define when using a GraphLCD color display device])
fi
AM_CONDITIONAL(HAVE_GRAPHLCD, test x"$withgraphlcd" != xno)

AC_ARG_WITH(lcd,
	AC_HELP_STRING([--with-lcd], [use LCD display, yes or no]),
	[[withlcd=$withval]],
	[[withlcd=no]]
)
if ! test x"$withlcd" != xno ; then
	AC_DEFINE(NO_LCD, 1,[Define when not using a LCD display device])
fi
AM_CONDITIONAL(NO_LCD, test x"$withlcd" != xno)
if test `echo "$BOXTYPE" | cut -b 1-2` == "vu"; then
	AC_DEFINE(FORCE_NO_BLENDING_ACCELERATION, 1,[define when the framebuffer acceleration does not have alphablending support, though the autodetection might indicate that it does])
	AC_DEFINE(FORCE_NO_FILL_ACCELERATION, 1,[define when the framebuffer acceleration does not have fill support])
	AC_DEFINE(FORCE_ADVANCED_REMOTE, 1,[define to fixup the input device identification when the remote control is actually an 'advanced' remote (with play/forward/rewind keys)])
fi

AC_ARG_WITH(libsdl,
	AS_HELP_STRING([--with-libsdl],[use libsdl, yes or no]),
	[with_libsdl=$withval],[with_libsdl=no])
if test "$with_libsdl" = "yes"; then
	PKG_CHECK_MODULES(LIBSDL, sdl)
fi
AM_CONDITIONAL(HAVE_LIBSDL, test "$with_libsdl" = "yes")

AC_ARG_WITH(libxine,
	AS_HELP_STRING([--with-libxine],[use libxine, yes or no]),
	[with_libxine=$withval],[with_libxine=no])
if test "$with_libxine" = "yes"; then
	PKG_CHECK_MODULES(LIBXINE, libxine)
	AC_DEFINE([WITH_XINE],[1],[Define to 1 if you have libxine])
fi
AM_CONDITIONAL(HAVE_LIBXINE, test "$with_libxine" = "yes")

AC_ARG_WITH(debug,
	AS_HELP_STRING([--without-debug],[disable debugging code]),
	[with_debug="$withval"],[with_debug="yes"])
if test "$with_debug" = "yes"; then
	AC_DEFINE([DEBUG],[1],[Define to 1 to enable debugging code])
fi

AC_ARG_WITH(memcheck,
	AS_HELP_STRING([--with-memcheck],[enable memory leak checks]),
	[with_memcheck="$withval"],[with_memcheck="no"])
if test "$with_memcheck" = "yes"; then
	AC_DEFINE([MEMLEAK_CHECK],[1],[Define to 1 to enable memory leak checks])
fi

AC_ARG_WITH(po,
	AS_HELP_STRING([--with-po],[enable updating of po files]),
	[with_po="$withval"],[with_po="no"])
if test "$with_po" = "yes"; then
	AC_PATH_PROG(MSGINIT, msginit)
	AC_PATH_PROG(MSGMERGE, msgmerge)
	AC_PATH_PROG(MSGUNIQ, msguniq)
	AC_PATH_PROG(MSGATTRIB, msgattrib)
	AC_PATH_PROG(XGETTEXT, xgettext)
	if test -z "$MSGINIT" -o -z "$MSGMERGE" -o -z "$MSGUNIQ" -o -z "$MSGATTRIB" -o -z "$XGETTEXT"; then
		AC_MSG_ERROR([Could not find required gettext tools])
	fi
fi
AM_CONDITIONAL(UPDATE_PO, test "$with_po" = "yes")

AC_ARG_WITH(alsa,
	AC_HELP_STRING([--with-alsa], [Enable ALSA support]),
	[[with_alse=$withval]],
	[[with_alse=no]]
)
if test x"$with_alsa" == xyes ; then
	AC_DEFINE(HAVE_ALSA, 1,[Enables ALSA support])
	PKG_CHECK_MODULES(ALSA, alsa)
fi

AC_ARG_WITH(alsacard,
	AC_HELP_STRING([--with-alsacard=card], [use 'card' for alsa card device, e.g. hw:0]),
	[[with_alsacard=$withval]],
	[[with_alsacard=no]]
)
if test x"$with_alsacard" != xno ; then
	AC_DEFINE_UNQUOTED(ALSA_CARD, "$withval",[Defines which alsa card to use])
fi

AC_ARG_WITH(alsamixer,
	AC_HELP_STRING([--with-alsamixer=mixername], [use alsa 'mixername' for volume control, e.g. Master]),
	[[with_alsamixer=$withval]],
	[[with_alsamixer=no]]
)
if test x"$with_alsamixer" != xno ; then
	AC_DEFINE_UNQUOTED(ALSA_VOLUME_MIXER, "$withval",[Defines which alsa mixer to use for volume control])
fi

AC_ARG_WITH(fbdev,
	AC_HELP_STRING([--with-fbdev=devicename], [use devicename for framebuffer device, e.g. /dev/fb0 ]),
	[[with_fbdev=$withval]],
	[[with_fbdev=no]]
)
if test x"$with_fbdev" != xno ; then
	AC_DEFINE_UNQUOTED(FB_DEV, "$withval", [Defines which device to use for main framebuffer (e.g. /dev/fb0)])
fi

AC_ARG_WITH(lcddev,
	AC_HELP_STRING([--with-lcddev=devicename], [use devicename for lcd framebuffer device, e.g. /dev/fb1 ]),
	[[with_lcddev=$withval]],
	[[with_lcddev=no]]
)
if test x"$with_lcddev" != xno ; then
	AC_DEFINE_UNQUOTED(LCD_DEV, "$withval", [Defines which device to use for lcd (e.g. /dev/fb1)])
fi

AC_ARG_WITH(amlogic,
	AC_HELP_STRING([--with-amlogic], [use amlogic MPEG decoder]),
	[[with_amlogic=$withval]],
	[[with_amlogic=no]]
)
AM_CONDITIONAL(HAVE_AMLOGIC, test x"$with_amlogic" = xyes)
if test x"$with_amlogic" = xyes ; then
	AC_DEFINE(HAVE_AMLOGIC, 1,[Enables AMLOGIC decoder support])
	PKG_CHECK_MODULES(AMCODEC, libamcodec)
	PKG_CHECK_MODULES(AMADEC, libamadec)
	PKG_CHECK_MODULES(DVBCSA, libdvbcsa)
fi

AC_ARG_WITH(alphablendingacceleration,
	AC_HELP_STRING([--with-alphablendingacceleration=never/always/auto], [alphablending acceleration strategy: never accelerate / always accelerate / automatically decide when to accelerate (default)]),
	[[with_alphablendingacceleration=$withval]],
	[[with_alphablendingacceleration=auto]]
)

if test x"$with_alphablendingacceleration" = xnever ; then
	AC_DEFINE_UNQUOTED(FORCE_NO_BLENDING_ACCELERATION, 1, [Do not attempt to accelerate alphablending blits])
elif test x"$with_alphablendingacceleration" = xalways ; then
	AC_DEFINE_UNQUOTED(FORCE_ALPHABLENDING_ACCELERATION, 1, [Accelerate alphablending blits])
fi

AC_ARG_WITH(accelerationthreshold,
	AC_HELP_STRING([--with-accelerationthreshold=n], [use acceleration threshold of n bytes]),
	[[with_accelerationthreshold=$withval]],
	[[with_accelerationthreshold=48000]]
)

AC_DEFINE_UNQUOTED(GFX_SURFACE_ACCELERATION_THRESHOLD, $with_accelerationthreshold,[Configure threshold for accelerated surfaces (in bytes)])

AC_ARG_WITH(fillaccelerationthreshold,
	AC_HELP_STRING([--with-fillaccelerationthreshold=n], [use fill acceleration threshold of n bytes]),
	[[with_fillaccelerationthreshold=$withval]],
	[[with_fillaccelerationthreshold=80000]]
)

AC_DEFINE_UNQUOTED(GFX_SURFACE_FILL_ACCELERATION_THRESHOLD, $with_fillaccelerationthreshold,[Configure threshold for accelerated fill operations (in bytes)])

AC_ARG_WITH(blitaccelerationthreshold,
	AC_HELP_STRING([--with-blitaccelerationthreshold=n], [use blit acceleration threshold of n bytes]),
	[[with_blitaccelerationthreshold=$withval]],
	[[with_blitaccelerationthreshold=0]]
)

AC_DEFINE_UNQUOTED(GFX_SURFACE_BLIT_ACCELERATION_THRESHOLD, $with_blitaccelerationthreshold,[Configure threshold for accelerated blit operations (in bytes)])

AC_ARG_WITH(accelerationaccumulation,
	AC_HELP_STRING([--with-accelerationaccumulation], [accumulate blit/fill acceleration operations]),
	[[with_accelerationaccumulation=$withval]],
	[[with_accelerationaccumulation=no]]
)

if test x"$with_accelerationaccumulation" = xyes ; then
	AC_DEFINE(SUPPORT_ACCUMULATED_ACCELERATION_OPERATIONS, 1,[Accumulate blit/fill acceleration operations])
fi

AC_CHECK_HEADERS([sys/klog.h])
AC_CHECK_FUNCS([klogctl])
AC_CHECK_HEADERS([shadow.h])

AC_CHECK_LIB([crypt], [crypt], [BASE_LIBS+=" -lcrypt"], [AC_MSG_ERROR([Could not find crypt])])
AC_CHECK_LIB([rt], [clock_gettime], [BASE_LIBS+=" -lrt"], [AC_MSG_ERROR([Could not find rt])])

ENIGMA2_CFLAGS="-fno-rtti -fno-exceptions -rdynamic -funwind-tables"
AC_SUBST(ENIGMA2_CFLAGS)

CPPFLAGS="$CPPFLAGS $PYTHON_CPPFLAGS -std=c++11"
CFLAGS="$CFLAGS -Wall -std=c++11"
CXXFLAGS="$CXXFLAGS -Wall -std=c++11 $BASE_CFLAGS $ENIGMA2_CFLAGS $PTHREAD_CFLAGS $OPENMP_CFLAGS $ALSA_CFLAGS $AMCODEC_CFLAGS $AMADEC_CFLAGS $DVBCSA_CFLAGS"

AC_CONFIG_FILES([
Makefile
data/Makefile
data/fonts/Makefile
data/countries/Makefile
data/extensions/Makefile
data/keymaps/Makefile
data/hw_info/Makefile
data/rc_models/Makefile
data/skin_default/Makefile
data/skin_default/menu/Makefile
data/skin_default/icons/Makefile
data/skin_default/buttons/Makefile
data/skin_default/spinner/Makefile
data/skin_default/LCDIcons/Makefile
include/Makefile
lib/Makefile
lib/base/eenv.cpp
lib/python/Makefile
lib/python/Components/Makefile
lib/python/Components/Converter/Makefile
lib/python/Components/Renderer/Makefile
lib/python/Components/Sources/Makefile
lib/python/Screens/Makefile
lib/python/Plugins/Makefile
lib/python/Plugins/SystemPlugins/CableScan/Makefile
lib/python/Plugins/SystemPlugins/FastScan/Makefile
lib/python/Plugins/SystemPlugins/OSDPositionSetup/Makefile
lib/python/Plugins/SystemPlugins/OSD3DSetup/Makefile
lib/python/Plugins/SystemPlugins/HdmiCEC/Makefile
lib/python/Plugins/SystemPlugins/VideoClippingSetup/Makefile
lib/python/Plugins/Extensions/CutListEditor/Makefile
lib/python/Plugins/Extensions/CutListEditor/meta/Makefile
lib/python/Plugins/Extensions/DVDBurn/Makefile
lib/python/Plugins/Extensions/DVDBurn/meta/Makefile
lib/python/Plugins/Extensions/DVDPlayer/Makefile
lib/python/Plugins/Extensions/DVDPlayer/meta/Makefile
lib/python/Plugins/Extensions/GraphMultiEPG/Makefile
lib/python/Plugins/Extensions/GraphMultiEPG/meta/Makefile
lib/python/Plugins/Extensions/Makefile
lib/python/Plugins/Extensions/MediaPlayer/Makefile
lib/python/Plugins/Extensions/MediaPlayer/meta/Makefile
lib/python/Plugins/Extensions/MediaScanner/Makefile
lib/python/Plugins/Extensions/MediaScanner/meta/Makefile
lib/python/Plugins/Extensions/PicturePlayer/Makefile
lib/python/Plugins/Extensions/PicturePlayer/meta/Makefile
lib/python/Plugins/Extensions/PicturePlayer/data/Makefile
lib/python/Plugins/Extensions/SocketMMI/Makefile
lib/python/Plugins/Extensions/SocketMMI/meta/Makefile
lib/python/Plugins/Extensions/SocketMMI/src/Makefile
lib/python/Plugins/Extensions/TuxboxPlugins/Makefile
lib/python/Plugins/Extensions/TuxboxPlugins/meta/Makefile
lib/python/Plugins/PLi/Makefile
lib/python/Plugins/SystemPlugins/CommonInterfaceAssignment/Makefile
lib/python/Plugins/SystemPlugins/CommonInterfaceAssignment/meta/Makefile
lib/python/Plugins/SystemPlugins/DefaultServicesScanner/Makefile
lib/python/Plugins/SystemPlugins/DefaultServicesScanner/meta/Makefile
lib/python/Plugins/SystemPlugins/DiseqcTester/Makefile
lib/python/Plugins/SystemPlugins/DiseqcTester/meta/Makefile
lib/python/Plugins/SystemPlugins/Hotplug/Makefile
lib/python/Plugins/SystemPlugins/Hotplug/meta/Makefile
lib/python/Plugins/SystemPlugins/KeymapManager/Makefile
lib/python/Plugins/SystemPlugins/KeymapManager/meta/Makefile
lib/python/Plugins/SystemPlugins/Makefile
lib/python/Plugins/SystemPlugins/TempFanControl/Makefile
lib/python/Plugins/SystemPlugins/TempFanControl/meta/Makefile
lib/python/Plugins/SystemPlugins/NetworkWizard/Makefile
lib/python/Plugins/SystemPlugins/NetworkWizard/meta/Makefile
lib/python/Plugins/SystemPlugins/PositionerSetup/Makefile
lib/python/Plugins/SystemPlugins/PositionerSetup/meta/Makefile
lib/python/Plugins/SystemPlugins/SatelliteEquipmentControl/Makefile
lib/python/Plugins/SystemPlugins/SatelliteEquipmentControl/meta/Makefile
lib/python/Plugins/SystemPlugins/Satfinder/Makefile
lib/python/Plugins/SystemPlugins/Satfinder/meta/Makefile
lib/python/Plugins/SystemPlugins/SkinSelector/Makefile
lib/python/Plugins/SystemPlugins/SkinSelector/meta/Makefile
lib/python/Plugins/SystemPlugins/SoftwareManager/Makefile
lib/python/Plugins/SystemPlugins/SoftwareManager/meta/Makefile
lib/python/Plugins/SystemPlugins/VideoEnhancement/Makefile
lib/python/Plugins/SystemPlugins/VideoEnhancement/meta/Makefile
lib/python/Plugins/SystemPlugins/VideoTune/Makefile
lib/python/Plugins/SystemPlugins/VideoTune/meta/Makefile
lib/python/Plugins/SystemPlugins/Videomode/Makefile
lib/python/Plugins/SystemPlugins/Videomode/meta/Makefile
lib/python/Plugins/SystemPlugins/WirelessLan/Makefile
lib/python/Plugins/SystemPlugins/WirelessLan/meta/Makefile
lib/python/Plugins/SystemPlugins/SparkVFDControl/Makefile
lib/python/Plugins/SystemPlugins/SparkVFDControl/meta/Makefile
lib/python/Plugins/SystemPlugins/SH4OSDAdjustment/Makefile
lib/python/Plugins/SystemPlugins/SH4OSDAdjustment/meta/Makefile
lib/python/Plugins/SystemPlugins/SH4BoosterControl/Makefile
lib/python/Plugins/SystemPlugins/SH4BoosterControl/meta/Makefile
lib/python/Plugins/SystemPlugins/SparkUnionTunerType/Makefile
lib/python/Plugins/SystemPlugins/SparkUnionTunerType/meta/Makefile
lib/python/Plugins/SystemPlugins/OnErrorRestartService/Makefile
lib/python/Plugins/Extensions/ModemSettings/Makefile
lib/python/Plugins/Extensions/adb_5800VFD/Makefile
lib/python/Plugins/Extensions/adb_5800VFD/meta/Makefile
lib/python/Plugins/Extensions/adb_5800VFD/locale/Makefile
lib/python/Plugins/Extensions/adb_5800VFD/locale/nl/Makefile
lib/python/Plugins/Extensions/adb_5800VFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CuberevoVFD/Makefile
lib/python/Plugins/Extensions/fs9000VFD/Makefile
lib/python/Plugins/Extensions/fs9000VFD/meta/Makefile
lib/python/Plugins/Extensions/fs9000VFD/locale/Makefile
lib/python/Plugins/Extensions/fs9000VFD/locale/nl/Makefile
lib/python/Plugins/Extensions/fs9000VFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/hs7110VFD/Makefile
lib/python/Plugins/Extensions/hs7110VFD/meta/Makefile
lib/python/Plugins/Extensions/hs7110VFD/locale/Makefile
lib/python/Plugins/Extensions/hs7110VFD/locale/nl/Makefile
lib/python/Plugins/Extensions/hs7110VFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/hs742xVFD/Makefile
lib/python/Plugins/Extensions/hs742xVFD/meta/Makefile
lib/python/Plugins/Extensions/hs742xVFD/locale/Makefile
lib/python/Plugins/Extensions/hs742xVFD/locale/nl/Makefile
lib/python/Plugins/Extensions/hs742xVFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/hs7810aVFD/Makefile
lib/python/Plugins/Extensions/hs7810aVFD/meta/Makefile
lib/python/Plugins/Extensions/hs7810aVFD/locale/Makefile
lib/python/Plugins/Extensions/hs7810aVFD/locale/nl/Makefile
lib/python/Plugins/Extensions/hs7810aVFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/hs8200VFD/Makefile
lib/python/Plugins/Extensions/hs8200VFD/meta/Makefile
lib/python/Plugins/Extensions/hs8200VFD/locale/Makefile
lib/python/Plugins/Extensions/hs8200VFD/locale/nl/Makefile
lib/python/Plugins/Extensions/hs8200VFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/hs9510VFD/Makefile
lib/python/Plugins/Extensions/hs9510VFD/meta/Makefile
lib/python/Plugins/Extensions/hs9510VFD/locale/Makefile
lib/python/Plugins/Extensions/hs9510VFD/locale/nl/Makefile
lib/python/Plugins/Extensions/hs9510VFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/opt9600VFD/Makefile
lib/python/Plugins/Extensions/opt9600VFD/meta/Makefile
lib/python/Plugins/Extensions/opt9600VFD/locale/Makefile
lib/python/Plugins/Extensions/opt9600VFD/locale/nl/Makefile
lib/python/Plugins/Extensions/opt9600VFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/pace7241VFD/Makefile
lib/python/Plugins/Extensions/pace7241VFD/meta/Makefile
lib/python/Plugins/Extensions/pace7241VFD/locale/Makefile
lib/python/Plugins/Extensions/pace7241VFD/locale/nl/Makefile
lib/python/Plugins/Extensions/pace7241VFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/sparkVFD/Makefile
lib/python/Plugins/Extensions/sparkVFD/meta/Makefile
lib/python/Plugins/Extensions/sparkVFD/locale/Makefile
lib/python/Plugins/Extensions/sparkVFD/locale/nl/Makefile
lib/python/Plugins/Extensions/sparkVFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/spark7162VFD/Makefile
lib/python/Plugins/Extensions/spark7162VFD/meta/Makefile
lib/python/Plugins/Extensions/spark7162VFD/locale/Makefile
lib/python/Plugins/Extensions/spark7162VFD/locale/nl/Makefile
lib/python/Plugins/Extensions/spark7162VFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/ufs9xxVFD/Makefile
lib/python/Plugins/Extensions/ufs9xxVFD/meta/Makefile
lib/python/Plugins/Extensions/ufs9xxVFD/locale/Makefile
lib/python/Plugins/Extensions/ufs9xxVFD/locale/nl/Makefile
lib/python/Plugins/Extensions/ufs9xxVFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/hchsxx00VFD/Makefile
lib/python/Plugins/Extensions/hchsxx00VFD/meta/Makefile
lib/python/Plugins/Extensions/hchsxx00VFD/locale/Makefile
lib/python/Plugins/Extensions/hchsxx00VFD/locale/nl/Makefile
lib/python/Plugins/Extensions/hchsxx00VFD/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/SystemPlugins/VFD-Icons/Makefile
lib/python/Plugins/SystemPlugins/VFD-Icons/meta/Makefile
lib/python/Tools/Makefile
po/Makefile
main/Makefile
tools/Makefile
tools/enigma2.sh
enigma2.pc
])
AC_OUTPUT
