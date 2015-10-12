%{!?version: %define version %(make get-version)}
%{!?rel: %define rel %(make get-release)}
%{!?package_name: %define package_name %(make get-package_name)}
%{!?package_summary: %define package_summary %(make get-summary)}
%{!?package_description: %define package_description %(make get-description)}

%{!?formula_name: %define formula_name %(make get-formula_name)}
%{!?state_name: %define state_name %(make get-state_name)}
%{!?saltenv: %define saltenv %(make get-saltenv)}
%{!?pillar_dir: %define pillar_dir %(make get-pillar_dir)}
%{!?formula_dir: %define formula_dir %(make get-formula_dir)}

Name:      qubes-mgmt-salt-base
Version:   %{version}
Release:   %{rel}%{?dist}
Summary:   %{package_summary}
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt-config
Requires:  qubes-mgmt-salt-base-config
Requires:  qubes-mgmt-salt-base-overrides

%define _builddir %(pwd)

%description
%{package_description}

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
%attr(750, root, root) %dir /srv/salt/_grains
/srv/salt/_grains/redfined_dom0_grains.py*
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
