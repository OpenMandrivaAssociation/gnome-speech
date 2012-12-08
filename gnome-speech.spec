%define lib_major 7
%define libname %mklibname gnomespeech %{lib_major}
%define libnamedev %mklibname -d gnomespeech

%ifarch %arm %mips
%define build_java 0
%else
%define build_java 1
%endif

Summary:	Simple general API for producing text-to-speech output
Name:		gnome-speech
Version:	0.4.25
Release:	6
License:	LGPLv2+
Group:		Accessibility
URL:		http://developer.gnome.org/projects/gap/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0:		gnome-speech-0.4.25-glib.patch
BuildRequires:	pkgconfig(bonobo-activation-2.0)
BuildRequires:	libespeak-devel
BuildRequires:	autoconf2.5
BuildRequires:	gnome-common
BuildRequires:	popt-devel
%if %{build_java}
BuildRequires:	java-access-bridge
BuildRequires:	java-devel
BuildRequires:	java-rpmbuild
%endif
Provides:	gnome_speech = %{version}-%{release}
Requires:	%{name}-driver = %{version}-%{release}

%description
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

%package -n %{libname}
Summary:	Simple general API for producing text-to-speech output
Group:		System/Libraries

Provides:	lib%{name} = %{version}-%{release}
Requires:	%{name} >= %{version}-%{release}


%description -n %{libname}
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

%package -n %{libnamedev}
Summary:	Static libraries, include files for gnome_speech
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	libgnomespeech-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{libnamedev}
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

%package driver-festival
Summary:	Backend for gnome-speech based on festival
Group:		System/Libraries
Provides:	%{name}-driver = %{version}-%{release}
Requires:	festival

%description driver-festival
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

This is a backend for %{name} based on festival.

%package driver-espeak
Summary:	Backend for gnome-speech based on espeak
Group:		System/Libraries
Provides:	%{name}-driver = %{version}-%{release}
Requires:	soundwrapper

%description driver-espeak
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

This is a backend for %{name} based on espeak.

%prep
%setup -q
%patch0 -p1

%build
%if %{build_java}
%configure2_5x --with-jab-dir=%{_datadir}/java --with-java-home=%{java_home}
%else
%configure2_5x
%endif

%make

%install
%makeinstall_std

# replace espeak driver with wrapper which calls soundwrapper if needed
mv %{buildroot}%{_bindir}/espeak-synthesis-driver %{buildroot}%{_bindir}/espeak-synthesis-driver.bin

cat << EOF >  %{buildroot}%{_bindir}/espeak-synthesis-driver
#!/bin/sh
/usr/bin/soundwrapper /usr/bin/espeak-synthesis-driver.bin \$@
EOF
chmod 755 %{buildroot}%{_bindir}/espeak-synthesis-driver

