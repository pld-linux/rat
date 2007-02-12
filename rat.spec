#
# Conditional build:
%bcond_with	alsa		# with ALSA support (0.5 only)
#
%define		_commonlibver	1.2.16
Summary:	Audio conference tool
Summary(pl.UTF-8):   Narzędzie do audio-konferencji
Name:		rat
Version:	4.2.25
Release:	2
License:	BSD-like
Group:		X11/Applications/Sound
Source0:	http://www-mice.cs.ucl.ac.uk/multimedia/software/rat/releases/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d959a507b27573f80511fd6739b33514
Patch0:		%{name}-FHS_DESTDIR.patch
Patch1:		%{name}-ipv6.patch
Patch2:		%{name}-common-shared.patch
Patch3:		%{name}-acfix.patch
Patch4:		%{name}-alsa.patch
Patch5:		%{name}-tcl.patch
Patch6:		%{name}-types.patch
Patch7:		%{name}-Werror.patch
URL:		http://www-mice.cs.ucl.ac.uk/multimedia/software/rat/
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	tcl-devel >= 8.4
BuildRequires:	tk-devel >= 8.4
BuildRequires:	ucl-common-devel >= %{_commonlibver}
Requires:	ucl-common >= %{_commonlibver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_commonincludedir	/usr/include/ucl

%description
RAT (Robust-Audio Tool) is a network audio tool that allows users to
particpate in audio conferences over the internet. These can be
between two participants directly, or between a group of participants
on a common multicast group. No special features are required to use
RAT in point-to-point mode, but to use the multicast conferencing
facilities of RAT, a connection to the Mbone, or a similar multicast
capable network, is required. RAT is based on IETF standards, using
RTP above UDP/IP as its transport protocol, and conforming to the RTP
profile for audio and video conferences with minimal control.

%description -l pl.UTF-8
RAT (Robust-Audio Tool) jest programem pozwalającym użytkownikom brać
udział w konferencjach audio w Internecie. Mogą sie one odbywać
pomiędzy dwoma uczestnikami bezpośrednio lub pomiędzy uczestnikami
grupy multicastowej. Do używania RAT w trybie punkt-punkt nie jest
potrzebna żadna specjalna konfiguracja, lecz aby korzystać z
możliwości konferencji multicastowej, przyłącze do sieci MBone lub
podobnej jest wymagane. RAT oparty jest na standardach IETF, używa RTP
po UDP/IP jako protokół transportowy i jest zgodny z profilem RTP
dotyczącym konferencji audio i video z minimalną kontrolą.

%package -n ucl-common
Summary:	UCL Common Code Library
Summary(pl.UTF-8):   Biblioteka wspólnego kodu UCL
Version:	%{_commonlibver}
Group:		Libraries

%description -n ucl-common
Routines common to a number of multimedia tools like sdr, nte or wbd.
The library originates from work on the RAT project: these are
portions that are not directly related to an audio tool and
potentially useful elsewhere.

%description -n ucl-common -l pl.UTF-8
Procedury używane przez kilka narzędzi multimedialnych, takich jak
sdr, nte czy wbd. Biblioteka ta wywodzi się z prac nad projektem RAT,
ale jej częsci nie są związane wyłącznie z narzędziami do dźwięku i
mogą być przydatne do innych celów.

%package -n ucl-common-devel
Summary:	Header files for UCL Common Code Library
Summary(pl.UTF-8):   Pliki nagłówkowe do biblioteki wspólnego kodu UCL
Version:	%{_commonlibver}
Group:		Development/Libraries
Requires:	ucl-common = %{_commonlibver}

%description -n ucl-common-devel
Header files for UCL Common Code Library.

%description -n ucl-common-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki wspólnego kodu UCL.

%package -n ucl-common-static
Summary:	UCL Common Code static library
Summary(pl.UTF-8):   Statyczna biblioteka wspólnego kodu UCL
Group:		Development/Libraries
Requires:	ucl-common-devel = %{_commonlibver}

%description -n ucl-common-static
UCL Common Code static library.

%description -n ucl-common-static -l pl.UTF-8
Statyczna biblioteka wspólnego kodu UCL.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
cd common
cp -f /usr/share/automake/config.* .
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--enable-ipv6 \
	--includedir=%{_commonincludedir}
%{__make}
cd ../rat
cp -f /usr/share/automake/config.* .
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--with-tcltk-version=8.4 \
	--with-tcl=/usr \
	--with-tk=/usr \
	--enable-ipv6 \
	%{!?debug:--enable-optimize} \
	%{?debug:--enable-debug} \
	%{!?with_alsa:--without-alsa}
#	--with-common=/usr/include/ucl
%{__make} \
	EXTERNAL_DEP=""

%install
rm -rf $RPM_BUILD_ROOT

%if 0
%{__make} -C common/src install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C rat install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n ucl-common -p /sbin/ldconfig
%postun	-n ucl-common -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc rat/MODS* rat/README* rat/COPYRIGHT*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%dir %{_sysconfdir}/sdr
%dir %{_sysconfdir}/sdr/plugins
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sdr/plugins/*

%if 0
%files -n ucl-common
%defattr(644,root,root,755)
%doc common/{COPYRIGHT,MODS,README,src/README.qfdes}
%attr(755,root,root) %{_libdir}/libuclmmbase.so.*.*.*

%files -n ucl-common-devel
%defattr(644,root,root,755)
%doc common/doc/html/*.html
%attr(755,root,root) %{_libdir}/libuclmmbase.so
%{_libdir}/libuclmmbase.la
%{_commonincludedir}

%files -n ucl-common-static
%defattr(644,root,root,755)
%{_libdir}/libuclmmbase.a
%endif
