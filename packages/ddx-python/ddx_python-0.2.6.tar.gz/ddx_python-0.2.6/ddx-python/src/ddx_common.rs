#[cfg(feature = "index_fund")]
use ddx_common::specs::index_fund::IndexFundPerpetual;
#[cfg(feature = "fixed_expiry_future")]
use ddx_common::specs::quarterly_expiry_future::{Quarter, QuarterlyExpiryFuture};
use ddx_common::{
    global::ApplicationContext,
    specs::{
        SingleNamePerpetual,
        types::{SpecsKey, SpecsKind},
    },
    types::{
        accounting::{Balance, Position, PositionSide, Price, PriceDirection, Strategy, TradeSide},
        identifiers::{
            BookOrderKey, EpochMetadataKey, InsuranceFundKey, PositionKey, PriceKey, StatsKey,
            StrategyKey,
        },
        primitives::{OrderSide, StampedTimeValue, TokenSymbol},
        request::{
            AdvanceEpoch, AdvanceSettlementEpoch, Block, CancelAllIntent, CancelOrderIntent,
            IndexPrice, InsuranceFundWithdrawIntent, MintPriceCheckpoint, ModifyOrderIntent,
            OrderIntent, ProfileUpdate, UpdateProductListings, WithdrawDDXIntent, WithdrawIntent,
        },
        state::{
            BookOrder, EpochMetadata, InsuranceFundContribution, Stats, TradableProduct,
            TradableProductKey, Trader, exported::python::*,
        },
        transaction::{InsuranceFundUpdateKind, StrategyUpdateKind, TraderUpdateKind},
    },
};
use pyo3::prelude::*;

use crate::SubModule;

pub(super) struct Module;

