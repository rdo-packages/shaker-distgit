# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%global __python %{__python3}
%else
%global pyver 2
%global __python %{__python2}
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname shaker
%global pypi_name pyshaker

%global common_desc \
Shaker is the distributed dataplane testing tool built for OpenStack. Shaker wraps \
around popular system network testing tools like iperf < iperf3 < and netperf \
(with help of flent < Shaker is able to deploy OpenStack instances and networks \
in different topologies. Shaker scenario specifies the deployment and list of \
tests to execute.

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        Distributed data-plane performance testing tool

License:        ASL 2.0
URL:            https://launchpad.net/%{sname}/
Source0:        http://tarballs.openstack.org/%{sname}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
# for config generation
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-pykwalify
# test requirements
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-heatclient
BuildRequires:  python%{pyver}-novaclient
BuildRequires:  python%{pyver}-neutronclient
BuildRequires:  python%{pyver}-glanceclient
BuildRequires:  python%{pyver}-oslo-concurrency
BuildRequires:  python%{pyver}-psutil

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-pygal
BuildRequires:  PyYAML
BuildRequires:  python-zmq
%else
BuildRequires:  python%{pyver}-pygal
BuildRequires:  python%{pyver}-PyYAML
BuildRequires:  python%{pyver}-zmq
%endif

%description
%{common_desc}

%package -n     python%{pyver}-%{sname}
Summary:        Distributed data-plane performance testing tool
%{?python_provide:%python_provide python%{pyver}-%{sname}}

Requires:       diskimage-builder >= 1.1.2
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-iso8601
Requires:       python%{pyver}-jinja2
Requires:       python%{pyver}-keystoneauth1 >= 2.18.0
Requires:       python%{pyver}-os-client-config >= 1.22.0
Requires:       python%{pyver}-oslo-concurrency >= 3.8.0
Requires:       python%{pyver}-oslo-config >= 2:3.14.0
Requires:       python%{pyver}-oslo-i18n >= 2.1.0
Requires:       python%{pyver}-oslo-log >= 3.11.0
Requires:       python%{pyver}-oslo-serialization >= 1.10.0
Requires:       python%{pyver}-oslo-utils >= 3.18.0
Requires:       python%{pyver}-pykwalify
Requires:       python%{pyver}-glanceclient >= 1:2.5.0
Requires:       python%{pyver}-neutronclient  >= 5.1.0
Requires:       python%{pyver}-novaclient >= 1:7.1.0
Requires:       python%{pyver}-heatclient >= 1.6.1
Requires:       python%{pyver}-six
Requires:       python%{pyver}-subunit

# Handle python2 exception
%if %{pyver} == 2
Requires:       python-pygal
Requires:       PyYAML
Requires:       python-zmq
%else
Requires:       python%{pyver}-pygal
Requires:       python%{pyver}-PyYAML
Requires:       python%{pyver}-zmq
%endif


%description -n python%{pyver}-%{sname}
%{common_desc}

%package -n python%{pyver}-%{sname}-tests
Summary:    Distributed data-plane performance testing tool tests
Requires:   python%{pyver}-%{sname} = %{version}-%{release}

Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-testrepository
Requires:  python%{pyver}-testtools

%description -n python%{pyver}-%{sname}-tests
%{common_desc}

It contains the unit tests for shaker.

%package -n python-%{sname}-doc
Summary:        Shaker documentation

BuildRequires:   python%{pyver}-sphinx
BuildRequires:   python%{pyver}-sphinxcontrib-httpdomain
BuildRequires:   python%{pyver}-sphinx_rtd_theme

%description -n python-%{sname}-doc
Documentation for shaker

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

rm -f test-requirements.txt requirements.txt rtd-requirements.txt

%build
%{pyver_build}

%{pyver_bin} setup.py build_sphinx

# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=config-generator.conf

%install
SHAKER_EXEC="shaker shaker-agent shaker-spot shaker-report shaker-image-builder \
shaker-cleanup shaker-all-in-one"

%{pyver_install}
for binary in $SHAKER_EXEC; do
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/$binary-%{python_version}
  ln -s $binary-%{python_version} %{buildroot}/%{_bindir}/$binary-%{pyver}
  ln -s $binary-%{pyver} %{buildroot}/%{_bindir}/$binary
done

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/pyshaker
install -p -D -m 640 etc/shaker.conf %{buildroot}%{_sysconfdir}/pyshaker/shaker.conf

%check
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc README.rst
%{_bindir}/shaker
%{_bindir}/shaker-%{pyver}
%{_bindir}/shaker-%{python_version}
%{_bindir}/shaker-agent
%{_bindir}/shaker-agent-%{pyver}
%{_bindir}/shaker-agent-%{python_version}
%{_bindir}/shaker-spot
%{_bindir}/shaker-spot-%{pyver}
%{_bindir}/shaker-spot-%{python_version}
%{_bindir}/shaker-report
%{_bindir}/shaker-report-%{pyver}
%{_bindir}/shaker-report-%{python_version}
%{_bindir}/shaker-image-builder
%{_bindir}/shaker-image-builder-%{pyver}
%{_bindir}/shaker-image-builder-%{python_version}
%{_bindir}/shaker-cleanup
%{_bindir}/shaker-cleanup-%{pyver}
%{_bindir}/shaker-cleanup-%{python_version}
%{_bindir}/shaker-all-in-one
%{_bindir}/shaker-all-in-one-%{pyver}
%{_bindir}/shaker-all-in-one-%{python_version}
%{pyver_sitelib}/shaker
%{pyver_sitelib}/%{pypi_name}-*.egg-info
%exclude %{pyver_sitelib}/%{sname}/tests
%config(noreplace) %{_sysconfdir}/%{pypi_name}/*.conf

%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html

%files -n python%{pyver}-%{sname}-tests
%license LICENSE
%{pyver_sitelib}/%{sname}/tests

%changelog

# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/shaker/commit/?id=abe9fbd877bc0114896b17e8c36b3fa6d71c7d02
