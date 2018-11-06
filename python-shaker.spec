%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname shaker
%global pypi_name pyshaker

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
Shaker is the distributed dataplane testing tool built for OpenStack. Shaker wraps \
around popular system network testing tools like iperf < iperf3 < and netperf \
(with help of flent < Shaker is able to deploy OpenStack instances and networks \
in different topologies. Shaker scenario specifies the deployment and list of \
tests to execute.

Name:           python-%{sname}
Version:        1.1.3
Release:        1%{?dist}
Summary:        Distributed data-plane performance testing tool

License:        ASL 2.0
URL:            https://launchpad.net/%{sname}/
Source0:        http://tarballs.openstack.org/%{sname}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  git
# for config generation
BuildRequires:  python2-oslo-config
BuildRequires:  PyYAML
BuildRequires:  python2-oslo-log
BuildRequires:  python2-pykwalify
# test requirements
BuildRequires:  python2-mock
BuildRequires:  python2-oslotest
BuildRequires:  python2-testrepository
BuildRequires:  python2-testtools
BuildRequires:  python2-heatclient
BuildRequires:  python2-novaclient
BuildRequires:  python2-neutronclient
BuildRequires:  python2-glanceclient
BuildRequires:  python2-oslo-concurrency
BuildRequires:  python-pygal
BuildRequires:  python-zmq
BuildRequires:  python2-psutil

%description
%{common_desc}

%package -n     python2-%{sname}
Summary:        Distributed data-plane performance testing tool
%{?python_provide:%python_provide python2-%{sname}}

Requires:       diskimage-builder >= 1.1.2
Requires:       python2-pbr
Requires:       python2-iso8601
Requires:       python2-jinja2
Requires:       python2-keystoneauth1 >= 2.18.0
Requires:       python2-os-client-config >= 1.22.0
Requires:       python2-oslo-concurrency >= 3.8.0
Requires:       python2-oslo-config >= 2:3.14.0
Requires:       python2-oslo-i18n >= 2.1.0
Requires:       python2-oslo-log >= 3.11.0
Requires:       python2-oslo-serialization >= 1.10.0
Requires:       python2-oslo-utils >= 3.18.0
Requires:       python-pygal
Requires:       python2-pykwalify
Requires:       python2-glanceclient >= 1:2.5.0
Requires:       python2-neutronclient  >= 5.1.0
Requires:       python2-novaclient >= 1:7.1.0
Requires:       python2-heatclient >= 1.6.1
Requires:       PyYAML
Requires:       python-zmq
Requires:       python2-six
Requires:       python2-subunit

%description -n python2-%{sname}
%{common_desc}

%package -n python2-%{sname}-tests
Summary:    Distributed data-plane performance testing tool tests
Requires:   python2-%{sname} = %{version}-%{release}

Requires:  python2-mock
Requires:  python2-oslotest
Requires:  python2-testrepository
Requires:  python2-testtools

%description -n python2-%{sname}-tests
%{common_desc}

It contains the unit tests for shaker.

%if 0%{?with_python3}
%package -n     python3-%{sname}
Summary:        Distributed data-plane performance testing tool
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

# test requirements
BuildRequires:  python3-glanceclient
BuildRequires:  python3-jinja2
BuildRequires:  python3-heatclient
BuildRequires:  python3-novaclient
BuildRequires:  python3-neutronclient
BuildRequires:  python3-mock
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslotest
BuildRequires:  python3-psutil
BuildRequires:  python3-pygal
BuildRequires:  python3-pykwalify
BuildRequires:  python3-PyYAML
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools
BuildRequires:  python3-zmq

Requires:       python3-pbr
Requires:       python3-iso8601
Requires:       python3-jinja2
Requires:       python3-keystoneauth1
Requires:       python3-os-client-config
Requires:       python3-oslo-concurrency
Requires:       python3-oslo-config
Requires:       python3-oslo-i18n
Requires:       python3-oslo-log
Requires:       python3-oslo-serialization
Requires:       python3-oslo-utils
Requires:       python3-psutil
Requires:       python3-pygal
Requires:       python3-pykwalify
Requires:       python3-glanceclient
Requires:       python3-neutronclient
Requires:       python3-novaclient
Requires:       python3-heatclient
Requires:       python3-PyYAML
Requires:       python3-zmq
Requires:       python3-six
Requires:       python3-subunit

%description -n python3-%{sname}
**The distributed dataplane testing tool built for OpenStack.**Shaker wraps
around popular system network testing tools like iperf < iperf3 < and netperf
(with help of flent < Shaker is able to deploy OpenStack instances and networks
in different topologies. Shaker scenario specifies the deployment and list of
tests to execute. Additionally tests may be tuned dynamically in ...

%package -n python3-%{sname}-tests
Summary:    Distributed data-plane performance testing tool tests
Requires:   python3-%{sname} = %{version}-%{release}

Requires:  python3-mock
Requires:  python3-oslotest
Requires:  python3-testrepository
Requires:  python3-testtools

%description -n python3-%{sname}-tests
%{common_desc}

It contains the unit tests for shaker.
%endif

%package -n python-%{sname}-doc
Summary:        Shaker documentation

BuildRequires:   python2-sphinx
BuildRequires:   python-sphinxcontrib-httpdomain
BuildRequires:   python-sphinx_rtd_theme

%description -n python-%{sname}-doc
Documentation for shaker

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

rm -f test-requirements.txt requirements.txt rtd-requirements.txt

%build
%py2_build

%{__python2} setup.py build_sphinx

# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

PYTHONPATH=. oslo-config-generator --config-file=config-generator.conf

%if 0%{?with_python3}
%py3_build
%endif

%install
SHAKER_EXEC="shaker shaker-agent shaker-spot shaker-report shaker-image-builder \
shaker-cleanup shaker-all-in-one"

%if 0%{?with_python3}
%py3_install
for binary in $SHAKER_EXEC; do
  cp %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/$binary-3
  ln -sf %{_bindir}/$binary-3 %{buildroot}/%{_bindir}/$binary-%{python3_version}
done
%endif

%py2_install
for binary in $SHAKER_EXEC; do
  cp %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/$binary-2
  ln -sf %{_bindir}/$binary-2 %{buildroot}/%{_bindir}/$binary-%{python2_version}
done

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/pyshaker
install -p -D -m 640 etc/shaker.conf %{buildroot}%{_sysconfdir}/pyshaker/shaker.conf

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{sname}
%license LICENSE
%doc README.rst
%{_bindir}/shaker
%{_bindir}/shaker-2
%{_bindir}/shaker-%{python2_version}
%{_bindir}/shaker-agent
%{_bindir}/shaker-agent-2
%{_bindir}/shaker-agent-%{python2_version}
%{_bindir}/shaker-spot
%{_bindir}/shaker-spot-2
%{_bindir}/shaker-spot-%{python2_version}
%{_bindir}/shaker-report
%{_bindir}/shaker-report-2
%{_bindir}/shaker-report-%{python2_version}
%{_bindir}/shaker-image-builder
%{_bindir}/shaker-image-builder-2
%{_bindir}/shaker-image-builder-%{python2_version}
%{_bindir}/shaker-cleanup
%{_bindir}/shaker-cleanup-2
%{_bindir}/shaker-cleanup-%{python2_version}
%{_bindir}/shaker-all-in-one
%{_bindir}/shaker-all-in-one-2
%{_bindir}/shaker-all-in-one-%{python2_version}
%{python2_sitelib}/shaker
%{python2_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python2_sitelib}/%{sname}/tests
%config(noreplace) %{_sysconfdir}/%{pypi_name}/*.conf


%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{_bindir}/shaker-3
%{_bindir}/shaker-%{python3_version}
%{_bindir}/shaker-agent-3
%{_bindir}/shaker-agent-%{python3_version}
%{_bindir}/shaker-spot-3
%{_bindir}/shaker-spot-%{python3_version}
%{_bindir}/shaker-report-3
%{_bindir}/shaker-report-%{python3_version}
%{_bindir}/shaker-image-builder-3
%{_bindir}/shaker-image-builder-%{python3_version}
%{_bindir}/shaker-cleanup-3
%{_bindir}/shaker-cleanup-%{python3_version}
%{_bindir}/shaker-all-in-one-3
%{_bindir}/shaker-all-in-one-%{python3_version}
%{python3_sitelib}/shaker
%{python3_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python3_sitelib}/%{sname}/tests
%config(noreplace) %{_sysconfdir}/%{pypi_name}/*.conf


%files -n python3-%{sname}-tests
%license LICENSE
%{python3_sitelib}/%{sname}/tests
%endif

%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html

%files -n python2-%{sname}-tests
%license LICENSE
%{python2_sitelib}/%{sname}/tests

%changelog
* Tue Aug 28 2018 RDO <dev@lists.rdoproject.org> 1.1.3-1
- Update to 1.1.3

* Wed Aug 30 2017 Haikel Guemar <hguemar@fedoraproject.org> 1.1.0-1
- Update to 1.1.0

# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/shaker/commit/?id=abe9fbd877bc0114896b17e8c36b3fa6d71c7d02
