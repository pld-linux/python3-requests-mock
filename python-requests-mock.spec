#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		requests_mock
%define		egg_name	%{module}
%define		pypi_name	requests-mock
Summary:	Mock out responses from the requests package
Summary(pl.UTF-8):	Podstawianie atrap odpowiedzi z pakietu requests
Name:		python-%{pypi_name}
Version:	1.11.0
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/requests-mock/
Source0:	https://files.pythonhosted.org/packages/source/r/requests-mock/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	04be84aa5fdc94fde14e57da1965c85d
Patch1:		%{name}-no-git.patch
URL:		https://requests-mock.readthedocs.io/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pbr
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-fixtures
BuildRequires:	python-mock
BuildRequires:	python-purl
BuildRequires:	python-pytest
BuildRequires:	python-requests >= 2.3
BuildRequires:	python-requests-futures
BuildRequires:	python-six
BuildRequires:	python-subunit
BuildRequires:	python-testrepository >= 0.0.18
BuildRequires:	python-testtools
BuildRequires:	subunit-python2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-pbr
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-fixtures
BuildRequires:	python3-purl
BuildRequires:	python3-pytest
BuildRequires:	python3-requests >= 2.3
BuildRequires:	python3-requests-futures
BuildRequires:	python3-six
BuildRequires:	python3-subunit
BuildRequires:	python3-testrepository >= 0.0.18
BuildRequires:	python3-testtools
BuildRequires:	subunit-python3
%endif
%endif
%if %{with doc}
BuildRequires:	python3-reno
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
requests-mock provides a building block to stub out the HTTP requests
portions of your testing code.

%description -l pl.UTF-8
Pakiet requests-mock udostępnia blok do tworzenia zaślepek żądań HTTP
w kodzie testowym.

%package -n python3-%{pypi_name}
Summary:	Mock out responses from the requests package
Summary(pl.UTF-8):	Podstawianie atrap odpowiedzi z pakietu requests
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{pypi_name}
requests-mock provides a building block to stub out the HTTP requests
portions of your testing code.

%description -n python3-%{pypi_name} -l pl.UTF-8
Pakiet requests-mock udostępnia blok do tworzenia zaślepek żądań HTTP
w kodzie testowym.

%package apidocs
Summary:	API documentation for requests_mock module
Summary(pl.UTF-8):	Dokumentacja API modułu requests_mock
Group:		Documentation

%description apidocs
API documentation for requests_mock module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu requests_mock.

%prep
%setup -q -n %{pypi_name}-%{version}
%patch -P 1 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=requests_mock.contrib._pytest_plugin \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests/pytest

%{__python} -m subunit.run discover | subunit2pyunit-2
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=requests_mock.contrib._pytest_plugin \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests/pytest

%{__python3} -m subunit.run discover | subunit2pyunit-3
%endif
%endif

%if %{with doc}
#%{__make} -C doc html \
#	SPHINXBUILD=sphinx-build-3
# broken Makefile (specifies . instead of "source" as source dir), so invoke directly:
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html doc/source doc/_build/html
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
%doc AUTHORS ChangeLog README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