# remove unpackaged files
rm -f %{buildroot}%{_libdir}/orbit-2.0/*.la

%if %{build_java}
#gw I think this dir is more appropiate
mv %{buildroot}%{_datadir}/jar %{buildroot}%{_datadir}/java
%endif

%files
%doc README ChangeLog AUTHORS
%{_bindir}/test-speech
%{_datadir}/idl/*
%{_libdir}/orbit-2.0/*.so
%if %{build_java}
%{_datadir}/java/gnome-speech.jar
%endif

%files driver-festival
%{_bindir}/festival-synthesis-driver
%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_Festival.server

%files driver-espeak
%{_bindir}/espeak-synthesis-driver*
%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_Espeak.server

%files -n %{libname}
%{_libdir}/*.so.%{lib_major}*

%files -n %{libnamedev}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.25-5mdv2011.0
+ Revision: 664885
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.25-4mdv2011.0
+ Revision: 605474
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.25-3mdv2010.1
+ Revision: 521514
- fix deps
- rebuilt for 2010.1

* Fri Sep 25 2009 Olivier Blin <oblin@mandriva.com> 0.4.25-2mdv2010.0
+ Revision: 448972
- disable java on arm & mips (from Arnaud Patard)

* Sun Feb 15 2009 Götz Waschk <waschk@mandriva.org> 0.4.25-1mdv2009.1
+ Revision: 340568
- update to new version 0.4.25

* Mon Feb 02 2009 Götz Waschk <waschk@mandriva.org> 0.4.23-1mdv2009.1
+ Revision: 336491
- new version

* Mon Nov 17 2008 Götz Waschk <waschk@mandriva.org> 0.4.22-1mdv2009.1
+ Revision: 303856
- update to new version 0.4.22

* Mon Aug 04 2008 Götz Waschk <waschk@mandriva.org> 0.4.21-1mdv2009.0
+ Revision: 262915
- new version
- update license

* Tue Jun 17 2008 Götz Waschk <waschk@mandriva.org> 0.4.20-2mdv2009.0
+ Revision: 223325
- bump release
- fix java home dir (Anssi)
- new version
- hardcode path to openjdk java home so it finds idlj

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Apr 18 2008 Götz Waschk <waschk@mandriva.org> 0.4.19-1mdv2009.0
+ Revision: 195529
- new version

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 0.4.18-3mdv2008.1
+ Revision: 189628
- Fix lib group

* Thu Mar 13 2008 Frederic Crozat <fcrozat@mandriva.com> 0.4.18-2mdv2008.1
+ Revision: 187573
- Add soundwrapper call to espeak driver

* Mon Jan 14 2008 Götz Waschk <waschk@mandriva.org> 0.4.18-1mdv2008.1
+ Revision: 151229
- new version
- add java binding

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Götz Waschk <waschk@mandriva.org> 0.4.17-1mdv2008.1
+ Revision: 131077
- new version
- new devel name

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Jul 30 2007 Götz Waschk <waschk@mandriva.org> 0.4.16-1mdv2008.0
+ Revision: 56480
- new version

* Mon Jul 09 2007 Götz Waschk <waschk@mandriva.org> 0.4.15-1mdv2008.0
+ Revision: 50564
- new version

* Mon Jun 18 2007 Götz Waschk <waschk@mandriva.org> 0.4.14-1mdv2008.0
+ Revision: 40694
- new version

* Mon Jun 04 2007 Götz Waschk <waschk@mandriva.org> 0.4.13-1mdv2008.0
+ Revision: 35145
- new version

* Mon May 14 2007 Götz Waschk <waschk@mandriva.org> 0.4.12-1mdv2008.0
+ Revision: 26735
- new version

* Tue Apr 17 2007 Götz Waschk <waschk@mandriva.org> 0.4.11-1mdv2008.0
+ Revision: 14038
- new version


* Sun Feb 25 2007 Götz Waschk <waschk@mandriva.org> 0.4.10-1mdv2007.0
+ Revision: 125666
- new version

* Mon Feb 12 2007 Götz Waschk <waschk@mandriva.org> 0.4.9-1mdv2007.1
+ Revision: 118850
- new version

* Tue Jan 30 2007 Götz Waschk <waschk@mandriva.org> 0.4.8-3mdv2007.1
+ Revision: 115387
- remove drivers from the main package

* Mon Jan 29 2007 Götz Waschk <waschk@mandriva.org> 0.4.8-2mdv2007.1
+ Revision: 115033
- add espeak driver

* Sat Jan 20 2007 Götz Waschk <waschk@mandriva.org> 0.4.8-1mdv2007.1
+ Revision: 111055
- new version

* Fri Dec 15 2006 Götz Waschk <waschk@mandriva.org> 0.4.7-1mdv2007.1
+ Revision: 97321
- new version
- drop obsolete patch

* Mon Nov 06 2006 Götz Waschk <waschk@mandriva.org> 0.4.6-1mdv2007.1
+ Revision: 76830
- Import gnome-speech

* Mon Nov 06 2006 Götz Waschk <waschk@mandriva.org> 0.4.6-1mdv2007.1
- New version 0.4.6

* Wed Aug 30 2006 Götz Waschk <waschk@mandriva.org> 0.4.5-1mdv2007.0
- New release 0.4.5

* Wed Aug 23 2006 Götz Waschk <waschk@mandriva.org> 0.4.4-1mdv2007.0
- New release 0.4.4

* Tue Aug 08 2006 Götz Waschk <waschk@mandriva.org> 0.4.3-1mdv2007.0
- New release 0.4.3

* Tue Jul 25 2006 Götz Waschk <waschk@mandriva.org> 0.4.2-1
- New release 0.4.2

* Tue Jul 11 2006 Götz Waschk <waschk@mandriva.org> 0.4.1-1mdv2007.0
- New release 0.4.1

* Mon May 15 2006 Götz Waschk <waschk@mandriva.org> 0.4.0-1mdk
- New release 0.4.0

* Thu Feb 23 2006 Götz Waschk <waschk@mandriva.org> 0.3.10-1mdk
- New release 0.3.10
- use mkrel

* Sat Oct 08 2005 Frederic Crozat <fcrozat@mandriva.com> 0.3.8-1mdk
- Release 0.3.8
- Remove patch1 (merged upstream)

* Wed Jul 13 2005 Frederic Crozat <fcrozat@mandriva.com> 0.3.7-2mdk 
- Patch1 (CVS): fix crash with festival (Mdk bug #16458)

* Thu May 12 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 0.3.7-1mdk
- New release 0.3.7

* Thu Feb 17 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 0.3.6-1mdk 
- Release 0.3.6
- Remove patch1 (no longer needed)

* Wed Oct 20 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.3.5-1mdk
- New release 0.3.5
- Fix java detection

* Fri May 14 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.3.2-3mdk
- fix devel requires (sync with AMD64)

* Thu Apr 08 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.3.2-2mdk
- Add conflicts to easy upgrading

* Wed Apr 07 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.3.2-1mdk
- Release 0.3.2

