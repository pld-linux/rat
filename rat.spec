%define		_commonlibver	1.2.8
Summary:	Audio conference tool
Summary(pl):	Narzêdzie do audio-konferencji
Name:		rat
Version:	4.2.18
Release:	2
License:	Custom
Group:		X11/Applications/Multimedia
Group(de):	X11/Applikationen/Multimedia
Group(pl):	X11/Aplikacje/Multimedia
Source0:	http://www-mice.cs.ucl.ac.uk/multimedia/software/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-FHS_DESTDIR.patch
URL:		http://www-mice.cs.ucl.ac.uk/multimedia/software/
BuildRequires:	tcl-devel >= 8.3
BuildRequires:	tk-devel >= 8.3
BuildRequires:	alsa-lib-static
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define 	_commonlibdir	/usr/lib
%define 	_commonincludedir /usr/include/ucl

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

%description -l pl
RAT (Robust-Audio Tool) jest programem pozwalaj±cym u¿ytkownikom braæ
udzia³ w konferencjach audio w Internecie. Mog± sie one odbywaæ
pomiêdzy dwoma uczestnikami bezpo¶rednio lub pomiêdzy uczestnikami
grupy multicast'owej. Do u¿ywania RAT w trybie punkt-punkt nie jest
potrzebna ¿adna specjalna konfiguracja, lecz aby ko¿ystaæ z mo¿liwo¶ci
konferencji multicast'owej, przy³±cze do sieci MBone lub podobnej jest
wymagane. RAT oparty jest na standardach IETF, u¿ywa RTP po UDP/IP
jako protokó³ transportowy i jest zgodny z profilem RTP dotycz±cym
konferencji audio i video z minimaln± kontrol±.

%package -n ucl-common-devel
Summary:	UCL Common Code Library
Summary(pl):	Biblioteka u¿ywana przez multimedialne narzêdzia UCL
Version:	1.2.8
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki

%description -n ucl-common-devel
Routines common to a number of multimedia tools like sdr, nte or wbd.
This package is needed only for compiling them.

%description -l pl -n ucl-common-devel
Procedury u¿ywane przez kilka narzêdzi multimedialnych, takich jak
sdr, nte czy wbd. Pakiet ten jest potrzebny wy³±cznie do ich
skompilowania.

%prep
%setup -q
%patch0 -p1

%build
cd common
aclocal
autoconf
%configure \
	--enable-ipv6 
%{__make}

cd ../%{name}
%configure2_13 \
	--with-tcltk-version=8.3 \
	--with-tcl=/usr \
	--with-tk=/usr \
	--enable-ipv6 \
	%{!?debug:--enable-optimize} \
	%{?debug:--enable-debug} 
#	--with-common=/usr/include/ucl 
%{__make} EXTERNAL_DEP=""
	

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_commonlibdir},%{_commonincludedir}}
install common/src/lib*.a $RPM_BUILD_ROOT%{_commonlibdir}
install common/src/*.h $RPM_BUILD_ROOT%{_commonincludedir}
gzip -nf common/{MODS,COPYRIGHT,README}

cd rat
%{__make} install DESTDIR=$RPM_BUILD_ROOT
gzip -9nf README* COPYRIGHT MODS 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc rat/MODS* rat/README* rat/COPYRIGHT*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sdr/plugins/*

%files -n ucl-common-devel
%defattr(644,root,root,755)
%doc common/MODS* common/COPYRIGHT* common/README*
%doc common/doc/html/*.html
%{_commonlibdir}/*
%{_commonincludedir}
