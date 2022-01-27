%global fork Cantera
%global branch main

Name:          cantera
Version:       2.6.0
Release:       0.7.a4%{?dist}
Summary:       Chemical kinetics, thermodynamics, and transport tool suite
License:       BSD
URL:           https://github.com/%{fork}/%{name}/
Source0:       %{url}archive/%{branch}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  eigen3-devel
BuildRequires:  fmt-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
BuildRequires:  python3
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-pytest
BuildRequires:  python3-ruamel-yaml
BuildRequires:  python3-scons
BuildRequires:  sundials-devel
BuildRequires:  yaml-cpp-devel

%if 0%{?fedora}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif

%global scons scons%{?rhel:-3}


%global common_description %{expand: \
 Cantera is a suite of object-oriented software tools for solving problems
 involving chemical kinetics, thermodynamics, and/or transport processes.
 Cantera can be used for simulating time-dependent or steady reactor
 networks and one-dimensional reacting flows. Thermodynamic models for
 ideal gases, aqueous electrolytes, plasmas, and multiphase substances
 are provided.}

%description
%{common_description}


%package common
Summary: Common files needed for all Cantera interfaces
%description common
%{common_description}
 .
 This package includes programs for parsing and converting chemical
 mechanisms, a set of common mechanism files, and several sample problems.


%package -n python3-%{name}
Requires: %{name}-common%{_isa} = %{version}-%{release}
Summary: Python 3 user interface for Cantera
%description -n python3-%{name}
%{common_description}
 .
 This package includes the Cantera Python 3 module.


%package devel
Requires: %{name}-common%{_isa} = %{version}-%{release}
Summary: Header files and shared object libraries for Cantera
%description devel
%{common_description}
 .
 This package contains the header files and shared object libraries needed to
 develop applications with the C++ and Fortran interfaces of Cantera.


%package static
Requires: %{name}-common%{_isa} = %{version}-%{release}
Summary: Static libraries for Cantera
%description static
%{common_description}
 .
 This package contains the static libraries for the C++ and Fortran
 interfaces of Cantera.


%prep
%autosetup -n %{name}-%{branch}


%build
%set_build_flags

%scons build prefix=%{_prefix} libdirname=%{_lib} system_sundials=y f90_interface=y renamed_shared_libraries=n python_package=full system_eigen=y extra_inc_dirs=/usr/include/eigen3 system_fmt=y


%install
%scons install prefix=%{_prefix} libdirname=%{_lib} stage_dir=%{buildroot}


%check
%scons test verbose_tests=y


%files common
%license %{_datadir}/%{name}/doc/LICENSE.txt

%doc AUTHORS README.rst
%doc %{_mandir}/man1/ck2cti.1.gz
%doc %{_mandir}/man1/ck2yaml.1.gz
%doc %{_mandir}/man1/cti2yaml.1.gz
%doc %{_mandir}/man1/ctml2yaml.1.gz
%doc %{_mandir}/man1/ctml_writer.1.gz

%{_bindir}/ck2cti
%{_bindir}/ck2yaml
%{_bindir}/cti2yaml
%{_bindir}/ctml2yaml
%{_bindir}/ctml_writer

%{_datadir}/%{name}


%files -n python3-%{name}
%{python3_sitearch}/Cantera-%{version}a4-py%{python3_version}.egg-info/
%{python3_sitearch}/%{name}/


%files devel
%{_includedir}/%{name}

%{_libdir}/pkgconfig/cantera.pc
%{_libdir}/libcantera.so
%{_libdir}/libcantera.so.2
%{_libdir}/libcantera.so.%{version}
%{_libdir}/libcantera_fortran.so
%{_libdir}/libcantera_fortran.so.2
%{_libdir}/libcantera_fortran.so.%{version}

%{_bindir}/setup_cantera
%{_bindir}/setup_cantera.csh


%files static
%{_libdir}/libcantera.a
%{_libdir}/libcantera_fortran.a


%changelog
* Sun Jan 23 2022 Mark E. Fuller <mark.e.fuller@gmx.de> - 2.6.0-0.7.a4
- first real Fedora deploy

* Sun Jan 23 2022 Mark E. Fuller <mark.e.fuller@gmx.de> - 2.6.0-0.6.a4
- Final revisions for Fedora approval
- Remove workaround fixed by #1172 (Issue #1149)
- Version for first Fedora builds
- Exclude s390x due to failing tests
- Exclude ppc64le in Rawhide due to build segfaults
- Rename Python package to follow Fedora standards

* Thu Jan 13 2022 Mark E. Fuller <mark.e.fuller@gmx.de> - 2.6.0-0.5.a4
- Move static libraries from devel to static subpackage

* Thu Jan 06 2022 Mark E. Fuller <mark.e.fuller@gmx.de> - 2.6.0-0.4.a4
- Cleanup spec per Fedora package review

* Sun Jan 02 2022 Mark E. Fuller <fuller@fedoraproject.org> - 2.6.0-0.3.a4
- Bump dist to a4

* Thu Dec 23 2021 Mark E. Fuller <fuller@fedoraproject.org> - 2.6.0-0.2.a3
- Bump dist to reflect many merged commits in a3 since October

* Tue Nov 30 2021 Mark E. Fuller <fuller@fedoraproject.org> - 2.6.0-0.1.a3
- Introduced distro-specific IF to build on both Fedora and RHEL

* Thu Nov 18 2021 Mark E. Fuller <fuller@fedoraproject.org> - 2.6.0-0.1.a3
- Moved "setup_cantera*" to devel
- Make all included files explicit

* Thu Oct 14 2021 Mark E. Fuller <fuller@fedoraproject.org> - 2.6.0-0.1.a3
- first attempt versions of spec file and packaging
