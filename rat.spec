Summary:	Robust-Audio Tool
Name:		rat
Version:	4.2.18
Release:	1
Group:		X11/Applications/Multimedia
Group(de):	X11/Applikationen/Multimedia
Group(pl):	X11/Aplikacje/Multimedia
Source0:	http://www-mice.cs.ucl.ac.uk/multimedia/software/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-FHS_DESTDIR.patch
URL:		http://www-mice.cs.ucl.ac.uk/multimedia/software/
License:	Custom
BuildRequires:	tcl-devel >= 8.3
BuildRequires:	tk-devel >= 8.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix	/usr/X11R6

%description
RAT is a network audio tool that allows users to particpate in audio
conferences over the internet. These can be between two participants
directly, or between a group of participants on a common multicast
group. No special features are required to use RAT in point-to-point
mode, but to use the multicast conferencing facilities of RAT, a
connection to the Mbone, or a similar multicast capable network, is
required. RAT is based on IETF standards, using RTP above UDP/IP as
its transport protocol, and conforming to the RTP profile for audio
and video conferences with minimal control.

%prep
%setup -q
%patch0 -p1

%build
cd common
%configure \
	--enable-ipv6 
%{__make}

cd ../%{name}
%configure \
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
