%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{sname}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core
# for config generation
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-log
BuildRequires:  python3-pykwalify
# test requirements
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools
BuildRequires:  python3-heatclient
BuildRequires:  python3-novaclient
BuildRequires:  python3-neutronclient
BuildRequires:  python3-glanceclient
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-psutil
BuildRequires:  python3-timeout-decorator

BuildRequires:  python3-pygal
BuildRequires:  python3-PyYAML
BuildRequires:  python3-zmq

%description
%{common_desc}

%package -n     python3-%{sname}
Summary:        Distributed data-plane performance testing tool
%{?python_provide:%python_provide python3-%{sname}}

Requires:       diskimage-builder >= 1.1.2
Requires:       python3-pbr
Requires:       python3-iso8601
Requires:       python3-jinja2
Requires:       python3-keystoneauth1 >= 2.18.0
Requires:       python3-os-client-config >= 1.22.0
Requires:       python3-oslo-concurrency >= 3.8.0
Requires:       python3-oslo-config >= 2:3.14.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-log >= 3.11.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.18.0
Requires:       python3-pykwalify
Requires:       python3-glanceclient >= 1:2.5.0
Requires:       python3-neutronclient  >= 5.1.0
Requires:       python3-novaclient >= 1:7.1.0
Requires:       python3-heatclient >= 1.6.1
Requires:       python3-six
Requires:       python3-subunit
Requires:       python3-timeout-decorator >= 0.4.0


Requires:       python3-pygal
Requires:       python3-PyYAML
Requires:       python3-zmq


%description -n python3-%{sname}
%{common_desc}

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

%package -n python-%{sname}-doc
Summary:        Shaker documentation

BuildRequires:   python3-sphinx
BuildRequires:   python3-sphinxcontrib-httpdomain
BuildRequires:   python3-sphinx_rtd_theme

%description -n python-%{sname}-doc
Documentation for shaker

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

rm -f test-requirements.txt requirements.txt rtd-requirements.txt

%build
%{py3_build}

%{__python3} setup.py build_sphinx

# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

PYTHONPATH=. oslo-config-generator --config-file=config-generator.conf

%install
SHAKER_EXEC="shaker shaker-agent shaker-spot shaker-report shaker-image-builder \
shaker-cleanup shaker-all-in-one"

%{py3_install}
for binary in $SHAKER_EXEC; do
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/$binary-%{python3_version}
  ln -s $binary-%{python3_version} %{buildroot}/%{_bindir}/$binary-3
  ln -s $binary-3 %{buildroot}/%{_bindir}/$binary
done

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/pyshaker
install -p -D -m 640 etc/shaker.conf %{buildroot}%{_sysconfdir}/pyshaker/shaker.conf

%check
%{__python3} setup.py test

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{_bindir}/shaker
%{_bindir}/shaker-3
%{_bindir}/shaker-%{python3_version}
%{_bindir}/shaker-agent
%{_bindir}/shaker-agent-3
%{_bindir}/shaker-agent-%{python3_version}
%{_bindir}/shaker-spot
%{_bindir}/shaker-spot-3
%{_bindir}/shaker-spot-%{python3_version}
%{_bindir}/shaker-report
%{_bindir}/shaker-report-3
%{_bindir}/shaker-report-%{python3_version}
%{_bindir}/shaker-image-builder
%{_bindir}/shaker-image-builder-3
%{_bindir}/shaker-image-builder-%{python3_version}
%{_bindir}/shaker-cleanup
%{_bindir}/shaker-cleanup-3
%{_bindir}/shaker-cleanup-%{python3_version}
%{_bindir}/shaker-all-in-one
%{_bindir}/shaker-all-in-one-3
%{_bindir}/shaker-all-in-one-%{python3_version}
%{python3_sitelib}/shaker
%{python3_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python3_sitelib}/%{sname}/tests
%config(noreplace) %{_sysconfdir}/%{pypi_name}/*.conf

%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html

%files -n python3-%{sname}-tests
%license LICENSE
%{python3_sitelib}/%{sname}/tests

%changelog

