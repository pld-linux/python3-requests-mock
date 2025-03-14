#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module		requests_mock
%define		egg_name	%{module}
%define		pypi_name	requests-mock
Summary:	Mock out responses from the requests package
Summary(pl.UTF-8):	Podstawianie atrap odpowiedzi z pakietu requests
Name:		python3-%{pypi_name}
Version:	1.12.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/requests-mock/
Source0:	https://files.pythonhosted.org/packages/source/r/requests-mock/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	84a910e415291bf1d986aa50c0c3eedb
Patch1:		no-git.patch
URL:		https://requests-mock.readthedocs.io/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-pbr
BuildRequires:	python3-build
BuildRequires:	python3-installer
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
%if %{with doc}
BuildRequires:	python3-reno
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
requests-mock provides a building block to stub out the HTTP requests
portions of your testing code.

%description -l pl.UTF-8
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
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
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

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
