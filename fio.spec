Summary:	I/O tool for benchmark and stress/hardware verification
#Summary(pl):	-
Name:		fio
Version:	1.12
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://brick.kernel.dk/snaps/%{name}-%{version}.tar.bz2
# Source0-md5:	d4acc850d9b7197e31c08a204368c1ab
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

#%%description -l pl

%prep
%setup -q

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
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO README
%attr(755,root,root) %{_bindir}/*
