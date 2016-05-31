Name:       mlnx-sriov-ceilometer
Version:    2015.1.0
Release:    1%{?dist}
Summary:    Mellanox SR-IOV ceilometer counters inspector
License:    GPLv2
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  python-pbr

Requires:  openstack-ceilometer-compute

%description
Mellanox SR-IOV ceilometer counters inspector

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-lib %{python_sitelib}/ceilometer/compute/virt

%files
%doc README.rst
%{python_sitelib}/ceilometer/compute/virt

%clean
rm -rf $RPM_BUILD_ROOT

%post
ep_file_path=$(find /usr/ -name entry_points.txt | grep  "/ceilometer[^/]*egg-info")
ep_value="mlnx_libvirt = ceilometer.compute.virt.mlnx_libvirt.inspector:MlnxLibvirtInspector"
section=ceilometer.compute.virt
if grep -q "^\[$section\]" $ep_file_path ; then
	if ! grep --no-message -q "$ep_value" $ep_file_path ; then	
		sed -i "/\[$section\]/a $ep_value" $ep_file_path
	fi
else
	echo "ERROR: Can not find section: $section in file: $ep_file_path"
	exit 1
fi
