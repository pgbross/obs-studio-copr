%undefine __cmake_in_source_build
%if 0%{?fedora} || 0%{?rhel} > 7
# bytecompile with Python 3
%global __python %{__python3}
%else
%global __python %{__python2}
%endif

%if 0%{?el7}
# Developper toolset version
%global dts_ver       8
%endif

%global commit1 a2cbc14324d2ba12ee9dc84babc85f73de9779c2
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

Name:           obs-studio
Version:        27.0.0
Release:        3%{?dist}
Summary:        Open Broadcaster Software Studio

License:        GPLv2+
URL:            https://obsproject.com/
Source0:        https://github.com/obsproject/obs-studio/archive/%{version}-rc1/%{name}-%{version}-rc1.tar.gz
Source1:        https://github.com/obsproject/obs-vst/archive/%{commit1}/obs-vst-%{shortcommit1}.tar.gz

BuildRequires:  gcc
BuildRequires:  cmake3
BuildRequires:  ninja-build
BuildRequires:  libappstream-glib
%if 0%{?el7}
BuildRequires: devtoolset-%{dts_ver}-toolchain, devtoolset-%{dts_ver}-libatomic-devel
%endif

BuildRequires:  alsa-lib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  jansson-devel
BuildRequires:  libcurl-devel
BuildRequires:  libGL-devel
BuildRequires:  libv4l-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXinerama-devel
BuildRequires:  luajit-devel
BuildRequires:  mbedtls-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  pipewire-devel
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python3-devel
%else
BuildRequires:  python2-devel
%endif
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtwayland-devel
BuildRequires:  qt5-qtx11extras-devel
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  speexdsp-devel
%else
BuildRequires:  speex-devel
%endif
BuildRequires:  swig
BuildRequires:  systemd-devel
BuildRequires:  wayland-devel
BuildRequires:  vlc-devel
BuildRequires:  x264-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       ffmpeg
Requires:       x264

%description
Open Broadcaster Software is free and open source
software for video recording and live streaming.

%package libs
Summary: Open Broadcaster Software Studio libraries

%description libs
Library files for Open Broadcaster Software

%package devel
Summary: Open Broadcaster Software Studio header files
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Header files for Open Broadcaster Software


%prep
%if 0%{?el7}
. /opt/rh/devtoolset-%{dts_ver}/enable
%endif
%autosetup -p0

# rpmlint reports E: hardcoded-library-path
# replace OBS_MULTIARCH_SUFFIX by LIB_SUFFIX
sed -i 's|OBS_MULTIARCH_SUFFIX|LIB_SUFFIX|g' cmake/Modules/ObsHelpers.cmake

# Prepare plugins/obs-vst
tar -xf %{SOURCE1} -C plugins/obs-vst --strip-components=1

%build
%if 0%{?el7}
. /opt/rh/devtoolset-%{dts_ver}/enable
%endif
%cmake3 -DOBS_VERSION_OVERRIDE=%{version} \
        -DUNIX_STRUCTURE=1 -GNinja \
        -DOpenGL_GL_PREFERENCE=GLVND
%cmake3_build


%install
%cmake3_install

# Add missing files to enable the build of obs-ndi
install -Dm644 UI/obs-frontend-api/obs-frontend-api.h %{buildroot}%{_includedir}/obs/
install -Dm644 cmake/external/ObsPluginHelpers.cmake %{buildroot}%{_libdir}/cmake/LibObs/

%check
%if 0%{?el7}
. /opt/rh/devtoolset-%{dts_ver}/enable
%endif
/usr/bin/desktop-file-validate %{buildroot}/%{_datadir}/applications/com.obsproject.Studio.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml

%ldconfig_scriptlets libs

%files
%doc README.rst
%license UI/data/license/gplv2.txt
%license COPYING
%{_bindir}/obs
%{_bindir}/obs-ffmpeg-mux
%{_datadir}/metainfo/com.obsproject.Studio.appdata.xml
%{_datadir}/applications/com.obsproject.Studio.desktop
%{_datadir}/icons/hicolor/256x256/apps/com.obsproject.Studio.png
%{_datadir}/obs/

