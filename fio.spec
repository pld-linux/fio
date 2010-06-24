Summary:	I/O tool for benchmark and stress/hardware verification
Summary(pl.UTF-8):	Narzędzie do mierzenia wydajności I/O i sprawdzania sprawności sprzętu
Name:		fio
Version:	1.41.4
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://brick.kernel.dk/snaps/%{name}-%{version}.tar.bz2
# Source0-md5:	2644e32d1c428e857a8b1c8690da1869
Patch0:		%{name}-makefile.patch
URL:		http://git.kernel.dk/?p=fio.git;a=summary
BuildRequires:	libaio-devel
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

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	%{?debug:DEBUGFLAGS=-D_FORTIFY_SOURCE=2}%{!?debug:DEBUGFLAGS=}

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
%doc HOWTO README
%doc examples
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/fio*.1*
