#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		requests_mock
%define		egg_name	%{module}
%define		pypi_name	requests-mock
Summary:	Mock out responses from the requests package
Name:		python-%{pypi_name}
Version:	1.3.0
Release:	2
License:	Apache
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/r/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	d2efbaf16d19153b7d271628071b4d4b
URL:		https://requests-mock.readthedocs.io
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-pbr
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-pbr
BuildRequires:	python3-setuptools
%endif
Requires:	python-requests
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
requests-mock provides a building block to stub out the HTTP requests
portions of your testing code.

%package -n python3-%{pypi_name}
Summary:	Mock out responses from the requests package
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}
requests-mock provides a building block to stub out the HTTP requests
portions of your testing code.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst *.txt
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst *.txt
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