// functionality defined in ddx-common/src/types/state/exported.rs
impl SubModule for Module {
    const NAME: &'static str = "common";
    fn init_submodule(py: Python, module: &PyModule) -> PyResult<()> {
        let requests_submod = PyModule::new(py, "requests")?;
        requests_submod.add_class::<AdvanceEpoch>()?;
        requests_submod.add_class::<StampedTimeValue>()?;
        requests_submod.add_class::<AdvanceSettlementEpoch>()?;
        requests_submod.add_class::<Block>()?;
        requests_submod.add_class::<IndexPrice>()?;
        requests_submod.add_class::<MintPriceCheckpoint>()?;
        requests_submod.add_class::<UpdateProductListings>()?;
        requests_submod.add_class::<SettlementAction>()?;

        let intents_submod = PyModule::new(py, "intents")?;
        intents_submod.add_class::<OrderIntent>()?;
        intents_submod.add_class::<ModifyOrderIntent>()?;
        intents_submod.add_class::<CancelOrderIntent>()?;
        intents_submod.add_class::<CancelAllIntent>()?;
        intents_submod.add_class::<ProfileUpdate>()?;
        intents_submod.add_class::<WithdrawIntent>()?;
        intents_submod.add_class::<WithdrawDDXIntent>()?;
        intents_submod.add_class::<InsuranceFundWithdrawIntent>()?;
        requests_submod.add_submodule(intents_submod)?;

        module.add_submodule(requests_submod)?;

        let enums_submod = PyModule::new(py, "enums")?;
        enums_submod.add_class::<OrderSide>()?;
        enums_submod.add_class::<OrderType>()?;
        enums_submod.add_class::<PositionSide>()?;
        enums_submod.add_class::<TradeSide>()?;
        enums_submod.add_class::<PriceDirection>()?;
        module.add_submodule(enums_submod)?;

        let state_submod = PyModule::new(py, "state")?;
        state_submod.add_class::<ItemKind>()?;
        state_submod.add_class::<Item>()?;
        state_submod.add_class::<TradableProductParameters>()?;
        state_submod.add_class::<DerivadexSMT>()?;
        state_submod.add_class::<MerkleProof>()?;
        state_submod.add_class::<Balance>()?;

        state_submod.add_class::<Trader>()?;
        state_submod.add_class::<Strategy>()?;
        state_submod.add_class::<Position>()?;
        state_submod.add_class::<BookOrder>()?;
        state_submod.add_class::<Price>()?;
        state_submod.add_class::<InsuranceFund>()?;
        state_submod.add_class::<Stats>()?;
        state_submod.add_class::<Signer>()?;
        state_submod.add_class::<Specs>()?;
        state_submod.add_class::<TradableProduct>()?;
        state_submod.add_class::<InsuranceFundContribution>()?;
        state_submod.add_class::<EpochMetadata>()?;

        let keys_submod = PyModule::new(py, "keys")?;
        keys_submod.add_class::<TraderKey>()?;
        keys_submod.add_class::<StrategyKey>()?;
        keys_submod.add_class::<PositionKey>()?;
        keys_submod.add_class::<BookOrderKey>()?;
        keys_submod.add_class::<PriceKey>()?;
        keys_submod.add_class::<InsuranceFundKey>()?;
        keys_submod.add_class::<StatsKey>()?;
        keys_submod.add_class::<SignerKey>()?;
        keys_submod.add_class::<SpecsKey>()?;
        keys_submod.add_class::<TradableProductKey>()?;
        keys_submod.add_class::<InsuranceFundContributionKey>()?;
        keys_submod.add_class::<EpochMetadataKey>()?;
        state_submod.add_submodule(keys_submod)?;

        module.add_submodule(state_submod)?;

        let transaction_submod = PyModule::new(py, "transactions")?;
        transaction_submod.add_class::<StrategyUpdateKind>()?;
        transaction_submod.add_class::<InsuranceFundUpdateKind>()?;
        transaction_submod.add_class::<TraderUpdateKind>()?;
        module.add_submodule(transaction_submod)?;

        let specs_submod = PyModule::new(py, "specs")?;
        specs_submod.add_class::<SpecsKind>()?;
        specs_submod.add_class::<ProductSpecs>()?;
        specs_submod.add_class::<SingleNamePerpetual>()?;
        #[cfg(feature = "index_fund")]
        specs_submod.add_class::<IndexFundPerpetual>()?;
        #[cfg(feature = "fixed_expiry_future")]
        {
            specs_submod.add_class::<QuarterlyExpiryFuture>()?;
            specs_submod.add_class::<Quarter>()?;
        }
        module.add_submodule(specs_submod)?;

        let accounting_submod = PyModule::new(py, "accounting")?;
        accounting_submod.add_class::<MarkPriceMetadata>()?;
        module.add_submodule(accounting_submod)?;

        module.add_function(wrap_pyfunction!(get_operator_context, module)?)?;
        module.add_class::<ProductSymbol>()?;
        module.add_class::<TokenSymbol>()?;
        module.add_class::<ApplicationContext>()?;
        module.add("DdxCommonError", py.get_type::<DdxCommonError>())?;
        Ok(())
    }

    fn finish_submodule(py: &Python, module: &PyModule) -> PyResult<()> {
        // this lets us import like `from ddx_python.decimal import Decimal`
        // https://github.com/PyO3/pyo3/issues/759
        let modules = py.import("sys")?.getattr("modules")?;
        modules.set_item("ddx_python.common", module)?;
        modules.set_item(
            "ddx_python.common.requests",
            module.getattr("requests").unwrap(),
        )?;
        modules.set_item(
            "ddx_python.common.requests.intents",
            module
                .getattr("requests")
                .unwrap()
                .getattr("intents")
                .unwrap(),
        )?;
        modules.set_item("ddx_python.common.enums", module.getattr("enums").unwrap())?;
        modules.set_item("ddx_python.common.state", module.getattr("state").unwrap())?;
        modules.set_item(
            "ddx_python.common.state.keys",
            module.getattr("state").unwrap().getattr("keys").unwrap(),
        )?;
        modules.set_item(
            "ddx_python.common.transactions",
            module.getattr("transactions").unwrap(),
        )?;
        modules.set_item("ddx_python.common.specs", module.getattr("specs").unwrap())?;
        modules.set_item(
            "ddx_python.common.accounting",
            module.getattr("accounting").unwrap(),
        )?;
        Ok(())
    }
}

pub fn add_submodule(py: Python, parent_mod: &PyModule) -> PyResult<()> {
    Module::add_submodule(py, parent_mod)
}
