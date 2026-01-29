Summary: Config files for KDE
Name:    horizon-kde-settings
Version: 42.1
Release: 1%{?dist}

License: MIT
URL:     https://github.com/horizonlinux/horizon-kde-settings
Source0: https://github.com/horizonlinux/horizon-kde-settings/archive/refs/tags/42.1.tar.gz
Source1: COPYING

BuildArch: noarch
Provides:  kde-settings = %{version}-%{release}

Requires: horizon-themes

BuildRequires: kde-filesystem
# ssh-agent.service
BuildRequires: systemd-rpm-macros
Source10: ssh-agent.sh

# when kdebugrc was moved here
Conflicts: kf5-kdelibs4support < 5.7.0-3

Obsoletes: kde-settings-ksplash < 24-2
Obsoletes: kde-settings-minimal < 24-3

Requires: kde-filesystem
# RHEL 10 has the fixex in 0.18-7
Requires: xdg-user-dirs >= 0.18-7
## add breeze deps here? probably, need more too -- rex
Requires: breeze-icon-theme
# Baseline mimeapps associations, e.g. LibreOffice
Requires: shared-mime-info

%description
%{summary}.

%package plasma
Summary: Configuration files for plasma
Requires: %{name} = %{version}-%{release}
Provides: kde-settings-plasma = %{version}-%{release}
Requires: system-logos
Requires: google-noto-sans-fonts
# Not required but expected by users as we use other fonts from the noto "family"
Recommends: google-noto-serif-fonts
%if 0%{?rhel} && 0%{?rhel} < 9
Requires: google-noto-mono-fonts
%else
Requires: google-noto-sans-mono-fonts
%endif
%description plasma
%{summary}.


%package sddm
Summary: Configuration files for sddm
Requires: sddm
Requires: breeze-cursor-theme
Provides: kde-settings-sddm = %{version}-%{release}
%description sddm
%{summary}.

%package -n qt-settings
Summary: Configuration files for Qt
# qt-graphicssystem.* scripts use lspci
#Requires: pciutils
%description -n qt-settings
%{summary}.

%prep
%autosetup -p1

# omit crud
rm -fv Makefile


%build
# Intentionally left blank.  Nothing to see here.


%install
tar cpf - . | tar --directory %{buildroot} -xvpf -

if [ %{_prefix} != /usr ] ; then
   pushd %{buildroot}
   mv %{buildroot}/usr %{buildroot}%{_prefix}
   mv %{buildroot}/etc %{buildroot}%{_sysconfdir}
   popd
fi

cp -p %{SOURCE1} .

# default wallpaper symlink
%if 0%{?version_maj:1}
mkdir -p %{buildroot}%{_datadir}/wallpapers
ln -s F%{version_maj} %{buildroot}%{_datadir}/wallpapers/Fedora
%endif

%if 0%{?rhel} && 0%{?rhel} < 9
# for rhel 8 and older with older noto fonts
sed -e "s/Noto Sans Mono/Noto Mono/g" \
    -i %{buildroot}%{_datadir}/kde-settings/kde-profile/default/{share/config/kdeglobals,xdg/kdeglobals}
%endif

# for ssh-agent.serivce, set SSH_AUTH_SOCK
install -p -m644 -D %{SOURCE10} %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/ssh-agent.sh

## unpackaged files

%files
%license COPYING
%config(noreplace) %{_sysconfdir}/profile.d/kde*
%{_sysconfdir}/fonts/conf.d/10-sub-pixel-rgb-for-kde.conf
%{_sysconfdir}/kde/env/env.sh
%{_sysconfdir}/kde/env/gpg-agent-startup.sh
%{_sysconfdir}/kde/shutdown/gpg-agent-shutdown.sh
%{_sysconfdir}/kde/env/gtk2_rc_files.sh
%if 0%{?fedora} || 0%{?rhel} > 7
%{_sysconfdir}/kde/env/fedora-bookmarks.sh
%{_datadir}/kde-settings/
# these can probably go now -- rex
%{_prefix}/lib/rpm/plasma4.prov
%{_prefix}/lib/rpm/plasma4.req
%{_prefix}/lib/rpm/fileattrs/plasma4.attr
%{_datadir}/polkit-1/rules.d/11-fedora-kde-policy.rules
%endif
%config(noreplace) %{_sysconfdir}/xdg/kcm-about-distrorc
%config(noreplace) %{_sysconfdir}/xdg/kdebugrc
%dir %{_sysconfdir}/pam.d
%config(noreplace) %{_sysconfdir}/pam.d/kcheckpass
%config(noreplace) %{_sysconfdir}/pam.d/kscreensaver
# drop noreplace, so we can be sure to get the new kiosk bits
%config %{_sysconfdir}/kderc
%config %{_sysconfdir}/kde4rc
%if 0%{?rhel} && 0%{?rhel} <= 7
%exclude %{_datadir}/kde-settings/kde-profile/default/share/apps/plasma-desktop/init/00-defaultLayout.js
%endif

%files plasma
%{_sysconfdir}/xdg/plasma-workspace/env/env.sh
%{_sysconfdir}/xdg/plasma-workspace/env/gtk2_rc_files.sh
%{_sysconfdir}/xdg/plasma-workspace/env/gtk3_scrolling.sh
%if 0%{?version_maj:1}
%{_datadir}/wallpapers/Fedora
%endif
%{_sysconfdir}/xdg/plasma-workspace/env/ssh-agent.sh


%files sddm
%{_prefix}/lib/sddm/sddm.conf.d/kde_settings.conf

%files -n qt-settings
%license COPYING
%config(noreplace) %{_sysconfdir}/Trolltech.conf

%changelog
* Thu Jan 29 2026 Marcel Mrówka
- Create package
