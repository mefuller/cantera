/**
 * @file MultiRate.h
 *
 * @warning This file is an experimental part of the %Cantera API and
 *     may be changed or removed without notice.
 */

// This file is part of Cantera. See License.txt in the top-level directory or
// at https://cantera.org/license.txt for license and copyright information.

#ifndef CT_MULTIRATE_H
#define CT_MULTIRATE_H

#include "cantera/kinetics/ReactionRate.h"

namespace Cantera
{

//! An abstract base class for evaluating all reactions of a particular type.
/**
 * Because this class has no template parameters, the `Kinetics` object
 * can store all of these rate coefficient evaluators as a
 * `vector<shared_ptr<MultiRateBase>>`.
 *
 * @todo At the moment, implemented methods are specific to `BulkKinetics`,
 *     which can be updated using information of a single `ThermoPhase`.
 *     `InterfaceKinetics` will require access to an entire `Kinetics` object
 *     or the underlying `vector<ThermoPhase*>` vector (e.g. `m_thermo`).
 *
 * @warning This class is an experimental part of the %Cantera API and
 *     may be changed or removed without notice.
 */
class MultiRateBase
{
public:
    virtual ~MultiRateBase() {}

    //! Add reaction rate object to the evaluator
    virtual void add(const size_t rxn_index,
                     const shared_ptr<ReactionRateBase> rate) = 0;

    //! Replace reaction rate object handled by the evaluator
    virtual bool replace(const size_t rxn_index,
                         const shared_ptr<ReactionRateBase> rate) = 0;

    //! Evaluate all rate constants handled by the evaluator
    virtual void getRateConstants(const ThermoPhase& bulk_phase,
                                  double* kf) const = 0;

    //! Update data common to reaction rates of a specific type
    virtual void update(const ThermoPhase& bulk) = 0;
};


//! A class template handling all reaction rates specific to `BulkKinetics`.
/**
 * @warning This class is an experimental part of the %Cantera API and
 *     may be changed or removed without notice.
 */
template <class RateType, class DataType>
class MultiBulkRates final : public MultiRateBase
{
public:
    virtual void add(const size_t rxn_index,
                     const shared_ptr<ReactionRateBase> rate) override {
        m_indices[rxn_index] = m_rates.size();
        m_rates.push_back(*std::dynamic_pointer_cast<RateType>(rate));
        m_rxn.push_back(rxn_index);
    }

    virtual bool replace(const size_t rxn_index,
                         const shared_ptr<ReactionRateBase> rate) override {
        if (rate->type() != RateType::staticType()) {
            throw CanteraError("MultiBulkRate::replace",
                 "Invalid operation: cannot replace rate object of type '{}' "
                 "with a new rate of type '{}'.", RateType::staticType(), rate->type());
        }
        if (m_indices.find(rxn_index) != m_indices.end()) {
            size_t j = m_indices[rxn_index];
            m_rates[j] = *std::dynamic_pointer_cast<RateType>(rate);
            return true;
        }
        return false;
    }

    virtual void getRateConstants(const ThermoPhase& bulk,
                                  double* kf) const override {
        for (size_t i = 0; i < m_rates.size(); i++) {
            kf[m_rxn[i]] = m_rates[i].eval(m_shared);
        }
    }

    virtual void update(const ThermoPhase& bulk) override {
        // update common data once for each reaction type
        m_shared.update(bulk);
        if (RateType::uses_update()) {
            // update reaction-specific data for each reaction. This loop
            // is efficient as all function calls are de-virtualized, and
            // all of the rate objects are contiguous in memory
            for (auto& rate : m_rates) {
                rate.update(m_shared, bulk);
            }
        }
    }

protected:
    std::vector<RateType> m_rates; //! Reaction rate objects
    std::vector<size_t> m_rxn; //! Index within overall rate vector
    std::map<size_t, size_t> m_indices; //! Mapping of indices
    DataType m_shared;
};

}

#endif