%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname shaker
%global pypi_name pyshaker
%global with_doc 1

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{sname}
Version:        1.1.0
Release:        1%{?dist}
Summary:        Distributed data-plane performance testing tool

License:        ASL 2.0
URL:            https://launchpad.net/%{sname}/
Source0:        http://tarballs.openstack.org/%{sname}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
# for config generation
BuildRequires:  python-oslo-config
BuildRequires:  PyYAML
BuildRequires:  python-oslo-log
BuildRequires:  python-pykwalify
# test requirements
BuildRequires:  python-mock
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
BuildRequires:  python-heatclient
BuildRequires:  python-novaclient
BuildRequires:  python-neutronclient
BuildRequires:  python-glanceclient
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-pygal
BuildRequires:  python-zmq
BuildRequires:  python-psutil

%description
Shaker is the distributed dataplane testing tool built for OpenStack. Shaker wraps
around popular system network testing tools like iperf < iperf3 < and netperf
(with help of flent < Shaker is able to deploy OpenStack instances and networks
in different topologies. Shaker scenario specifies the deployment and list of
tests to execute.

%package -n     python2-%{sname}
Summary:        Distributed data-plane performance testing tool
%{?python_provide:%python_provide python2-%{sname}}

Requires:       diskimage-builder >= 1.1.2
Requires:       python-pbr
Requires:       python-iso8601
Requires:       python-jinja2
Requires:       python-keystoneauth1 >= 2.18.0
Requires:       python-os-client-config >= 1.22.0
Requires:       python-oslo-concurrency >= 3.8.0
Requires:       python-oslo-config >= 2:3.14.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 3.11.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.18.0
Requires:       python-pygal
Requires:       python-pykwalify
Requires:       python-glanceclient >= 1:2.5.0
Requires:       python-neutronclient  >= 5.1.0
Requires:       python-novaclient >= 1:7.1.0
Requires:       python-heatclient >= 1.6.1
Requires:       PyYAML
Requires:       python-zmq
Requires:       python-six
Requires:       python-subunit

%description -n python2-%{sname}
Shaker is the distributed dataplane testing tool built for OpenStack. Shaker wraps
around popular system network testing tools like iperf < iperf3 < and netperf
(with help of flent < Shaker is able to deploy OpenStack instances and networks
in different topologies. Shaker scenario specifies the deployment and list of
tests to execute.

%package -n python2-%{sname}-tests
Summary:    Distributed data-plane performance testing tool tests
Requires:   python2-%{sname} = %{version}-%{release}

Requires:  python-mock
Requires:  python-oslotest
Requires:  python-testrepository
Requires:  python-testtools

%description -n python2-%{sname}-tests
Shaker is the distributed dataplane testing tool built for OpenStack. Shaker wraps
around popular system network testing tools like iperf < iperf3 < and netperf
(with help of flent < Shaker is able to deploy OpenStack instances and networks
in different topologies. Shaker scenario specifies the deployment and list of
tests to execute.

It contains the unit tests for shaker.

%if 0%{?with_python3}
%package -n     python3-%{sname}
Summary:        Distributed data-plane performance testing tool
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

# test requirements
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools

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
Shaker is the distributed dataplane testing tool built for OpenStack. Shaker wraps
around popular system network testing tools like iperf < iperf3 < and netperf
(with help of flent < Shaker is able to deploy OpenStack instances and networks
in different topologies. Shaker scenario specifies the deployment and list of
tests to execute.

It contains the unit tests for shaker.
%endif

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:        Shaker documentation

BuildRequires:   python-sphinx
BuildRequires:   python-sphinxcontrib-httpdomain
BuildRequires:   python-sphinx_rtd_theme

%description -n python-%{sname}-doc
Documentation for shaker
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

rm -f test-requirements.txt requirements.txt rtd-requirements.txt

%if 0%{?with_doc}
%build
%py2_build

%{__python2} setup.py build_sphinx

# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

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

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python2-%{sname}-tests
%license LICENSE
%{python2_sitelib}/%{sname}/tests

%changelog
* Wed Aug 30 2017 Haikel Guemar <hguemar@fedoraproject.org> 1.1.0-1
- Update to 1.1.0

