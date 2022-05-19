%global fork Cantera
%global branch main

Name:          cantera
Version:       2.6.0
Release:       ci%{?dist}
Summary:       Chemical kinetics, thermodynamics, and transport tool suite
License:       BSD
URL:           https://github.com/%{fork}/%{name}/
Source0:       %{url}/archive/%{branch}.tar.gz


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
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-ruamel-yaml
BuildRequires:  python3-scons
BuildRequires:  python3-wheel
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
%autosetup -n cantera-%{branch}


%build
%set_build_flags

%scons build prefix=%{_prefix} python_prefix=%{_prefix} libdirname=%{_lib} system_sundials=y f90_interface=y renamed_shared_libraries=n python_package=full system_eigen=y extra_inc_dirs=/usr/include/eigen3 system_fmt=y


%install
%scons install prefix=%{_prefix} python_prefix=%{_prefix} libdirname=%{_lib} stage_dir=%{buildroot}

###kludges for https://github.com/Cantera/cantera/issues/1233

# incorrect installation to /usr/local/bin on F36+
%if 0%{?fedora} >= 36
mv %{buildroot}%{_prefix}/local/bin/* %{buildroot}%{_bindir}/
rm -rf %{buildroot}%{_prefix}/local/bin
%endif

# incorrect installation to /usr/lib/ on 64 bit systems on F36-
%if 0%{?fedora} <= 36
if [[ -d %{buildroot}%{_prefix}/lib/python%{python3_version}/site-packages ]] && [ %{_lib} == "lib64" ]; then
  mkdir -p %{buildroot}%{python3_sitearch}/
  mv %{buildroot}%{_prefix}/lib/python%{python3_version}/site-packages/* %{buildroot}%{python3_sitearch}/
fi
if [[ -d %{buildroot}%{_prefix}/local/lib/python%{python3_version}/site-packages ]] && [ %{_lib} == "lib64" ]; then
  mkdir -p %{buildroot}%{python3_sitearch}/
  mv %{buildroot}%{_prefix}/local/lib/python%{python3_version}/site-packages/* %{buildroot}%{python3_sitearch}/
fi
%endif

# incorrect installation to /usr/local/lib* on F36+
%if 0%{?fedora} >= 36
mkdir -p %{buildroot}%{python3_sitearch}/
mv %{buildroot}%{_prefix}/local/%{_lib}/python%{python3_version}/site-packages/* %{buildroot}%{python3_sitearch}/
rm -rf %{buildroot}%{_prefix}/local/
%endif
###end_kludge

%check
%scons test


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

#not required for packaged installations
%ghost %{_bindir}/setup_cantera
%ghost %{_bindir}/setup_cantera.csh


%files -n python3-%{name}
%{python3_sitearch}/Cantera-%{version}.dist-info/
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


%files static
%{_libdir}/libcantera.a
%{_libdir}/libcantera_fortran.a



%changelog
* Tue May 3 2022 Mark E. Fuller <fuller@fedoraproject.org> - 2.6.0-ci
- Spec for CI on COPR (nightly/triggered)
