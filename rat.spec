Summary:	Robust-Audio Tool
Name:		rat-step-alsa
Version:	3.0.23
Release:	1
Source0:	rat-3.0.23.tar.gz
Source10:	tcl8.0p2.tar.gz
Source11:	tk8.0p2.tar.gz
#Source12:	TkInterStep-1.5a4-p2.tar.gz
Source13:	tk8.0p2-to-TkStep8.0p2.patch.gz
Source20:	auddev_linux_alsa.c
Patch0:		rat-3.0.23.patch
License:	GPL
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe

%description
RAT for MBONE

%prep
%setup -q -n rat-3.0
%patch -p0
mkdir tcltk
tar x -C tcltk -vvzf $RPM_SOURCE_DIR/tcl8.0p2.tar.gz
tar x -C tcltk -vvzf $RPM_SOURCE_DIR/tk8.0p2.tar.gz
#tar x -C tcltk -vvzf $RPM_SOURCE_DIR/TkInterStep-1.5a4-p2.tar.gz
cd tcltk; zcat $RPM_SOURCE_DIR/tk8.0p2-to-TkStep8.0p2.patch.gz | patch -p0; cd ..
cp -avf $RPM_SOURCE_DIR/auddev_linux_alsa.c src/auddev_linux.c

%build
cd tcltk/tcl8.0p2/unix
LDFLAGS="-s"; export LDFLAGS
%configure \
	--enable-gcc

%{__make}
mkdir -p ../lib
cd ../lib
mkdir -p include lib
cd include
ln -s ../../generic/tcl.h
cd ../lib
ln -s ../../unix/libtcl8.0.a libtcl.a
ln -s ../../library tcl
cd ../../../..

cd tcltk/tk8.0p2/unix
autoconf
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} \
        --with-tcl=../../tcl8.0p2/unix \
        --enable-gcc \
        --enable-step \
        --enable-xpm \
        --enable-tiff
%{__make} -j3
mkdir -p ../lib
cd ../lib
mkdir -p include lib
cd include
ln -s ../../generic/tk.h
cd ../lib
ln -s ../../unix/libtkstep8.0.a libtk.a
ln -s ../../library tk
cd ../../../..

# let build script create directories
./Build fake
#
export OSTYPE=Linux
export OSMVER=`uname -r | awk -F. '{printf("%d_%d", $1, $2)}'`
export OSVERS=`uname -r`
%{__make} OSTYPE=Linux \
	OSMVER=$OSMVER \
	OSVERS=$OSVERS \
	USER=root1 \
	'INCS=-Itcltk/tcl8.0p2/lib/include -Itcltk/tk8.0p2/lib/include' \
	'LDLIBS=-static -Ltcltk/tcl8.0p2/lib/lib -Ltcltk/tk8.0p2/lib/lib -ltk -ltcl -L%{_prefix}/X11R6/lib -lX11 -lXpm -ltiff -lm -ldl -lasound' \
	bin/root1/rat-Linux-$OSVERS

%install
rm -rf $RPM_BUILD_ROOT
install -s -o root bin/root1/rat-Linux-* %{_bindir}/rat

%files
%defattr(644,root,root,755)
%doc COPYRIGHT MODS README README.qfdes
%attr(-,root,root) %{_bindir}/rat
