pub use ddx_common::types::primitives::exported::python::*;
use pyo3::prelude::*;

use crate::SubModule;

struct Module;

// functionality defined in ddx-common/src/types/primitives/numbers.rs
impl SubModule for Module {
    const NAME: &'static str = "decimal";
    fn init_submodule(py: Python, module: &PyModule) -> PyResult<()> {
        module.add_class::<Decimal>()?;
        // see https://github.com/PyO3/pyo3/issues/732
        module.add("DecimalError", py.get_type::<DecimalError>())?;
        Ok(())
    }

    fn finish_submodule(py: &Python, module: &PyModule) -> PyResult<()> {
        // this lets us import like `from ddx_python.decimal import Decimal`
        // https://github.com/PyO3/pyo3/issues/759
        py.import("sys")?
            .getattr("modules")?
            .set_item("ddx_python.decimal", module)?;
        Ok(())
    }
}

pub fn add_submodule(py: Python, parent_mod: &PyModule) -> PyResult<()> {
    Module::add_submodule(py, parent_mod)
}
