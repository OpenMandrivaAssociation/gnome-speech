%define url_ver %(echo %{version}|cut -d. -f1,2)

%define major	7
%define libname %mklibname gnomespeech %{major}
%define devname %mklibname -d gnomespeech

%ifarch %arm %mips
%define build_java 0
%else
%define build_java 1
%endif

Summary:	Simple general API for producing text-to-speech output
Name:		gnome-speech
Version:	0.4.25
Release:	7
License:	LGPLv2+
Group:		Accessibility
Url:		http://developer.gnome.org/projects/gap/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/gnome-speech/%{url_ver}/%{name}-%{version}.tar.bz2
Patch0:		gnome-speech-0.4.25-glib.patch
BuildRequires:	espeak-devel
BuildRequires:	gnome-common
BuildRequires:	pkgconfig(bonobo-activation-2.0)
BuildRequires:	pkgconfig(popt)
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
Suggests:	%{name} >= %{version}-%{release}

%description -n %{libname}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development library, include files for gnome_speech
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libgnomespeech-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

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
%apply_patches

%build
%configure2_5x \
%if %{build_java}
	--with-jab-dir=%{_datadir}/java \
	--with-java-home=%{java_home}
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
%{_libdir}/libgnomespeech.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

