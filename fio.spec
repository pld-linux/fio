# TODO:
# - HDFS (hadoop, --enable-libhdfs, requires also java)
# - fusion-aw (nvm-primitives): http://opennvm.github.io/
#
# Conditional build:
%bcond_with	ceph		# RBD (CephFS) support
%bcond_without	glusterfs	# GFAPI support
%bcond_without	gtk		# GTK+ based GUI (gfio)
%bcond_without	numa		# NUMA support
#
Summary:	I/O tool for benchmark and stress/hardware verification
Summary(pl.UTF-8):	Narzędzie do mierzenia wydajności I/O i sprawdzania sprawności sprzętu
Name:		fio
Version:	2.19
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://brick.kernel.dk/snaps/%{name}-%{version}.tar.bz2
# Source0-md5:	83275de968ca2c5e9429e7b83710d20e
Patch0:		%{name}-guasi.patch
URL:		http://git.kernel.dk/?p=fio.git;a=summary
BuildRequires:	bison
%{?with_ceph:BuildRequires:	ceph-devel}
BuildRequires:	flex
%{?with_glusterfs:BuildRequires:	glusterfs-devel}
BuildRequires:	guasi-devel
BuildRequires:	libaio-devel
BuildRequires:	libibverbs-devel
BuildRequires:	librdmacm-devel
BuildRequires:	numactl-devel
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
%if %{with gtk}
BuildRequires:	cairo-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 2:2.18.0
BuildRequires:	pkgconfig
%endif
# x86 features detection relies on cpuid
ExcludeArch:	i386 i486
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
fio is an I/O tool meant to be used both for benchmark and
stress/hardware verification. It has support for 9 different types of
I/O engines (sync, mmap, libaio, posixaio, SG v3, splice, null,
network, syslet), I/O priorities (for newer Linux kernels), rate I/O,
forked or threaded jobs, and much more. It can work on block devices
as well as files. fio accepts job descriptions in a
simple-to-understand text format. Several example job files are
included. fio displays all sorts of I/O performance information. It
supports Linux, FreeBSD, and OpenSolaris.

%description -l pl.UTF-8
fio to narzędzie do mierzenia wydajności I/O oraz sprawdzania
sprawności sprzętu pod dużym obciążeniem. Obsługuje 9 różnych rodzajów
silników I/O (sync, mmap, libaio, posixaio, SG v3, splice, null,
network, syslet), priorytety I/O (dla nowszych jąder Linuksa),
przepustowość I/O, zadania wieloprocesowe lub wielowątkowe i wiele
więcej. Może działać na urządzeniach blokowych oraz na plikach. fio
przyjmuje opisy zadań w formacie tekstowym prostym do zrozumienia. Ma
załączone kilka przykładowych plików zadań. Wyświetla wszystkie
rodzaje informacji o wydajności I/O. Obsługuje Linuksa, FreeBSD i
OpenSolarisa.

%package devel
Summary:	Header files for developing FIO engine modules
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia modułów silników FIO
Group:		Development/Libraries
# doesn't require base

%description devel
Header files for developing FIO engine modules.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia modułów silników FIO.

%package -n gfio
Summary:	GTK+ based graphical front-end for fio
Summary(pl.UTF-8):	Oparty na GTK+ graficzny interfejs do fio
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description -n gfio
gfio is a GTK+ based graphical front-end for fio. It is often
installed on the testers workstation whereas fio would be installed on
the server.

%description -n gfio -l pl.UTF-8
gfio to oparty na GTK+ graficzny interfejs do fio. Zwykle jest
instalowany na komputerze testerów, podczas gdy fio jest zainstalowany
na serwerze.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' tools/genfio
%{__sed} -i -e '1s,/usr/bin/env python,/usr/bin/python,' tools/plot/fio2gnuplot

%build
./configure \
	--cc="%{__cc}" \
	--extra-cflags="%{rpmcflags} %{rpmcppflags}" \
	%{!?with_glusterfs:--enable-gfapi} \
	%{?with_gtk:--enable-gfio} \
	%{!?with_numa:--disable-numa} \
	%{!?with_ceph:--disable-rbd} \

