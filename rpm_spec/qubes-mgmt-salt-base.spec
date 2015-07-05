%{!?version: %define version %(cat version)}
%{!?rel: %define rel %(cat rel)}
%{!?formula_name: %define formula_name %(cat formula_name)}

Name:      qubes-mgmt-salt-base
Version:   %{version}
Release:   %{rel}%{?dist}
Summary:   Custom base modules and states that are shared between dom0 and VM
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt-config
Requires:  qubes-mgmt-salt-base-salt
Requires:  qubes-mgmt-salt-base-overrides
Requires:  qubes-mgmt-salt-base-yamlscript-renderer
Requires:  qubes-mgmt-salt-base-yamlscript-users
Requires:  qubes-mgmt-salt-base-gpg

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
# TODO:
# - Add formula path to file_roots
# - Add formula to salt top.sls
# - Add formula to pillar top.sls if contains pillar data
salt-call --local saltutil.sync_all -l quiet --out quiet > /dev/null || true
salt-call --local state.sls salt.standalone-config -l quiet --out quiet > /dev/null || true

%files
%defattr(-,root,root)
%attr(750, root, root) %dir /srv/formulas/base/%{formula_name}
/srv/formulas/base/%{formula_name}/*

%changelog
