Name:          cantera
Version:       2.5.1
Release:       1%{?dist}
Summary:       Chemical kinetics, thermodynamics, and transport tool suite
License:       BSD-3-Clause
URL:           https://github.com/Cantera/cantera/
Source0:       https://github.com/Cantera/cantera/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  eigen3-devel
BuildRequires:  fmt-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-fortran
BuildRequires:  git
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
BuildRequires:  python3
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-ruamel-yaml
BuildRequires:  python3-scons
BuildRequires:  sundials-devel
BuildRequires:  yaml-cpp-devel


%description
 Cantera is a suite of object-oriented software tools for solving problems
 involving chemical kinetics, thermodynamics, and/or transport processes.
 Cantera can be used for simulating time-dependent or steady reactor
 networks and one-dimensional reacting flows. Thermodynamic models for
 ideal gases, aqueous electrolytes, plasmas, and multiphase substances
 are provided.

%package common
Summary: Common files needed for all Cantera interfaces
%description common
 Cantera is a suite of object-oriented software tools for solving problems
 involving chemical kinetics, thermodynamics, and/or transport processes.
 Cantera can be used for simulating time-dependent or steady reactor
 networks and one-dimensional reacting flows. Thermodynamic models for
 ideal gases, aqueous electrolytes, plasmas, and multiphase substances
 are provided.
 .
 This package includes programs for parsing and converting chemical
 mechanisms, a set of common mechanism files, and several sample problems.

%package python3
Requires: %{name}-common%{_isa} = %{version}-%{release}
Summary: Python 3 user interface for Cantera
%description python3
 Cantera is a suite of object-oriented software tools for solving problems
 involving chemical kinetics, thermodynamics, and/or transport processes.
 Cantera can be used for simulating time-dependent or steady reactor
 networks and one-dimensional reacting flows. Thermodynamic models for
 ideal gases, aqueous electrolytes, plasmas, and multiphase substances
 are provided.
 .
 This package includes the Cantera Python 3 module.

%package devel
Requires: %{name}-common%{_isa} = %{version}-%{release}
Summary: Header files and static libraries for Cantera
%description devel
 Cantera is a suite of object-oriented software tools for solving problems
 involving chemical kinetics, thermodynamics, and/or transport processes.
 Cantera can be used for simulating time-dependent or steady reactor
 networks and one-dimensional reacting flows. Thermodynamic models for
 ideal gases, aqueous electrolytes, plasmas, and multiphase substances
 are provided.
 .
 These files are used for developing applications that use Cantera's
 C++ and Fortran interfaces.


%prep
%autosetup -n %{name}-%{version}


%build
%set_build_flags
scons build prefix=%{_prefix} libdirname=%{_lib} system_sundials=y f90_interface=y renamed_shared_libraries=n python_package=full system_eigen=y extra_inc_dirs=/usr/include/eigen3 system_fmt=y

%install
scons install stage_dir=%{buildroot}


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
%{_bindir}/setup_cantera
%{_bindir}/setup_cantera.csh
%{_datadir}/%{name}/data/
%{_datadir}/%{name}/samples/

%files python3
%{python3_sitearch}/Cantera-%{version}-py%{python3_version}.egg-info/
%{python3_sitearch}/%{name}/

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/cantera.pc
%{_libdir}/libcantera.a
%{_libdir}/libcantera.so
%{_libdir}/libcantera.so.2
%{_libdir}/libcantera.so.%{version}
%{_libdir}/libcantera_fortran.a
%{_libdir}/libcantera_fortran.so
%{_libdir}/libcantera_fortran.so.2
%{_libdir}/libcantera_fortran.so.%{version}


%changelog
* Tue Oct 19 2021 Mark E. Fuller <fuller@fedoraproject.org>
- v2.5.1 variant created
* Thu Oct 14 2021 Mark E. Fuller <fuller@fedoraproject.org>
- first attempt versions of spec file and packaging
