Summary:	A DomainKeys Identified Mail (DKIM) milter to sign and/or verify mail
Name:		opendkim
Version:	2.9.2
Release:	0.1
License:	BSD and Sendmail
Group:		Daemons
Source0:	http://downloads.sourceforge.net/opendkim/%{name}-%{version}.tar.gz
# Source0-md5:	08cc80a2aedec62b0444d8d6af24a155
URL:		http://opendkim.org/
BuildRequires:	db-devel
BuildRequires:	libmemcached-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	sendmail-devel
BuildRequires:	unbound-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenDKIM allows signing and/or verification of email through an open
source library that implements the DKIM service, plus a milter-based
filter application that can plug in to any milter-aware MTA, including
sendmail, Postfix, or any other MTA that supports the milter protocol.

%package libs
Summary:	An open source DKIM library
Group:		Libraries

%description libs
This package contains the library files required for running services
built using libopendkim.

%package libs-devel
Summary:	Development files for libopendkim
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description libs-devel
This package contains the static libraries, headers, and other support
files required for developing applications against libopendkim.

%prep
%setup -q

%build
%configure \
	--with-unbound \
	--with-libmemcached \
	--with-db \

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -d $RPM_BUILD_ROOT%{_initrddir}
install -d $RPM_BUILD_ROOT%{systemdunitdir}
install -p contrib/init/redhat/%{name} $RPM_BUILD_ROOT%{_initrddir}/%{name}
cp -p contrib/systemd/%{name}.service $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
cp -p contrib/init/redhat/%{name}-default-keygen $RPM_BUILD_ROOT%{_sbindir}/%{name}-default-keygen

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc FEATURES KNOWNBUGS LICENSE LICENSE.Sendmail RELEASE_NOTES RELEASE_NOTES.Sendmail INSTALL
%doc contrib/convert/convert_keylist.sh %{name}/*.sample
%doc %{name}/%{name}.conf.simple-verify %{name}/%{name}.conf.simple
%doc %{name}/README contrib/lua/*.lua
%doc contrib/stats/README.%{name}-reportstats
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%config(noreplace) %attr(640,%{name},%{name}) %{_sysconfdir}/%{name}/SigningTable
%config(noreplace) %attr(640,%{name},%{name}) %{_sysconfdir}/%{name}/KeyTable
%config(noreplace) %attr(640,%{name},%{name}) %{_sysconfdir}/%{name}/TrustedHosts
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/*/*
%dir %attr(-,%{name},%{name}) %{_localstatedir}/spool/%{name}
%dir %attr(-,%{name},%{name}) %{_localstatedir}/run/%{name}
%dir %attr(-,root,%{name}) %{_sysconfdir}/%{name}
%dir %attr(750,%{name},%{name}) %{_sysconfdir}/%{name}/keys
%{systemdunitdir}/%{name}.service
%attr(755,root,root) %{_sbindir}/%{name}-default-keygen

%files libs
%defattr(644,root,root,755)
%doc LICENSE LICENSE.Sendmail README
%{_libdir}/libopendkim.so.*

%files libs-devel
%defattr(644,root,root,755)
%doc LICENSE LICENSE.Sendmail
%doc libopendkim/docs/*.html
%{_includedir}/%{name}
%{_libdir}/*.so
%{_pkgconfigdir}/*.pc
