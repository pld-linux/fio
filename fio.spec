# TODO: HDFS (--enable-libhdfs, requires also java), guasi, fusion-aw (nvm-primitives)
#
# Conditional build:
%bcond_without	ceph		# RDB (CephFS) support
%bcond_without	glusterfs	# GFAPI support
%bcond_without	gtk		# GTK+ based GUI (gfio)
%bcond_without	numa		# NUMA support
#
Summary:	I/O tool for benchmark and stress/hardware verification
Summary(pl.UTF-8):	Narzędzie do mierzenia wydajności I/O i sprawdzania sprawności sprzętu
Name:		fio
Version:	2.2.7
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://brick.kernel.dk/snaps/%{name}-%{version}.tar.bz2
# Source0-md5:	0c30299c4e37cd3ae9657c2e4a363092
URL:		http://git.kernel.dk/?p=fio.git;a=summary
BuildRequires:	bison
%{?with_ceph:BuildRequires:	ceph-devel}
BuildRequires:	flex
%{?with_glusterfs:BuildRequires:	glusterfs-devel}
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

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' tools/genfio
%{__sed} -i -e '1s,/usr/bin/env python,/usr/bin/python,' tools/plot/fio2gnuplot

%build
./configure \
	--cc="%{__cc}" \
	--extra-cflags="%{rpmcflags} %{rpmcppflags}" \
	%{!?with_glusterfs:--enable-gfapi} \
	%{?with_gtk:--enable-gfio} \
	%{!?with_numa:--disable-numa} \
	%{!?with_ceph:--disable-rdb} \

%{__make} \
	LDFLAGS="%{rpmldflags}" \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix="%{_prefix}" \
	mandir="%{_mandir}" \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO MORAL-LICENSE README REPORTING-BUGS SERVER-TODO examples
%attr(755,root,root) %{_bindir}/fio
%attr(755,root,root) %{_bindir}/fio-btrace2fio
%attr(755,root,root) %{_bindir}/fio-dedupe
%attr(755,root,root) %{_bindir}/fio-genzipf
%attr(755,root,root) %{_bindir}/fio2gnuplot
%attr(755,root,root) %{_bindir}/fio_generate_plots
%attr(755,root,root) %{_bindir}/genfio
%{_datadir}/fio
%{_mandir}/man1/fio.1*
%{_mandir}/man1/fio2gnuplot.1*
%{_mandir}/man1/fio_generate_plots.1*

%if %{with gtk}
%files -n gfio
%defattr(644,root,root,755)
%doc GFIO-TODO
%attr(755,root,root) %{_bindir}/gfio
%endif