%{__make} \
	LDFLAGS="%{rpmldflags}" \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix="%{_prefix}" \
	mandir="%{_mandir}" \
	DESTDIR=$RPM_BUILD_ROOT

# development files for fio modules
install -d $RPM_BUILD_ROOT%{_includedir}/fio/{arch,compiler,engines,lib,os,oslib}
cp -p client.h config-host.h debug.h diskutil.h fifo.h file.h fio.h fio_time.h flist.h flow.h gettime.h helper_thread.h helpers.h io_ddir.h io_u.h io_u_queue.h ioengines.h iolog.h json.h log.h minmax.h mutex.h options.h parse.h profile.h server.h stat.h steadystate.h td_error.h thread_options.h workqueue.h $RPM_BUILD_ROOT%{_includedir}/fio
cp -p arch/arch.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%ifarch %{ix86} %{x8664} x32
cp -p arch/arch-x86.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch %{x8664} x32
cp -p arch/arch-x86_64.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch %{ix86} %{x8664} x32
cp -p arch/arch-x86-common.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch ppc ppc64
cp -p arch/arch-ppc.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch ia64
cp -p arch/arch-ia64.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch alpha
cp -p arch/arch-ia64.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch s390 s390x
cp -p arch/arch-s390.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch sparc sparcv9 sparc64
cp -p arch/arch-sparc.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch sparc64
cp -p arch/arch-sparc64.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch arm aarch64
cp -p arch/arch-arm.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch mips
cp -p arch/arch-mips.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch sh
cp -p arch/arch-sh.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch hppa
cp -p arch/arch-hppa.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifarch aarch64
cp -p arch/arch-aarch64.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
%ifnarch %{ix86} %{x8664} x32 ppc ppc64 ia64 alpha s390 s390x sparc sparcv9 sparc64 arm mips sh hppa aarch64
cp -p arch/arch-generic.h $RPM_BUILD_ROOT%{_includedir}/fio/arch
%endif
cp -p compiler/{compiler,compiler-gcc*}.h $RPM_BUILD_ROOT%{_includedir}/fio/compiler
cp -p lib/{axmap,ffz,gauss,ieee754,lfsr,output_buffer,pattern,rand,rbtree,types,zipf}.h $RPM_BUILD_ROOT%{_includedir}/fio/lib
cp -p os/{binject,os,os-linux,os-linux-syscall}.h $RPM_BUILD_ROOT%{_includedir}/fio/os
cp -p oslib/{getopt,strlcat}.h $RPM_BUILD_ROOT%{_includedir}/fio/oslib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO MORAL-LICENSE README REPORTING-BUGS SERVER-TODO examples
%attr(755,root,root) %{_bindir}/fio
%attr(755,root,root) %{_bindir}/fio-btrace2fio
%attr(755,root,root) %{_bindir}/fio-dedupe
%attr(755,root,root) %{_bindir}/fio-genzipf
%attr(755,root,root) %{_bindir}/fio-verify-state
%attr(755,root,root) %{_bindir}/fio2gnuplot
%attr(755,root,root) %{_bindir}/fio_generate_plots
%attr(755,root,root) %{_bindir}/fio_latency2csv.py
%attr(755,root,root) %{_bindir}/fiologparser.py
%attr(755,root,root) %{_bindir}/fiologparser_hist.py
%attr(755,root,root) %{_bindir}/genfio
%{_datadir}/fio
%{_mandir}/man1/fio.1*
%{_mandir}/man1/fio2gnuplot.1*
%{_mandir}/man1/fio_generate_plots.1*
%{_mandir}/man1/fiologparser_hist.py.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/fio

%if %{with gtk}
%files -n gfio
%defattr(644,root,root,755)
%doc GFIO-TODO
%attr(755,root,root) %{_bindir}/gfio
%endif
