%define lib_major 7
%define libname %mklibname gnomespeech %{lib_major}
%define libnamedev %mklibname -d gnomespeech
%define last_abi_break_version 0.3.2

Summary: Simple general API for producing text-to-speech output
Name: gnome-speech
Version: 0.4.17
Release: %mkrel 1
License: LGPL
Group: Accessibility
URL: http://developer.gnome.org/projects/gap/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libbonobo-activation-devel
BuildRequires: libespeak-devel
BuildRequires: autoconf2.5
BuildRequires: gnome-common
Obsoletes: gnome_speech
Provides: gnome_speech = %{version}-%{release}
Requires: %name-driver = %version

%description
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

%package -n %{libname}
Summary:	 Simple general API for producing text-to-speech output
Group:		%{group}

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

%description driver-espeak
This is GNOME Speech.  It's purpose is to provide a
simple general API for producing text-to-speech output.

This is a backend for %name based on espeak.

%prep
%setup -q

%build

%configure2_5x

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
  
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README ChangeLog AUTHORS
%{_bindir}/test-speech
%{_datadir}/idl/*
%{_libdir}/orbit-2.0/*.so

%files driver-festival
%defattr(-,root,root,-)
%_bindir/festival-synthesis-driver
%_libdir/bonobo/servers/GNOME_Speech_SynthesisDriver_Festival.server

%files driver-espeak
%defattr(-,root,root,-)
%_bindir/espeak-synthesis-driver
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
