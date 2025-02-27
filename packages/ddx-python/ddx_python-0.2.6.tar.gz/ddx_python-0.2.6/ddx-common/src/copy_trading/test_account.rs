use super::auth::SubaccountAuth;
use anyhow::Result;

/// Populate subaccounts from key pairs stored in the data directory.
///
/// Using string for the PEM contents for consistency with Binance API.
pub fn read_binance_subaccounts() -> Result<Vec<SubaccountAuth>> {
    // NOTE: Path determined by convention, configured in docker image and must not be made configurable.

    use ddx_common::copy_trading::auth::SubaccountAuth;
    let mut testnet_dir = super::certs_dir();
    testnet_dir.push("copytrading");
    testnet_dir.push("testnet");
    testnet_dir.push("binance");
    assert!(
        testnet_dir.exists(),
        "Data dir {:?} containing testnet accounts must exist; use the docker image as intended or configure accordingly",
        testnet_dir,
    );
    let mut data = Vec::new();
    for entry in std::fs::read_dir(testnet_dir)? {
        let entry = entry?;
        let path = entry.path();
        if path.is_file() {
            if let Some(filename) = path.file_name().and_then(|s| s.to_str()) {
                if filename.starts_with("binance_") && filename.ends_with("_private.pem") {
                    let api_key = filename
                        .trim_start_matches("binance_")
                        .trim_end_matches("_private.pem")
                        .to_string();
                    // Load the private key from the PEM file.
                    let secret_key_pem = std::fs::read_to_string(&path)?;
                    data.push(SubaccountAuth::binance(
                        api_key,
                        secret_key_pem,
                        "EXAMPLE".to_string(),
                    ));
                }
            }
        }
    }
    Ok(data)
}
