Name:          cantera
Version:       2.6.0
Release:       0.3.a4%{?dist}
Summary:       Chemical kinetics, thermodynamics, and transport tool suite
License:       BSD-3-Clause
URL:           https://github.com/Cantera/cantera/
Source0:       https://github.com/Cantera/cantera/archive/main.tar.gz

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
%autosetup -n %{name}-main


%build
%set_build_flags
scons build prefix=%{_prefix} libdirname=%{_lib} system_sundials=y f90_interface=y renamed_shared_libraries=n python_package=full system_eigen=y extra_inc_dirs=/usr/include/eigen3 system_fmt=y

%install
scons install stage_dir=%{buildroot}
mv %{buildroot}%{_prefix}/local/bin/ck2cti %{buildroot}%{_prefix}/bin/ck2cti
mv %{buildroot}%{_prefix}/local/bin/ck2yaml %{buildroot}%{_prefix}/bin/ck2yaml
mv %{buildroot}%{_prefix}/local/bin/cti2yaml %{buildroot}%{_prefix}/bin/cti2yaml
mv %{buildroot}%{_prefix}/local/bin/ctml2yaml %{buildroot}%{_prefix}/bin/ctml2yaml
mv %{buildroot}%{_prefix}/local/bin/ctml_writer %{buildroot}%{_prefix}/bin/ctml_writer


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
%{_datadir}/%{name}/data/sample-data/LiC6_electrodebulk.yaml
%{_datadir}/%{name}/data/KOH.cti
%{_datadir}/%{name}/data/KOH.xml
%{_datadir}/%{name}/data/KOH.yaml
%{_datadir}/%{name}/data/air.cti
%{_datadir}/%{name}/data/air.xml
%{_datadir}/%{name}/data/air.yaml
%{_datadir}/%{name}/data/airNASA9.cti
%{_datadir}/%{name}/data/airNASA9.xml
%{_datadir}/%{name}/data/airNASA9.yaml
%{_datadir}/%{name}/data/argon.cti
%{_datadir}/%{name}/data/argon.xml
%{_datadir}/%{name}/data/critical-properties.yaml
%{_datadir}/%{name}/data/diamond.cti
%{_datadir}/%{name}/data/diamond.xml
%{_datadir}/%{name}/data/diamond.yaml
%{_datadir}/%{name}/data/elements.xml
%{_datadir}/%{name}/data/graphite.cti
%{_datadir}/%{name}/data/graphite.xml
%{_datadir}/%{name}/data/graphite.yaml
%{_datadir}/%{name}/data/gri30.cti
%{_datadir}/%{name}/data/gri30.xml
%{_datadir}/%{name}/data/gri30.yaml
%{_datadir}/%{name}/data/gri30_highT.cti
%{_datadir}/%{name}/data/gri30_highT.xml
%{_datadir}/%{name}/data/gri30_highT.yaml
%{_datadir}/%{name}/data/gri30_ion.cti
%{_datadir}/%{name}/data/gri30_ion.xml
%{_datadir}/%{name}/data/gri30_ion.yaml
%{_datadir}/%{name}/data/h2o2.cti
%{_datadir}/%{name}/data/h2o2.xml
%{_datadir}/%{name}/data/h2o2.yaml
%{_datadir}/%{name}/data/liquidvapor.cti
%{_datadir}/%{name}/data/liquidvapor.xml
%{_datadir}/%{name}/data/liquidvapor.yaml
%{_datadir}/%{name}/data/lithium_ion_battery.cti
%{_datadir}/%{name}/data/lithium_ion_battery.xml
%{_datadir}/%{name}/data/lithium_ion_battery.yaml
%{_datadir}/%{name}/data/methane_pox_on_pt.cti
%{_datadir}/%{name}/data/methane_pox_on_pt.xml
%{_datadir}/%{name}/data/methane_pox_on_pt.yaml
%{_datadir}/%{name}/data/nDodecane_Reitz.cti
%{_datadir}/%{name}/data/nDodecane_Reitz.xml
%{_datadir}/%{name}/data/nDodecane_Reitz.yaml
%{_datadir}/%{name}/data/nasa.cti
%{_datadir}/%{name}/data/nasa.xml
%{_datadir}/%{name}/data/nasa_condensed.cti
%{_datadir}/%{name}/data/nasa_condensed.xml
%{_datadir}/%{name}/data/nasa_condensed.yaml
%{_datadir}/%{name}/data/nasa_gas.cti
%{_datadir}/%{name}/data/nasa_gas.xml
%{_datadir}/%{name}/data/nasa_gas.yaml
%{_datadir}/%{name}/data/ohn.cti
%{_datadir}/%{name}/data/ohn.xml
%{_datadir}/%{name}/data/ohn.yaml
%{_datadir}/%{name}/data/ptcombust.cti
%{_datadir}/%{name}/data/ptcombust.xml
%{_datadir}/%{name}/data/ptcombust.yaml
%{_datadir}/%{name}/data/silane.cti
%{_datadir}/%{name}/data/silane.xml
%{_datadir}/%{name}/data/silane.yaml
%{_datadir}/%{name}/data/silicon.cti
%{_datadir}/%{name}/data/silicon.xml
%{_datadir}/%{name}/data/silicon.yaml
%{_datadir}/%{name}/data/silicon_carbide.cti
%{_datadir}/%{name}/data/silicon_carbide.xml
%{_datadir}/%{name}/data/silicon_carbide.yaml
%{_datadir}/%{name}/data/sofc.cti
%{_datadir}/%{name}/data/sofc.xml
%{_datadir}/%{name}/data/sofc.yaml
%{_datadir}/%{name}/data/water.cti
%{_datadir}/%{name}/data/water.xml
%{_datadir}/%{name}/data/water.yaml
%{_datadir}/%{name}/samples/cxx/LiC6_electrode/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/LiC6_electrode/Makefile
%{_datadir}/%{name}/samples/cxx/LiC6_electrode/SConstruct
%{_datadir}/%{name}/samples/cxx/LiC6_electrode/LiC6_electrode.cpp
%{_datadir}/%{name}/samples/cxx/bvp/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/bvp/Makefile
%{_datadir}/%{name}/samples/cxx/bvp/SConstruct
%{_datadir}/%{name}/samples/cxx/bvp/blasius.cpp
%{_datadir}/%{name}/samples/cxx/bvp/BoundaryValueProblem.h
%{_datadir}/%{name}/samples/cxx/combustor/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/combustor/Makefile
%{_datadir}/%{name}/samples/cxx/combustor/SConstruct
%{_datadir}/%{name}/samples/cxx/combustor/combustor.cpp
%{_datadir}/%{name}/samples/cxx/custom/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/custom/Makefile
%{_datadir}/%{name}/samples/cxx/custom/SConstruct
%{_datadir}/%{name}/samples/cxx/custom/custom.cpp
%{_datadir}/%{name}/samples/cxx/demo/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/demo/Makefile
%{_datadir}/%{name}/samples/cxx/demo/SConstruct
%{_datadir}/%{name}/samples/cxx/demo/demo.cpp
%{_datadir}/%{name}/samples/cxx/flamespeed/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/flamespeed/Makefile
%{_datadir}/%{name}/samples/cxx/flamespeed/SConstruct
%{_datadir}/%{name}/samples/cxx/flamespeed/flamespeed.cpp
%{_datadir}/%{name}/samples/cxx/gas_transport/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/gas_transport/Makefile
%{_datadir}/%{name}/samples/cxx/gas_transport/SConstruct
%{_datadir}/%{name}/samples/cxx/gas_transport/gas_transport.cpp
%{_datadir}/%{name}/samples/cxx/kinetics1/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/kinetics1/Makefile
%{_datadir}/%{name}/samples/cxx/kinetics1/SConstruct
%{_datadir}/%{name}/samples/cxx/kinetics1/kinetics1.cpp
%{_datadir}/%{name}/samples/cxx/kinetics1/example_utils.h
%{_datadir}/%{name}/samples/cxx/openmp_ignition/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/openmp_ignition/Makefile
%{_datadir}/%{name}/samples/cxx/openmp_ignition/SConstruct
%{_datadir}/%{name}/samples/cxx/openmp_ignition/openmp_ignition.cpp
%{_datadir}/%{name}/samples/cxx/rankine/CMakeLists.txt
%{_datadir}/%{name}/samples/cxx/rankine/Makefile
%{_datadir}/%{name}/samples/cxx/rankine/SConstruct
%{_datadir}/%{name}/samples/cxx/rankine/rankine.cpp
%{_datadir}/%{name}/samples/f77/Makefile
%{_datadir}/%{name}/samples/f77/SConstruct
%{_datadir}/%{name}/samples/f77/ctlib.f
%{_datadir}/%{name}/samples/f77/demo.f
%{_datadir}/%{name}/samples/f77/demo_ftnlib.cpp
%{_datadir}/%{name}/samples/f77/isentropic.f
%{_datadir}/%{name}/samples/f90/CMakeLists.txt
%{_datadir}/%{name}/samples/f90/Makefile
%{_datadir}/%{name}/samples/f90/SConstruct
%{_datadir}/%{name}/samples/f90/demo.f90

