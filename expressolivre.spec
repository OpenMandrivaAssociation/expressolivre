# (oe) undefining these makes the build _real_ quick.
%undefine __find_provides
%undefine __find_requires

%define	name	expressolivre
%define	ShortName expresso
%define	version	2.0.9
%define	Version	2_0_9
%define	release	%mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Web-based groupware suite written in php
License:	GPL+
Group:		System/Servers
URL:		http://www.expressolivre.org/
Source0:	http://downloads.sourceforge.net/%{name}/%{ShortName}-%{version}.tar.bz2
#Source1:	http://www.expressolivre.org/html/expressolivre/downloads/releases/%{ShortName}-%{Version}.tar.gz

Requires:	apache-mod_php
Requires:	apache-mod_ldap
Requires:	apache-mod_deflate
Requires:	apache-mod_dav
Requires:	apache-mod_userdir
Requires:	apache-mod_proxy
Requires:	apache-mod_cache
Requires:	apache-mod_suexec
Requires:	apache-mod_disk_cache
Requires:	apache-mod_file_cache
Requires:	apache-mod_mem_cache
Requires:	postgresql8.4-server
Requires:	openldap
Requires:	php-xml
Requires:	php-gd
Requires:	php-cli
Requires:	php-dom
Requires:	php-ldap
Requires:	php-pgsql
Suggests:	php-pdo_mysql
Suggests:	php-mcrypt
Suggests:	php-imap
Suggests:	openldap-server
Provides:	expressolivre-contactcenter = %{version}-%{release}
Provides:	expressolivre-expressoMail1_2 = %{version}-%{release}
Provides:       expressolivre-calendar = %{version}-%{release}
Provides:       expressolivre-mobile = %{version}-%{release}
Provides:       expressolivre-expressoAdmin1_2 = %{version}-%{release}
Provides:       expressolivre-jabberit_messenger = %{version}-%{release}
Provides:	expressolivre-workflow = %{version}-%{release}
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
ExpressoLivre is a web-based groupware suite written in PHP based on Egroupware. 
The core package provides the admin, setup, phpgwapi, emailadmin and preferences
packages.

%package contactcenter
Summary:	The expressolivre bookmarks application
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}

%description contactcenter
Manage your bookmarks with expressolivre.

%package expressoMail1_2
Summary:	The expressolivre email application
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}

%description expressoMail1_2
The Expresso Email reader and manager.

%package calendar
Summary:	The expressolivre calendar application
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}

%description calendar
Web-Calendar with Alarms and E-Mail integration

%package mobile
Summary:	The expressolivre mobile -PDA or Phone- interface
Group:		System/Servers
Requires:	%{name} >= %{version}-%{release}

%description mobile
The expressolivre mobile -PDA or Phone- interface

%package expressoAdmin1_2
Summary:        The expressolivre manager
Group:          System/Servers
Requires:       %{name} >= %{version}-%{release}

%description expressoAdmin1_2
The expressolivre manager

%package jabberit_messenger
Summary:        The expressolivre messenger
Group:          System/Servers
Requires:       %{name} >= %{version}-%{release}

%description jabberit_messenger
The expressolivre messenger

%package workflow
Summary:        The expressolivre workflow
Group:          System/Servers
Requires:       %{name} >= %{version}-%{release}

%description workflow
The expressolivre workflow

#%package filemanager
#Summary:	The expressolivre filemanager application
#Group:		System/Servers
#Requires:	%{name} >= %{version}-%{release}

#%description filemanager
#This is the filemanager app for expressolivre.

%prep
%setup -q -n %{ShortName}

# cleanup
find . -type d -name CVS | xargs rm -rf
find . -type f -name *.old -o -name *.backup | xargs rm -f
find . -type f -empty | xargs rm -f
find . -type f | xargs chmod 644
find . -name .htaccess |xargs rm -f
find . -name .svn | xargs rm -rf

%build

%install
rm -rf %{buildroot}

%define doc_pkg doc-expressolivre/rhel5-centos5/arqs-conf-mdv/
# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
sed 's,\/usr\/share\/expressolivre,\/var\/www\/expressolivre,' %{doc_pkg}apache.conf > %{buildroot}%{_webappconfdir}/%{name}.conf

# install files
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/default/files
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/default/backup
install -d -m 755 %{buildroot}%{_var}/www/%{name}
cp -aRf * %{buildroot}%{_var}/www/%{name}

# setup the config file: this dummy content triggers the setup process 
# (from upstream's package)
#cp %{doc_pkg}header.inc.php %{buildroot}%{_localstatedir}/lib/%{name}/header.inc.php
#ln -s %{_localstatedir}/lib/%{name}/header.inc.php %{buildroot}%{_var}/www/%{name}/header.inc.php

# post-install cleanup
rm -rf %{buildroot}%{_var}/www/%{name}/doc-expressolivre
rm -rf %{buildroot}%{_var}/www/%{name}/*/doc-expressolivre

%post
 
%postun
/etc/init.d/postgresql start
/etc/init.d/httpd start

	    
%clean
rm -rf %{buildroot}

%files
%defattr(-,apache,apache)
%doc doc* 
%doc phpgwapi/doc/*
# Apache configuration file
%config(noreplace) %{_webappconfdir}/%{name}.conf
# Header config file
#%attr(640,apache,apache) %config(noreplace) %{_localstatedir}/lib/%{name}/header.inc.php
# top level dir and files
%dir %{_var}/www/%{name}
%{_var}/www/%{name}/*.php
%{_var}/www/%{name}/header.inc.php.template
%{_var}/www/%{name}/phpgwapi
%{_var}/www/%{name}/news_admin
%{_var}/www/%{name}/help
%{_var}/www/%{name}/emailadmin
%{_var}/www/%{name}/admin
%{_var}/www/%{name}/security
%{_var}/www/%{name}/preferences
%{_var}/www/%{name}/setup
%{_var}/www/%{name}/home.php
%{_var}/www/%{name}/robots.txt
%{_var}/www/%{name}/favicon.ico

%files contactcenter
%defattr(-,apache,apache)
%{_var}/www/%{name}/contactcenter

%files expressoMail1_2
%defattr(-,apache,apache)
%{_var}/www/%{name}/expressoMail1_2

%files calendar
%defattr(-,apache,apache)
%{_var}/www/%{name}/calendar

%files mobile
%defattr(-,apache,apache)
%{_var}/www/%{name}/mobile

%files expressoAdmin1_2
%defattr(-,apache,apache)
%{_var}/www/%{name}/expressoAdmin1_2

%files jabberit_messenger
%defattr(-,apache,apache)
%{_var}/www/%{name}/jabberit_messenger

%files workflow
%defattr(-,apache,apache)
%{_var}/www/%{name}/workflow
