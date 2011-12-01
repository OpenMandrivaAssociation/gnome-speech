%define lib_major 7
%define libname %mklibname gnomespeech %{lib_major}
%define libnamedev %mklibname -d gnomespeech
%define last_abi_break_version 0.3.2

%ifarch %arm %mips
%define build_java 0
%else
%define build_java 1
%endif

Summary: Simple general API for producing text-to-speech output
Name: gnome-speech
Version: 0.4.25
Release: %mkrel 5
License: LGPLv2+
Group: Accessibility
URL: http://developer.gnome.org/projects/gap/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libbonobo-activation-devel
BuildRequires: libespeak-devel
BuildRequires: autoconf2.5
BuildRequires: gnome-common
BuildRequires: popt-devel
%if %{build_java}
BuildRequires: java-access-bridge
BuildRequires: java-devel java-rpmbuild
%endif
Obsoletes: gnome_speech
Provides: gnome_speech = %{version}-%{release}
Requires: %name-driver = %version

%description
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

%package -n %{libname}
Summary:	 Simple general API for producing text-to-speech output
Group:		System/Libraries

Provides:	lib%{name} = %{version}-%{release}
Requires:   %{name} >= %{version}-%{release}


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
Requires:   libbonobo2_x-devel
Conflicts:  lib%{name}-devel < %{last_abi_break_version}
Obsoletes: %mklibname -d gnomespeech 7

%description -n %{libnamedev}
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

%package driver-festival
Summary: Backend for gnome-speech based on festival
Group: System/Libraries
Provides: %name-driver = %version
Requires: festival

%description driver-festival
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

This is a backend for %name based on festival.

%package driver-espeak
Summary: Backend for gnome-speech based on espeak
Group: System/Libraries
Provides: %name-driver = %version
Requires: soundwrapper

%description driver-espeak
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

This is a backend for %name based on espeak.

%prep
%setup -q

%build

%if %{build_java}
%configure2_5x --with-jab-dir=%_datadir/java --with-java-home=%java_home
%else
%configure2_5x
%endif

%make

%install
rm -rf %{buildroot}

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
mv %buildroot%_datadir/jar %buildroot%_datadir/java
%endif

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
  
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc README ChangeLog AUTHORS
%{_bindir}/test-speech
%{_datadir}/idl/*
%{_libdir}/orbit-2.0/*.so
%if %{build_java}
%_datadir/java/gnome-speech.jar
%endif

%files driver-festival
%defattr(-,root,root,-)
%_bindir/festival-synthesis-driver
%_libdir/bonobo/servers/GNOME_Speech_SynthesisDriver_Festival.server

%files driver-espeak
%defattr(-,root,root,-)
%_bindir/espeak-synthesis-driver*
%_libdir/bonobo/servers/GNOME_Speech_SynthesisDriver_Espeak.server

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/*.so.%{lib_major}*

%files -n %{libnamedev}
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/pkgconfig/*