%files python3
%{python3_sitearch}/Cantera-%{version}a4-py%{python3_version}.egg-info/
%{python3_sitearch}/%{name}/

%files devel
%{_includedir}/%{name}/cantera_funcs.mod
%{_includedir}/%{name}/cantera_iface.mod
%{_includedir}/%{name}/cantera_kinetics.mod
%{_includedir}/%{name}/Cantera.mak
%{_includedir}/%{name}/cantera.mod
%{_includedir}/%{name}/cantera_thermo.mod
%{_includedir}/%{name}/cantera_transport.mod
%{_includedir}/%{name}/cantera_xml.mod
%{_includedir}/%{name}/fct.mod
%{_includedir}/%{name}/fctxml.mod
%{_includedir}/%{name}/kinetics.h
%{_includedir}/%{name}/onedim.h
%{_includedir}/%{name}/reactionpaths.h
%{_includedir}/%{name}/thermo.h
%{_includedir}/%{name}/transport.h
%{_includedir}/%{name}/zerodim.h
%{_includedir}/%{name}/base/AnyMap.h
%{_includedir}/%{name}/base/AnyMap.inl.h
%{_includedir}/%{name}/base/Array.h
%{_includedir}/%{name}/base/clockWC.h
%{_includedir}/%{name}/base/config.h
%{_includedir}/%{name}/base/config.h.in
%{_includedir}/%{name}/base/ct_defs.h
%{_includedir}/%{name}/base/ctexceptions.h
%{_includedir}/%{name}/base/ctml.h
%{_includedir}/%{name}/base/Delegator.h
%{_includedir}/%{name}/base/FactoryBase.h
%{_includedir}/%{name}/base/fmt.h
%{_includedir}/%{name}/base/global.h
%{_includedir}/%{name}/base/logger.h
%{_includedir}/%{name}/base/plots.h
%{_includedir}/%{name}/base/Solution.h
%{_includedir}/%{name}/base/stringUtils.h
%{_includedir}/%{name}/base/Units.h
%{_includedir}/%{name}/base/utilities.h
%{_includedir}/%{name}/base/ValueCache.h
%{_includedir}/%{name}/base/xml.h
%{_includedir}/%{name}/base/yaml.h
%{_includedir}/%{name}/base/YamlWriter.h
%{_includedir}/%{name}/clib/clib_defs.h
%{_includedir}/%{name}/clib/ctfunc.h
%{_includedir}/%{name}/clib/ct.h
%{_includedir}/%{name}/clib/ctmatlab.h
%{_includedir}/%{name}/clib/ctmultiphase.h
%{_includedir}/%{name}/clib/ctonedim.h
%{_includedir}/%{name}/clib/ctreactor.h
%{_includedir}/%{name}/clib/ctrpath.h
%{_includedir}/%{name}/clib/ctsurf.h
%{_includedir}/%{name}/clib/ctxml.h
%{_includedir}/%{name}/cython/funcWrapper.h
%{_includedir}/%{name}/cython/wrappers.h
%{_includedir}/%{name}/equil/ChemEquil.h
%{_includedir}/%{name}/equil/MultiPhaseEquil.h
%{_includedir}/%{name}/equil/MultiPhase.h
%{_includedir}/%{name}/equil/vcs_defs.h
%{_includedir}/%{name}/equil/vcs_internal.h
%{_includedir}/%{name}/equil/vcs_MultiPhaseEquil.h
%{_includedir}/%{name}/equil/vcs_solve.h
%{_includedir}/%{name}/equil/vcs_SpeciesProperties.h
%{_includedir}/%{name}/equil/vcs_species_thermo.h
%{_includedir}/%{name}/equil/vcs_VolPhase.h
%{_includedir}/%{name}/kinetics/Arrhenius.h
%{_includedir}/%{name}/kinetics/BulkKinetics.h
%{_includedir}/%{name}/kinetics/Custom.h
%{_includedir}/%{name}/kinetics/EdgeKinetics.h
%{_includedir}/%{name}/kinetics/FalloffFactory.h
%{_includedir}/%{name}/kinetics/Falloff.h
%{_includedir}/%{name}/kinetics/FalloffMgr.h
%{_includedir}/%{name}/kinetics/GasKinetics.h
%{_includedir}/%{name}/kinetics/Group.h
%{_includedir}/%{name}/kinetics/ImplicitSurfChem.h
%{_includedir}/%{name}/kinetics/importKinetics.h
%{_includedir}/%{name}/kinetics/InterfaceKinetics.h
%{_includedir}/%{name}/kinetics/KineticsFactory.h
%{_includedir}/%{name}/kinetics/Kinetics.h
%{_includedir}/%{name}/kinetics/MultiRate.h
%{_includedir}/%{name}/kinetics/MultiRateBase.h
%{_includedir}/%{name}/kinetics/RateCoeffMgr.h
%{_includedir}/%{name}/kinetics/ReactionData.h
%{_includedir}/%{name}/kinetics/reaction_defs.h
%{_includedir}/%{name}/kinetics/ReactionFactory.h
%{_includedir}/%{name}/kinetics/Reaction.h
%{_includedir}/%{name}/kinetics/ReactionPath.h
%{_includedir}/%{name}/kinetics/ReactionRateFactory.h
%{_includedir}/%{name}/kinetics/ReactionRate.h
%{_includedir}/%{name}/kinetics/RxnRates.h
%{_includedir}/%{name}/kinetics/solveSP.h
%{_includedir}/%{name}/kinetics/StoichManager.h
%{_includedir}/%{name}/kinetics/ThirdBodyCalc.h
%{_includedir}/%{name}/numerics/BandMatrix.h
%{_includedir}/%{name}/numerics/ctlapack.h
%{_includedir}/%{name}/numerics/CVodesIntegrator.h
%{_includedir}/%{name}/numerics/DAE_Solver.h
%{_includedir}/%{name}/numerics/DenseMatrix.h
%{_includedir}/%{name}/numerics/eigen_dense.h
%{_includedir}/%{name}/numerics/eigen_sparse.h
%{_includedir}/%{name}/numerics/Func1.h
%{_includedir}/%{name}/numerics/FuncEval.h
%{_includedir}/%{name}/numerics/funcs.h
%{_includedir}/%{name}/numerics/GeneralMatrix.h
%{_includedir}/%{name}/numerics/IDA_Solver.h
%{_includedir}/%{name}/numerics/Integrator.h
%{_includedir}/%{name}/numerics/polyfit.h
%{_includedir}/%{name}/numerics/ResidEval.h
%{_includedir}/%{name}/numerics/ResidJacEval.h
%{_includedir}/%{name}/oneD/Boundary1D.h
%{_includedir}/%{name}/oneD/Domain1D.h
%{_includedir}/%{name}/oneD/Inlet1D.h
%{_includedir}/%{name}/oneD/IonFlow.h
%{_includedir}/%{name}/oneD/MultiJac.h
%{_includedir}/%{name}/oneD/MultiNewton.h
%{_includedir}/%{name}/oneD/OneDim.h
%{_includedir}/%{name}/oneD/refine.h
%{_includedir}/%{name}/oneD/Sim1D.h
%{_includedir}/%{name}/oneD/StFlow.h
%{_includedir}/%{name}/test/gtest_utils.h
%{_includedir}/%{name}/thermo/BinarySolutionTabulatedThermo.h
%{_includedir}/%{name}/thermo/ConstCpPoly.h
%{_includedir}/%{name}/thermo/DebyeHuckel.h
%{_includedir}/%{name}/thermo/EdgePhase.h
%{_includedir}/%{name}/thermo/electrolytes.h
%{_includedir}/%{name}/thermo/Elements.h
%{_includedir}/%{name}/thermo/GibbsExcessVPSSTP.h
%{_includedir}/%{name}/thermo/HMWSoln.h
%{_includedir}/%{name}/thermo/IdealGasPhase.h
%{_includedir}/%{name}/thermo/IdealMolalSoln.h
%{_includedir}/%{name}/thermo/IdealSolidSolnPhase.h
%{_includedir}/%{name}/thermo/IdealSolnGasVPSS.h
%{_includedir}/%{name}/thermo/IonsFromNeutralVPSSTP.h
%{_includedir}/%{name}/thermo/LatticePhase.h
%{_includedir}/%{name}/thermo/LatticeSolidPhase.h
%{_includedir}/%{name}/thermo/MargulesVPSSTP.h
%{_includedir}/%{name}/thermo/MaskellSolidSolnPhase.h
%{_includedir}/%{name}/thermo/MetalPhase.h
%{_includedir}/%{name}/thermo/MixtureFugacityTP.h
%{_includedir}/%{name}/thermo/MolalityVPSSTP.h
%{_includedir}/%{name}/thermo/Mu0Poly.h
%{_includedir}/%{name}/thermo/MultiSpeciesThermo.h
%{_includedir}/%{name}/thermo/Nasa9Poly1.h
%{_includedir}/%{name}/thermo/Nasa9PolyMultiTempRegion.h
%{_includedir}/%{name}/thermo/NasaPoly1.h
%{_includedir}/%{name}/thermo/NasaPoly2.h
%{_includedir}/%{name}/thermo/PDSS_ConstVol.h
%{_includedir}/%{name}/thermo/PDSSFactory.h
%{_includedir}/%{name}/thermo/PDSS.h
%{_includedir}/%{name}/thermo/PDSS_HKFT.h
%{_includedir}/%{name}/thermo/PDSS_IdealGas.h
%{_includedir}/%{name}/thermo/PDSS_IonsFromNeutral.h
%{_includedir}/%{name}/thermo/PDSS_SSVol.h
%{_includedir}/%{name}/thermo/PDSS_Water.h
%{_includedir}/%{name}/thermo/PengRobinson.h
%{_includedir}/%{name}/thermo/Phase.h
%{_includedir}/%{name}/thermo/PureFluidPhase.h
%{_includedir}/%{name}/thermo/RedlichKisterVPSSTP.h
%{_includedir}/%{name}/thermo/RedlichKwongMFTP.h
%{_includedir}/%{name}/thermo/ShomatePoly.h
%{_includedir}/%{name}/thermo/SingleSpeciesTP.h
%{_includedir}/%{name}/thermo/Species.h
%{_includedir}/%{name}/thermo/SpeciesThermoFactory.h
%{_includedir}/%{name}/thermo/SpeciesThermoInterpType.h
%{_includedir}/%{name}/thermo/speciesThermoTypes.h
%{_includedir}/%{name}/thermo/StoichSubstance.h
%{_includedir}/%{name}/thermo/SurfPhase.h
%{_includedir}/%{name}/thermo/ThermoFactory.h
%{_includedir}/%{name}/thermo/ThermoPhase.h
%{_includedir}/%{name}/thermo/VPStandardStateTP.h
%{_includedir}/%{name}/thermo/WaterProps.h
%{_includedir}/%{name}/thermo/WaterPropsIAPWS.h
%{_includedir}/%{name}/thermo/WaterPropsIAPWSphi.h
%{_includedir}/%{name}/thermo/WaterSSTP.h
%{_includedir}/%{name}/tpx/Sub.h
%{_includedir}/%{name}/tpx/utils.h
%{_includedir}/%{name}/transport/DustyGasTransport.h
%{_includedir}/%{name}/transport/GasTransport.h
%{_includedir}/%{name}/transport/HighPressureGasTransport.h
%{_includedir}/%{name}/transport/IonGasTransport.h
%{_includedir}/%{name}/transport/MixTransport.h
%{_includedir}/%{name}/transport/MultiTransport.h
%{_includedir}/%{name}/transport/TransportBase.h
%{_includedir}/%{name}/transport/TransportData.h
%{_includedir}/%{name}/transport/TransportFactory.h
%{_includedir}/%{name}/transport/UnityLewisTransport.h
%{_includedir}/%{name}/transport/WaterTransport.h
%{_includedir}/%{name}/zeroD/ConstPressureReactor.h
%{_includedir}/%{name}/zeroD/flowControllers.h
%{_includedir}/%{name}/zeroD/FlowDeviceFactory.h
%{_includedir}/%{name}/zeroD/FlowDevice.h
%{_includedir}/%{name}/zeroD/FlowReactor.h
%{_includedir}/%{name}/zeroD/IdealGasConstPressureReactor.h
%{_includedir}/%{name}/zeroD/IdealGasReactor.h
%{_includedir}/%{name}/zeroD/ReactorBase.h
%{_includedir}/%{name}/zeroD/ReactorDelegator.h
%{_includedir}/%{name}/zeroD/ReactorFactory.h
%{_includedir}/%{name}/zeroD/Reactor.h
%{_includedir}/%{name}/zeroD/ReactorNet.h
%{_includedir}/%{name}/zeroD/ReactorSurface.h
%{_includedir}/%{name}/zeroD/Reservoir.h
%{_includedir}/%{name}/zeroD/WallFactory.h
%{_includedir}/%{name}/zeroD/Wall.h
%{_libdir}/pkgconfig/cantera.pc
%{_libdir}/libcantera.a
%{_libdir}/libcantera.so
%{_libdir}/libcantera.so.2
%{_libdir}/libcantera.so.%{version}
%{_libdir}/libcantera_fortran.a
%{_libdir}/libcantera_fortran.so
%{_libdir}/libcantera_fortran.so.2
%{_libdir}/libcantera_fortran.so.%{version}
%{_bindir}/setup_cantera
%{_bindir}/setup_cantera.csh


%changelog
* Sun Jan 02 2022 <fuller@fedoraproject.org>
- Bump dist to a4

* Thu Dec 23 2021 <fuller@fedoraproject.org>
- Bump dist to reflect many merged commits in a3 since October

* Tue Nov 30 2021 <fuller@fedoraproject.org>
- Introduced distro-specific IF to build on both Fedora and RHEL

* Thu Nov 18 2021 Mark E. Fuller <fuller@fedoraproject.org>
- Moved "setup_cantera*" to devel
- Make all included files explicit

* Thu Oct 14 2021 Mark E. Fuller <fuller@fedoraproject.org>
- first attempt versions of spec file and packaging
