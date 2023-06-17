Name:       dracut-sshd
Version:    0.6.5
Release:    2%{?dist}
Summary:    Provide SSH access to initramfs early user space
URL:        https://github.com/gsauthof/%{name}
License:    GPLv3+
Source:     https://github.com/gsauthof/%{name}/archive/refs/tags/%{version}.tar.gz
BuildArch:  noarch
BuildRequires: git
Requires:   dracut-network
Patch1:     backports.patch

%description
This Dracut module integrates the OpenSSH sshd into your
initramfs. It allows for remote unlocking of a fully encrypted
root filesystem and remote access to the Dracut emergency shell
(i.e. early userspace).

%package networkmanager
Summary:    Enables NetworkManager for sshd during initramfs
Requires:   %{name}
Requires:   NetworkManager

%description networkmanager
This module enables dracut network-manager settings for %{name}.

- If no configuration is provided it uses DHCP to bring up ethernet
  in the same manner as rootfs NetworkManager.
- Cleanly tears down networking prior to switchroot to avoid conflicts
  thereby allowing the OS full control of networking config.
- Network settings could be overriden by copying ifcfg or nmconnection
  settings into the initrd. e.g. static IP's

%prep
%autosetup -T -b 0 -p1 -Sgit

%build
# nothing to do here

%install
mkdir -p %{buildroot}/usr/lib/dracut/modules.d
cp -r 46sshd %{buildroot}/usr/lib/dracut/modules.d/
cp -r 99sshd-shadow-fixup %{buildroot}/usr/lib/dracut/modules.d/
cp -r 99sshd-networkmanager %{buildroot}/usr/lib/dracut/modules.d/

%files
%dir /usr/lib/dracut/modules.d/46sshd/
/usr/lib/dracut/modules.d/46sshd/module-setup.sh
/usr/lib/dracut/modules.d/46sshd/sshd.service
/usr/lib/dracut/modules.d/46sshd/motd
/usr/lib/dracut/modules.d/46sshd/profile
/usr/lib/dracut/modules.d/99sshd-shadow-fixup/module-setup.sh
%config(noreplace) /usr/lib/dracut/modules.d/46sshd/sshd_config
%doc README.md
%doc example/20-wired.network
%doc example/90-networkd.conf

%files networkmanager
%dir /usr/lib/dracut/modules.d/99sshd-networkmanager/
/usr/lib/dracut/modules.d/99sshd-networkmanager/module-setup.sh

%changelog
* Thu Jun 15 2023 Warren Togami <wtogami@gmail.com> - 0.6.5-2
- silence 99sshd-shadow-fixup because missing /etc/shadow is valid
- rpm owns module directories to ensure clean uninstall
- dracut-sshd-networkmanager subpackage
  99sshd-networkmanager adjusts nm-initrd.service to run for dracut-sshd.
- If config is lacking, auto DHCP ethernet in the same manner as rootfs NetworkManager.
- Clean network teardown prior to switchroot avoids conflicts and gives OS full control.
- Settings could be overriden by copying ifcfg or nmconnection settings into the initrd.
- 99sshd-shadow-fixup enables ssh pubkey login with disabled password as intended

* Sat May 27 2023 Georg Sauthoff <mail@gms.tf> - 0.6.5-1
- eliminate tmpfiles and fix Debian/Ubuntu support

* Sun May 7 2023 Georg Sauthoff <mail@gms.tf> - 0.6.4-1
- fix motd

* Sat May 1 2021 Georg Sauthoff <mail@gms.tf> - 0.6.3-1
- fix privilege separation directory for Fedora 34

* Sun Nov 22 2020 Akos Balla <akos.balla@sirc.hu> - 0.6.2-2
- support Fedora Silverblue
- add motd/profile files

* Sat Oct 31 2020 Georg Sauthoff <mail@gms.tf> - 0.6.2-1
- check whether key is included

* Thu May 28 2020 Georg Sauthoff <mail@gms.tf> - 0.6.1-2
- add example dracut config

* Thu May 28 2020 Georg Sauthoff <mail@gms.tf> - 0.6.1-1
- eliminate dracut module dependencies
- don't auto-include networkd configurations, anymore
- auto-include sshd executable dependencies

* Sat Jan 26 2019 Georg Sauthoff <mail@gms.tf> - 0.4-1
- initial packaging