%files libs
%{_libdir}/obs-plugins/
%{_libdir}/obs-scripting/
%{_libdir}/libobs-scripting.so
%{_libdir}/*.so.*

%files devel
%{_libdir}/cmake/LibObs/
%{_libdir}/pkgconfig/libobs.pc
%{_libdir}/*.so
%{_includedir}/obs/

%changelog
* Wed Feb 10 2021 Nicolas Chauvet <kwizart@gmail.com> - 26.1.2-3
- Add obs-vst plugins
- Build for all arches (armv7hl, aarch64, ppc64le)
- Re-order build dependencies

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 26.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Martin Gansser <martinkg@fedoraproject.org> - 26.1.2-1
- Update to 26.1.2

* Tue Jan 19 2021 Martin Gansser <martinkg@fedoraproject.org> - 26.1.1-1
- Update to 26.1.1

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 26.1.0-2
- Rebuilt for new ffmpeg snapshot

* Sat Dec 26 2020 Momcilo Medic <fedorauser@fedoraproject.org> - 26.1.0-1
- Updated to 26.1.0

* Fri Nov 27 2020 S??rgio Basto <sergio@serjux.com> - 26.0.2-3
- Mass rebuild for x264-0.161

* Wed Oct 14 2020 Momcilo Medic <fedorauser@fedoraproject.org> - 26.0.2-2
- Bumped release for setting developer toolset version

* Wed Oct 14 2020 Momcilo Medic <fedorauser@fedoraproject.org> - 26.0.2-1
- Removed doxygen bits as upstream removed it
- Updated to 26.0.2

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 25.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Aug 06 2020 Leigh Scott <leigh123linux@gmail.com> - 25.0.8-4
- Improve compatibility with new CMake macro

* Tue Jul 07 2020 S??rgio Basto <sergio@serjux.com> - 25.0.8-3
- Mass rebuild for x264

* Sat May 30 2020 Leigh Scott <leigh123linux@gmail.com> - 25.0.8-2
- Rebuild for python-3.9

* Tue Apr 28 2020 Leigh Scott <leigh123linux@googlemail.com> - 25.0.8-1
- Updated to 25.0.8

* Thu Apr 16 2020 Leigh Scott <leigh123linux@gmail.com> - 25.0.6-1
- Updated to 25.0.6

* Mon Apr 06 2020 Momcilo Medic <fedorauser@fedoraproject.org> - 25.0.4-1
- Updated to 25.0.4

* Tue Mar 31 2020 Momcilo Medic <fedorauser@fedoraproject.org> - 25.0.3-1
- Updated to 25.0.3

* Fri Mar 20 2020 Martin Gansser <martinkg@fedoraproject.org> - 25.0.1-1
- Update to 25.0.1

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 24.0.6-2
- Rebuild for ffmpeg-4.3 git

* Fri Feb 21 2020 Martin Gansser <martinkg@fedoraproject.org> - 24.0.6-1
- Update to 24.0.6

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 24.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 24.0.5-1
- Updated to 24.0.5

* Tue Dec 17 2019 Leigh Scott <leigh123linux@gmail.com> - 24.0.3-3
- Mass rebuild for x264

* Sun Oct 13 2019 Momcilo Medic <fedorauser@fedoraproject.org> - 24.0.3-2
- Switched BR gcc-objc to gcc to unify SPEC file across builds

* Sat Oct 12 2019 Momcilo Medic <fedorauser@fedoraproject.org> - 24.0.3-1
- Updated to 24.0.3

* Sun Sep 22 2019 Momcilo Medic <fedorauser@fedoraproject.org> - 24.0.1-1
- Updated to 24.0.1

* Sat Aug 24 2019 Leigh Scott <leigh123linux@gmail.com> - 23.2.1-3
- Rebuild for python-3.8

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 23.2.1-2
- Rebuild for new ffmpeg version

* Tue Jun 18 2019 Momcilo Medic <fedorauser@fedoraproject.org> - 23.2.1-1
- Updated to 23.2.1

* Mon Apr 08 2019 Momcilo Medic <fedorauser@fedoraproject.org> - 23.1.0-1
- Updated to 23.1.0

* Sun Apr 07 2019 Martin Gansser <martinkg@fedoraproject.org> - 23.0.2-4
- Add obs-frontend-api.h to devel subpkg, to enable build of obs-ndi
- Add ObsPluginHelpers.cmake to devel subpkg, to enable build of obs-ndi

* Mon Mar 18 2019 Xavier Bachelot <xavier@bachelot.org> - 23.0.2-3
- Fix BR: on speex/speexdsp for EL7.
- Fix BR: on python for EL7.

* Tue Mar 12 2019 S??rgio Basto <sergio@serjux.com> - 23.0.2-2
- Mass rebuild for x264

* Sun Mar 10 2019 Momcilo Medic <fedorauser@fedoraproject.org> - 23.0.2-1
- Updated to 23.0.2

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 23.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Feb 25 2019 Momcilo Medic <fedorauser@fedoraproject.org> - 23.0.0-1
- Updated to 23.0.0

* Wed Jan 9 2019 Momcilo Medic <fedorauser@fedoraproject.org> - 22.0.3-3
- Fixed missing dependencies
- Enabled scripting support

* Thu Oct 04 2018 S??rgio Basto <sergio@serjux.com> - 22.0.3-2
- Mass rebuild for x264 and/or x265

* Fri Sep 7 2018 Momcilo Medic <fedorauser@fedoraproject.org> - 22.0.3-1
- Updated to 22.0.3

* Wed Aug 22 2018 Momcilo Medic <fedorauser@fedoraproject.org> - 22.0.1-1
- Updated to 22.0.1

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 21.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Miro Hron??ok <mhroncok@redhat.com> - 21.1.2-2
- Rebuilt for Python 3.7

* Wed May 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 21.1.2-1
- Update to 21.1.2
- Fix requires

* Sat Mar 31 2018 Leigh Scott <leigh123linux@googlemail.com> - 21.1.1-1
- Update to 21.1.1

* Mon Mar 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 21.1.0-1
- Update to 21.1.0

* Fri Mar 09 2018 Martin Gansser <martinkg@fedoraproject.org> - 21.0.3-1
- Update to 21.0.3
- Add BR python3-devel
- Add bytecompile with Python 3 %%global __python %%{__python3}A

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 21.0.2-4
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 21.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 08 2018 Leigh Scott <leigh123linux@googlemail.com> - 21.0.2-2
- Fix scriptlets
- Use ninja to build

* Wed Feb 07 2018 Momcilo Medic <fedorauser@fedoraproject.org> - 21.0.2-1
- Updated to 21.0.2

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 20.1.3-3
- Rebuilt for ffmpeg-3.5 git

* Sun Dec 31 2017 S??rgio Basto <sergio@serjux.com> - 20.1.3-2
- Mass rebuild for x264 and x265

* Fri Dec 08 2017 Leigh Scott <leigh123linux@googlemail.com> - 20.1.3-1
- Updated to 20.1.3

* Tue Oct 17 2017 Martin Gansser <martinkg@fedoraproject.org> - 20.0.1-1
- Updated to 20.0.1

* Thu Aug 10 2017 Momcilo Medic <fedorauser@fedoraproject.org> - 20.0.0-1
- Updated to 20.0.0

* Sat Jul 08 2017 Martin Gansser <martinkg@fedoraproject.org> - 19.0.3-1
- Updated to 19.0.3

* Mon May 22 2017 Momcilo Medic <fedorauser@fedoraproject.org> - 19.0.2-1
- Updated to 19.0.2

* Wed May 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 18.0.2-2
- Rebuild for ffmpeg update

* Sat May 6 2017 Momcilo Medic <fedorauser@fedoraproject.org> - 18.0.2-1
- Updated to 18.0.2

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 18.0.1-3
- Rebuild for ffmpeg update

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 18.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 8 2017 Momcilo Medic <fedorauser@fedoraproject.org> - 18.0.1-1
- Updated to 18.0.1

* Wed Mar 1 2017 Momcilo Medic <fedorauser@fedoraproject.org> - 18.0.0-1
- Updated to 18.0.0

* Mon Jan 30 2017 Momcilo Medic <fedorauser@fedoraproject.org> - 17.0.2-2
- Reintroduced obs-ffmpeg-mux.patch
- Fixes #4436

* Wed Jan 18 2017 Momcilo Medic <fedorauser@fedoraproject.org> - 17.0.2-1
- Updated to 17.0.2

* Tue Jan 03 2017 Momcilo Medic <fedorauser@fedoraproject.org> - 17.0.0-1
- Upstream fixed arch-dependent-file-in-usr-share
- Removed obs-ffmpeg-mux.patch
- Updated to 17.0.0

* Sun Nov 27 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.16.6-1
- Updated to 0.16.6

* Tue Nov 08 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.16.5-1
- Updated to 0.16.5

* Tue Oct 18 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.16.2-2.20161018git4505d5a
- Updated to git to resolve unversioned shared object
- Identified speexdsp-devel as a dependency

* Sat Oct 01 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.16.2-1
- Updated to 0.16.2
- Build doxygen html documentation
- Added BR doxygen

* Fri Aug 26 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.15.4-3
- Actually define FFMPEG_MUX_FIXED (fixes 'command not found' when trying to record)

* Sat Aug 13 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.15.4-2
- Disable build for ARM (Arm gcc has no xmmintrin.h file)

* Fri Aug 12 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.15.4-1
- Fix release tag (0.x release is for git releases)

* Mon Aug 08 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.15.4-0.1
- Updated to 0.15.4

* Fri Aug 05 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.15.2-0.5
- Added alsa-devel as BR for ALSA plugin.
- Added vlc-devel as BR for VLC plugin.
- Added systemd-devel as BR for Udev V4L.

* Wed Aug 03 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.15.2-0.4
- Fix source tag (spectool now downloads in n-v format)
- Remove surplus ldconfig from postun (no public .so files in main package)
- Update scriptlets to meet guidelines (need full path)

* Wed Jul 20 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.15.2-0.3
- Added license file gplv2.txt

* Mon Jul 18 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.15.2-0.2
- Fixed arch-dependent-file-in-usr-share
- Added obs-ffmpeg-mux.patch
- Added libs subpkg
- Call ldconfig in post(un) scripts for the shared library

* Sat Jul 16 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.15.2-0.1
- Updated to 0.15.2

* Sun Jul 10 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.15.1-0.1
- Updated to 0.15.1

* Sat Jul 09 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.15.0-0.1
- Updated to 0.15.0

* Mon May 16 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.14.2-0.1
- Updated to 0.14.2

* Mon Apr 25 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.14.1-0.1
- Updated to 0.14.1

* Sun Apr 24 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.14.0-0.1
- Updated to 0.14.0

* Tue Mar 22 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.13.4-0.1
- Updated to 0.13.4

* Sun Mar 20 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.13.3-0.1
- Updated to 0.13.3

* Tue Feb 23 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.13.2-0.1
- Updated to 0.13.2

* Sat Feb 06 2016 Momcilo Medic <fedorauser@fedoraproject.org> - 0.13.1-0.1
- Updated to 0.13.1

* Sun Dec 20 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.12.4-0.2
- replace OBS_MULTIARCH_SUFFIX by LIB_SUFFIX

* Sat Dec 12 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.12.4-0.1
- Updated to 0.12.4

* Sat Dec 05 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.12.3-0.1
- Updated to 0.12.3

* Sat Nov 21 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.12.2-0.1
- Updated to 0.12.2

* Thu Nov 19 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.12.1-0.1
- Updated to 0.12.1

* Thu Sep 24 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.12.0-0.1
- Updated to 0.12.0

* Mon Aug 17 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.11.4-0.1
- Added OBS_VERSION_OVERRIDE to correct version in compilation
- Updated to 0.11.4

* Sat Aug 08 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.11.3-0.1
- Updated to 0.11.3

* Thu Jul 30 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.11.2-0.1
- Updated to 0.11.2

* Fri Jul 10 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.11.1-0.1
- Updated to 0.11.1

* Wed May 27 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.10.1-0.1
- Initial .spec file
