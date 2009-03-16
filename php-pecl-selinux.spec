%define		_modname	selinux
%define		_status		devel
Summary:	SELinux binding for PHP script language
Summary(pl.UTF-8):	Dowiązania PHP do SELinuksa
Name:		php-pecl-%{_modname}
Version:	0.2.1
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	ed7c13a929ec37b885828d98e32bd755
URL:		http://pecl.php.net/package/selinux/
BuildRequires:	libselinux-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides a set of interfaces to communicate between
SELinux and PHP script language. It contains functions to get/set
security context of processes and other objects, to get/set system
booleans, to make a query for in-kernel security server and so on.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Rozszerzenie to udostępnia zestaw interfejsów do komunikacji pomiędzy
PHP a SELinuksem. Zawiera między innymi funkcje do pobierania /
ustawiania kontekstów bezpieczeństwa procesów czy innych obiektów,
wartości logicznych, odpytywania wbudowanego w kernel wserwera
bezpieczeństwa itp.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
mv %{_modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so