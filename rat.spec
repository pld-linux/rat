Summary:	UCL Network Text Editor
Name:		rat
Version:	4.2.18
Release:	1
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://www-mice.cs.ucl.ac.uk/multimedia/software/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-FHS_DESTDIR.patch
URL:		http://www-mice.cs.ucl.ac.uk/multimedia/software/
License:	Custom
BuildRequires:	tcl-devel >= 8.3
BuildRequires:	tk-devel >= 8.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix	/usr/X11R6

%description
NTE is a shared text editor designed for use on the Mbone.

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
%doc rat/CHANGES* rat/KNOWN_BUGS* rat/CHANGES*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sdr/plugins/*
