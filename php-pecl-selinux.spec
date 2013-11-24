%define		php_name	php%{?php_suffix}
%define		modname		selinux
%define		status		devel
Summary:	SELinux binding for PHP script language
Summary(pl.UTF-8):	Dowiązania PHP do SELinuksa
Name:		%{php_name}-pecl-%{modname}
Version:	0.3.1
Release:	6
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	54857a8908e199113d128b8a652f5121
URL:		http://pecl.php.net/package/selinux/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	libselinux-devel >= 2.0.80
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides a set of interfaces to communicate between
SELinux and PHP script language. It contains functions to get/set
security context of processes and other objects, to get/set system
booleans, to make a query for in-kernel security server and so on.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to udostępnia zestaw interfejsów do komunikacji pomiędzy
PHP a SELinuksem. Zawiera między innymi funkcje do pobierania /
ustawiania kontekstów bezpieczeństwa procesów czy innych obiektów,
wartości logicznych, odpytywania wbudowanego w kernel wserwera
bezpieczeństwa itp.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -q -c
mv %{modname}-%{version}/* .

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
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
