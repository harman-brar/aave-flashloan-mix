
from brownie import FlashloanV2, accounts, config, network, interface

MINIMUM_FLASHLOAN_WMATIC_BALANCE = 5 * 1e18
POLYGONSCAN_TX_URL = "https://mumbai.etherscan.com/tx/{}"


def main():
    """
    Executes the funcitonality of the flash loan.
    """
    acct = accounts.add(config["wallets"]["from_key"])
    print("Getting Flashloan contract...")
    flashloan = FlashloanV2[len(FlashloanV2) - 1]
    wmatic = interface.WmaticInterface(config["networks"][network.show_active()]["wmatic"])
    # We need to fund it if it doesn't have any token to fund!
    if wmatic.balanceOf(flashloan) < MINIMUM_FLASHLOAN_WMATIC_BALANCE:
        print("Funding Flashloan contract with WMATIC...")
        wmatic.transfer(flashloan, "100000000000000", {"from": acct})
    print("Executing Flashloan...")
    tx = flashloan.flashloan(wmatic, {"from": acct})
    print("You did it! View your tx here: " + POLYGONSCAN_TX_URL.format(tx.txid))
    return flashloan
