Summary: Robust-Audio Tool
Name: rat-step-alsa
Version: 3.0.23
Release: 1
Source: rat-3.0.23.tar.gz
Source10: tcl8.0p2.tar.gz
Source11: tk8.0p2.tar.gz
#Source12: TkInterStep-1.5a4-p2.tar.gz
Source13: tk8.0p2-to-TkStep8.0p2.patch.gz
Source20: auddev_linux_alsa.c
Patch: rat-3.0.23.patch
Copyright: GPL
Group: Applications/Networking
Packager: Jaroslav Kysela <perex@jcu.cz>

%description
RAT for MBONE

%prep
%setup -n rat-3.0
%patch -p0
mkdir tcltk
tar x -C tcltk -vvzf $RPM_SOURCE_DIR/tcl8.0p2.tar.gz
tar x -C tcltk -vvzf $RPM_SOURCE_DIR/tk8.0p2.tar.gz
#tar x -C tcltk -vvzf $RPM_SOURCE_DIR/TkInterStep-1.5a4-p2.tar.gz
cd tcltk; zcat $RPM_SOURCE_DIR/tk8.0p2-to-TkStep8.0p2.patch.gz | patch -p0; cd ..
cp -avf $RPM_SOURCE_DIR/auddev_linux_alsa.c src/auddev_linux.c

%build
cd tcltk/tcl8.0p2/unix
CFLAGS="$RPM_OPT_FLAGS" \
./configure %{_target_platform} \
	--prefix=/usr \
	--enable-gcc
make -j3
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
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr \
        --with-tcl=../../tcl8.0p2/unix \
        --enable-gcc \
        --enable-step \
        --enable-xpm \
        --enable-tiff
make -j3
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
make OSTYPE=Linux \
     OSMVER=$OSMVER \
     OSVERS=$OSVERS \
     USER=root1 \
     'INCS=-Itcltk/tcl8.0p2/lib/include -Itcltk/tk8.0p2/lib/include' \
     'LDLIBS=-static -Ltcltk/tcl8.0p2/lib/lib -Ltcltk/tk8.0p2/lib/lib -ltk -ltcl -L/usr/X11R6/lib -lX11 -lXpm -ltiff -lm -ldl -lasound' \
     bin/root1/rat-Linux-$OSVERS

%install
install -s -o root -g root bin/root1/rat-Linux-* %{_bindir}/rat

%files
%doc COPYRIGHT MODS README README.qfdes
%attr(-,root,root) %{_bindir}/rat
