%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?py2_build: %global py2_build %{__python2} setup.py build}
%{!?py2_install: %global py2_install %{__python2} setup.py install --skip-build --root %{buildroot}}
%bcond_with python3
%if 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_version: %global python2_version %(%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])")}
%endif
%else
%bcond_without python3
%endif

%bcond_without tests

%global srcname dockerfile-parse
%global modname %(n=%{srcname}; echo ${n//-/_})

%global commit 256e7fc490a8accda0b6b6f84436b0dcd4d7b707
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python-%{srcname}
Version:        0.0.15
Release:        1%{?dist}

Summary:        Python library for Dockerfile manipulation
License:        BSD
URL:            https://github.com/containerbuildsystem/dockerfile-parse
Source0:        %{url}/archive/%{commit}/%{srcname}-%{commit}.tar.gz

BuildArch:      noarch

%description
%{summary}.


%if %{with python3}
%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-six
BuildRequires:  python3-pytest
%endif
Requires: python3-six

%description -n python3-%{srcname}
%{summary}.

Python 3 version.

%else
%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with tests}
BuildRequires:  python-six
BuildRequires:  pytest
%endif
Requires: python-six

%description -n python2-%{srcname}
%{summary}.

Python 2 version.
%endif

%prep
%setup -n %{srcname}-%{commit}

%build
%if %{with python3}
%py3_build
%else
%py2_build
%endif

%install
%if %{with python3}
%py3_install
%else
%py2_install
%endif

%if %{with tests}
%check
export LANG=C.utf8
%if %{with python3}
py.test-%{python3_version} -v tests
%else
py.test-%{python2_version} -v tests
%endif
%endif


%if %{with python3}
%files -n python3-%{srcname}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{modname}-*.egg-info/
%{python3_sitelib}/%{modname}/
%else
%files -n python-%{srcname}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{modname}-*.egg-info/
%{python2_sitelib}/%{modname}/
%endif

%changelog
* Mon Jul 15 2019 Robert Cerven <rcerven@redhat.com> - 0.0.15-1
- new upstream release: 0.0.15

* Fri Apr 26 2019 Robert Cerven <rcerven@redhat.com> - 0.0.14-1
- new upstream release: 0.0.14

* Wed Nov 14 2018 Robert Cerven <rcerven@redhat.com> - 0.0.13-1
- new upstream release: 0.0.13

* Fri Oct 05 2018 Robert Cerven <rcerven@redhat.com> - 0.0.12-1
- new upstream release: 0.0.12

* Wed Jun 13 2018 Robert Cerven <rcerven@redhat.com> - 0.0.11-1
- new upstream release: 0.0.11

* Fri Mar 23 2018 Robert Cerven <rcerven@redhat.com> - 0.0.10-1
- new upstream release: 0.0.10

* Mon Feb 12 2018 Robert Cerven <rcerven@redhat.com> - 0.0.9-1
- new upstream release: 0.0.9

* Tue Jan 16 2018 Robert Cerven <rcerven@redhat.com> - 0.0.8-1
- new upstream release: 0.0.8

* Mon May 22 2017 Tim Waugh <twaugh@redhat.com> - 0.0.7-1
- 0.0.7

* Fri Feb  3 2017 Tim Waugh <twaugh@redhat.com>
- Incorporate modernisations from Fedora spec file.

* Tue Dec 20 2016 Tim Waugh <twaugh@redhat.com> - 0.0.6-1
- 0.0.6

* Fri Nov 20 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.5-3
- don't use py3dir
- new python macros
- use python_provide macro

* Fri Nov 06 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.5-2
- %%check section

* Mon Sep 21 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.5-1
- 0.0.5

* Thu Aug 27 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.4-1
- 0.0.4

* Tue Jun 30 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.3-2
- define macros for RHEL-6

* Fri Jun 26 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.3-1
- 0.0.3

* Fri Jun 26 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.2-1
- 0.0.2

* Thu Jun 18 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.1-1
- initial release
