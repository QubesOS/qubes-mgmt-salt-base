%{!?version: %define version %(cat version)}

Name:      qubes-mgmt-salt-base
Version:   %{version}
Release:   1%{?dist}
summary:   Custom base modules and states that are shared between dom0 and VM.
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt-config
Requires:  qubes-mgmt-salt-base-overrides
Requires:  qubes-mgmt-salt-base-overrides-libs
Requires:  qubes-mgmt-salt-base-topd
Requires:  qubes-mgmt-salt-base-config

%define _builddir %(pwd)

%description
Custom base modules and states that are shared between dom0 and VM.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build

%install
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} SYSCONFDIR=%{_sysconfdir}

%post
# Update Salt Configuration
qubesctl state.sls config -l quiet --out quiet > /dev/null || true
qubesctl saltutil.clear_cache -l quiet --out quiet > /dev/null || true
qubesctl saltutil.sync_all refresh=true -l quiet --out quiet > /dev/null || true

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%attr(750, root, root) %dir /srv/salt/_grains
/srv/salt/_grains/redefined_dom0_grains.py*
/srv/salt/_grains/whonix.py*

%attr(750, root, root) %dir /srv/salt/_modules
/srv/salt/_modules/debug.py*
/srv/salt/_modules/module_utils.py*
/srv/salt/_modules/qubes.py*

%attr(750, root, root) %dir /srv/salt/_states
/srv/salt/_states/debug.py*
/srv/salt/_states/status.py*

%attr(750, root, root) %dir /srv/salt/_utils
/srv/salt/_utils/__init__.py*
/srv/salt/_utils/nulltype.py*
/srv/salt/_utils/qubes_utils.py*

%changelog
