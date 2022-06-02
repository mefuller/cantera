classdef Mixture < handle

    properties
        mixID
        phases % Phases in the mixture
        T % Temperature
        P % Pressure
    end

    methods
        %% Mixture class constructor

        function m = Mixture(phases)
            % MIXTURE  Multiphase mixture class constructor.
            % m = Mixture(phases)
            % Class :mat:func:`Mixture` represents mixtures of one or more phases of matter.
            % To construct a mixture, supply a cell array of phases and
            % mole numbers::
            %
            %     >> gas = Solution('gas.yaml');
            %     >> graphite = Solution('graphite.yaml');
            %     >> mix = Mixture({gas, 1.0; graphite, 0.1});
            %
            % Phases may also be added later using the addPhase method::
            %
            %     >> water = Solution('water.yaml');
            %     >> mix.addPhase(water, 3.0);
            %
            % Note that the objects representing each phase compute only the
            % intensive state of the phase - they do not store any information
            % on the amount of this phase. Mixture objects, on the other hand,
            % represent the full extensive state.
            %
            % Mixture objects are 'lightweight' in the sense that they do not
            % store parameters needed to compute thermodynamic or kinetic
            % properties of the phases. These are contained in the
            % ('heavyweight') phase objects. Multiple mixture objects may be
            % constructed using the same set of phase objects. Each one stores
            % its own state information locally, and synchronizes the phase
            % objects whenever it requires phase properties.
            %
            % :param phases:
            %     Cell array of phases and mole numbers
            % :return:
            %     Instance of class :mat:func:`Mixture`
            %

            checklib;

            if nargin > 1
                error('Mixture: wrong number of arguments');
            end

            % Create an empty mixture.
            m.mixID = calllib(ct, 'mix_new');
            m.phases = phases;

            % If phases are supplied, add them
            if nargin == 1
                if ~isa(phases, 'cell')
                    error('Enter phases as a cell array.');
                end

                % First column contains the phase objects, and the second
                % column contains the mole numbers of each phase.
                [np, nc] = size(phases);
                if nc ~= 2
                    error('Cell array of phases should have each phase on a new row');
                end
                for n = 1:np
                    m.addPhase(phases{n, 1}, phases{n, 2});
                end
                m.T = phases{n, 1}.T;
                m.P = phases{n, 1}.P;
            end
        end

        %% Utility methods

        function display(m)
            % DISPLAY  Display the state of the mixture on the terminal.
            % m.display
            % :param self:
            %     Instance of class :mat:func:`Mixture`
            %
            calllib(ct, 'mix_updatePhases', m.mixID);
            [np, nc] = size(m.phases);
            for n = 1:np
                s = [sprintf('\n*******************    Phase %d', n) ...
                    sprintf('    ******************************\n\n Moles: %12.6g', ...
                            phaseMoles(m, n))];
                disp(s);
                display(m.phases{n, 1});
            end
        end

        function clear(m)
            % CLEAR  Delete the C++ MultiPhase object.
            % m.clear
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            %
            calllib(ct, 'mix_del', m.mixID);
        end

        function addPhase(m, phase, moles)
            % ADDPHASE  Add a phase to a mixture.
            % addPhase(self, phase, moles)
            % :param self:
            %     Instance of class :mat:func:`Mixture` to which phases should be
            %     added
            % :param phase:
            %     Instance of class :mat:func:`ThermoPhase` which should be added
            % :param moles:
            %     Number of moles of the ``phase`` to be added to this mixture.
            %     Units: kmol
            %
            if ~isa(phase, 'ThermoPhase')
                error('Phase object of wrong type.');
            end
            if ~isa(moles, 'numeric')
                error('Number of moles must be numeric');
            end
            if moles < 0.0
                error('Negative moles');
            end

            iok = calllib(ct, 'mix_addPhase', m.mixID, phase.tp_id, ...
                          moles);
            if iok < 0
                error('Error adding phase');
            end
        end

        %% Mixture Get methods

        function temperature = get.T(m)
            % GET.T  Get the temperature of a mixture.
            % temperature = m.T
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :return:
            %     Temperature (K)
            %
            temperature = calllib(ct, 'mix_temperature', m.mixID);
        end

        function pressure = get.P(m)
            % GET.P  Get the pressure of the mixture.
            % pressure = m.P
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :return:
            %     Pressure. Units: Pa
            %
            pressure = calllib(ct, 'mix_pressure', m.mixID);
        end

        function n = nAtoms(m, e)
            % NATOMS  Get the number of atoms of an element in a mixture.
            % n = m.nAtoms(e)
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param e:
            %     Index of element
            % :return:
            %     Number of atoms for element e
            %
            % Note: In keeping with the conventions used by Matlab, the
            % indices start from 1 instead of 0 as in Cantera C++ and
            % Python interfaces.
            %
            n = calllib(ct, 'mix_nPhases', m.mixID, k-1, e-1);
            % Check back on this one!
        end

        function n = nElements(m)
            % NELEMENTS  Get the number of elements in a mixture.
            % n = m.nElements
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :return:
            %     Number of elements in the input
            %
            n = calllib(ct, 'mix_nElements', m.mixID);
        end

        function n = nPhases(m)
            % NPHASES  Get the number of phases in a mixture.
            % n = m.nPhases
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :return:
            %     Number of phases in the input
            %
            n = calllib(ct, 'mix_nPhases', m.mixID);
        end

        function n = nSpecies(m)
            % NSPECIES  Get the number of species in a mixture.
            % n = m.nSpecies
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :return:
            %     Number of species in the input
            %
            n = calllib(ct, 'mix_nSpecies', m.mixID);
        end

        function n = elementIndex(m, name)
            % ELEMENTINDEX  Get the index of an element.
            % n = m.elementIndex(name)
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param name:
            %     Name of the element whose index is desired
            % :return:
            %     Index of element with name ``name``
            %
            % Note: In keeping with the conventions used by Matlab, the
            % indices start from 1 instead of 0 as in Cantera C++ and
            % Python interfaces.
            %
            n = calllib(ct, 'mix_elementIndex', m.mixID, name) + 1;
        end

        function n = speciesIndex(m, k, p)
            % SPECIESINDEX  Get the index of a species in a mixture.
            % n = m.speciesIndex(k, p)
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param name:
            %     Name of the speces whose index is desired
            % :return:
            %     Index of species with name ``name``
            %
            % Note: In keeping with the conventions used by Matlab, the
            % indices start from 1 instead of 0 as in Cantera C++ and
            % Python interfaces.
            %
            n = calllib(ct, 'mix_speciesIndex', m.mixID, k-1, p-1) + 1;
        end

        function moles = elementMoles(m, e)
            % ELEMENTMOLES  Get the number of moles of an element in a mixture.
            % moles = m.elementMoles(e)
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param e:
            %    Integer element number.
            % :return:
            %    Moles of element number 'e'. If input 'e' is empty, return
            %    moles of every element in the mixture. Unit: kmol.
            %
            if nargin == 2
                moles = calllib(ct, 'mix_elementMoles', m.mixID, e)
            elseif nargin == 1
                nel = m.nElements;
                moles = zeros(1, nel);
                for i = 1:nel
                    moles(i) = calllib(ct, 'mix_elementMoles', m.mixID, i);
                end
            else error('wrong number of arguments');
            end
        end

        function moles = phaseMoles(m, n)
            % PHASEMOLES  Get the number of moles of a phase in a mixture.
            % moles = m.phaseMoles(n)
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param n:
            %    Integer phase number.
            % :return:
            %    Moles of phase number 'n'. If input 'n' is empty, return
            %    moles of every phase in the mixture. Unit: kmol.
            %
            if nargin == 2
                moles = calllib(ct, 'mix_phaseMoles', m.mixID, n);
            elseif nargin == 1
                np = m.nPhases;
                moles = zeros(1, np);
                for i = 1:np
                    moles(i) = calllib(ct, 'mix_phaseMoles', ...
                                       m.mixID, i);
                end
            else error('wrong number of arguments');
            end
        end

        function moles = speciesMoles(m, k)
            % SPECIESMOLES  Get the number of moles of a species in a mixture.
            % moles = m.speciesMoles(n)
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param k:
            %    Integer species number.
            % :return:
            %    Moles of species number 'k'. If input 'k' is empty, return
            %    moles of every species in the mixture. Unit: kmol.

            if nargin == 2
                moles = calllib(ct, 'mix_speciesMoles', m.mixID, k);
            elseif nargin == 1
                nsp = m.nSpecies;
                moles = zeros(1, nsp);
                for i = 1:nsp
                    moles(i) = calllib(ct, 'mix_speciesMoles', ...
                                       m.mixID, i);
                end
            else error('wrong number of arguments');
            end
        end

        function mu = chemPotentials(m)
            % CHEMPOTENTIALS  Get the chemical potentials of species in a mixture.
            % mu = m.chemPotentials
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :return:
            %     Vector of chemical potentials. Units: J/kmol
            %
            nsp = m.nSpecies;
            xx = zeros(1, nsp);
            ptr = libpointer('doublePtr', xx);
            calllib(ct, 'mix_getChemPotential', m.mixID, nsp, ptr);
            mu = ptr.Value;
        end

        %% Mixture Set methods

        function m = set.T(m, temp)
            % SET.T  Set the mixture temperature.
            % m.T = temp
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param temp:
            %     Temperature. Units: K
            %
            calllib(ct, 'mix_setTemperature', m.mixID, temp);
        end

        function m = set.P(m, pressure)
            % SET.P  Set the pressure of the mixture.
            % m.P = pressure
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param pressure:
            %     Pressure. Units: Pa
            %
            calllib(ct, 'mix_setPressure', m.mixID, pressure);
        end

        function setPhaseMoles(m, n, moles)
            % SETPHASEMOLES  Set the number of moles of a phase in a mixture.
            % m.setPhaseMoles(n, moles)
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param n:
            %     Phase number in the input
            % :param moles:
            %     Number of moles to add. Units: kmol
            %
            calllib(ct, 'mix_setPhaseMoles', m.mixID, n-1, moles);
        end

        function setSpeciesMoles(m, moles)
            % SETSPECIESMOLES  Set the moles of the species.
            % m.setSpeciesMoles(moles)
            % Set the moles of the species in kmol. The moles may
            % be specified either as a string, or as an vector. If a vector is
            % used, it must be dimensioned at least as large as the total number
            % of species in the mixture. Note that the species may belong to any
            % phase, and unspecified species are set to zero. ::
            %
            %     >> mix.setSpeciesMoles('C(s):1.0, CH4:2.0, O2:0.2');
            %
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param moles:
            %     Vector or string specifying the moles of species
            %
            if isa(moles, 'double')
                l = length(moles);
                calllib(ct, 'mix_setMoles', m.mixID, l, moles);
            elseif isa(moles, 'string')
                calllib(ct, 'mix_setMolesByName', m.mixID, moles);
            else
                error('The input must be a vector or string!');
            end
        end

        function r = equilibrate(m, XY, err, maxsteps, maxiter, loglevel)
            % EQUILIBRATE  Set the mixture to a state of chemical equilibrium.
            % m.equilibrate(XY, err, maxsteps, maxiter, loglevel)
            % This method uses a version of the VCS algorithm to find the
            % composition that minimizes the total Gibbs free energy of the
            % mixture, subject to element conservation constraints. For a
            % description of the theory, see Smith and Missen, "Chemical
            % Reaction Equilibrium."  The VCS algorithm is implemented in
            % Cantera kernel class MultiPhaseEquil.
            %
            % The VCS algorithm solves for the equilibrium composition for
            % specified temperature and pressure. If any other property pair
            % other than "TP" is specified, then an outer iteration loop is
            % used to adjust T and/or P so that the specified property
            % values are obtained. ::
            %
            %     >> mix.equilibrate('TP')
            %     >> mix.equilibrate('TP', 1.0e-6, 500)
            %
            % :param m:
            %     Instance of class :mat:func:`Mixture`
            % :param XY:
            %     Two-letter string specifying the two properties to hold
            %     fixed.  Currently, ``'TP'``, ``'HP'``, ``'TV'``, and ``'SP'`` are
            %     implemented. Default: ``'TP'``.
            % :param err:
            %     Error tolerance. Iteration will continue until :math:`\Delta\mu)/RT`
            %     is less than this value for each reaction. Default:
            %     1.0e-9. Note that this default is very conservative, and good
            %     equilibrium solutions may be obtained with larger error
            %     tolerances.
            % :param maxsteps:
            %     Maximum number of steps to take while solving the
            %     equilibrium problem for specified T and P. Default: 1000.
            % :param maxiter:
            %     Maximum number of temperature and/or pressure
            %     iterations.  This is only relevant if a property pair other
            %     than (T,P) is specified. Default: 200.
            % :param loglevel:
            %     Set to a value > 0 to write diagnostic output.
            %     Larger values generate more detailed information.
            % :return:
            %     The error in the solution
            %
            if nargin < 6
                loglevel = 0;
            end
            if nargin < 5
                maxiter = 200;
            end
            if nargin < 4
                maxsteps = 1000;
            end
            if nargin < 3
                err = 1.0e-9;
            end
            if nargin < 2
                XY = 'TP'
            end
            r = calllib(ct, 'mix_equilibrate', m.mixID, XY, err, ...
                        maxsteps, maxiter, loglevel);
        end

    end
end
