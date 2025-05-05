import argparse
import json
import os


# define blockchains:
ABSTRACT = 2741
APECHAIN = 33139
ARBITRUM_ONE = 42161
ARBITRUM_NOVA = 42170
AVALANCHE = 43114
B3 = 8333
BERACHAIN = 80094
BLAST = 81457
BNB_MAINNET = 56
BOB = 60808
BOBA = 288
CELO = 42220
CORN = 21000000
DEGEN = 666666666
ETHEREUM_MAINNET = 1
FANTOM_OPERA = 250
FLARE = 14
GNOSIS = 100
INK = 57073
KAIA = 8217
LENS = 232
LINEA = 50144
MANTLE = 5000
NEAR = 397
OP_BNB = 204
OP_MAINNET = 10
PLUME_MAINNET = 98866
POLYGON_MAINNET = 137
POLYGON_ZKEVM = 1101
RONIN = 2020
SCROLL = 534352
SEI = 1329
SHAPE = 360
SONIC = 146
SOPHON = 50104
TRON = 728126428
UNICHAIN = 130
VICTION = 88
WORLDCHAIN = 480
ZKSYNC = 324
ZORA = 7777777

X_LAYER = 196
AURORA = 1313161554

# blockchains that are supported by safe wallet
safe_wallet_supported_blockchains = set(
    [
        AURORA,
        ETHEREUM_MAINNET,
        GNOSIS,
        POLYGON_MAINNET,
        POLYGON_ZKEVM,
        BNB_MAINNET,
        ARBITRUM_ONE,
        OP_MAINNET,
        BERACHAIN,
        INK,
        LINEA,
        SONIC,
        UNICHAIN,
        SCROLL,
        CELO,
        AVALANCHE,
        BLAST,
        MANTLE,
        WORLDCHAIN,
        X_LAYER,
    ]
)

# blockchains that are supported by dune
dune_supported_blockchains = set(
    [
        ABSTRACT,
        APECHAIN,
        ARBITRUM_ONE,
        ARBITRUM_NOVA,
        AVALANCHE,
        B3,
        BERACHAIN,
        BLAST,
        BNB_MAINNET,
        BOB,
        BOBA,
        CELO,
        CORN,
        DEGEN,
        ETHEREUM_MAINNET,
        FANTOM_OPERA,
        FLARE,
        GNOSIS,
        INK,
        KAIA,
        LENS,
        LINEA,
        MANTLE,
        NEAR,
        OP_BNB,
        OP_MAINNET,
        PLUME_MAINNET,
        POLYGON_MAINNET,
        POLYGON_ZKEVM,
        RONIN,
        SCROLL,
        SEI,
        SHAPE,
        SONIC,
        SOPHON,
        TRON,
        UNICHAIN,
        VICTION,
        WORLDCHAIN,
        ZKSYNC,
        ZORA,
    ]
)

# sanity check that ethereum mainnet is in the set
assert 1 in dune_supported_blockchains

# define the mapping
bc_mapping = {
    ABSTRACT: "ABSTRACT",
    APECHAIN: "APECHAIN",
    ARBITRUM_ONE: "ARBITRUM_ONE",
    ARBITRUM_NOVA: "ARBITRUM_NOVA",
    AVALANCHE: "AVALANCHE",
    B3: "B3",
    BERACHAIN: "BERACHAIN",
    BLAST: "BLAST",
    BNB_MAINNET: "BNB_MAINNET",
    BOB: "BOB",
    BOBA: "BOBA",
    CELO: "CELO",
    CORN: "CORN",
    DEGEN: "DEGEN",
    ETHEREUM_MAINNET: "ETHEREUM_MAINNET",
    FANTOM_OPERA: "FANTOM_OPERA",
    FLARE: "FLARE",
    GNOSIS: "GNOSIS",
    INK: "INK",
    KAIA: "KAIA",
    LENS: "LENS",
    LINEA: "LINEA",
    MANTLE: "MANTLE",
    NEAR: "NEAR",
    OP_BNB: "OP_BNB",
    OP_MAINNET: "OP_MAINNET",
    PLUME_MAINNET: "PLUME_MAINNET",
    POLYGON_MAINNET: "POLYGON_MAINNET",
    POLYGON_ZKEVM: "POLYGON_ZKEVM",
    RONIN: "RONIN",
    SCROLL: "SCROLL",
    SEI: "SEI",
    SHAPE: "SHAPE",
    SONIC: "SONIC",
    SOPHON: "SOPHON",
    TRON: "TRON",
    UNICHAIN: "UNICHAIN",
    VICTION: "VICTION",
    WORLDCHAIN: "WORLDCHAIN",
    ZKSYNC: "ZKSYNC",
    ZORA: "ZORA",
}


def load_deployed_chains(fname: str, deployment: str):
    # check if deoloyment is valid
    if deployment not in ["canonical", "eip155", "zksync"]:
        return set()

    # set path of the file
    path = os.path.join(os.path.dirname(__file__), fname)

    # check if the file exists
    if not os.path.exists(path):
        return set()

    # load the file
    with open(path, "r") as f:
        data = json.load(f)

    # iterate over networks
    networks = data["networkAddresses"]
    valid_networks = set()

    for k, v in networks.items():
        # try to convert the key to an int
        k = int(k)

        if k not in dune_supported_blockchains:
            continue

        if k not in safe_wallet_supported_blockchains:
            continue

        if type(v) is str:
            if v == deployment:
                valid_networks.add(k)
        elif type(v) is list:
            for n in v:
                if n == deployment:
                    valid_networks.add(k)

    # we want names not chain ids
    valid_networks = {bc_mapping[k] for k in valid_networks}

    # lets sort this
    valid_networks = sorted(valid_networks)

    # get contract address
    deployments = data["deployments"]
    if deployment not in deployments:
        raise KeyError(f"Deployment {deployment} not found in {fname}")

    contract_address = deployments[deployment]["address"]
    return contract_address, valid_networks


def print_supported_blockchains(fname: str, deployments: list):
    for deployment in deployments:
        print(f"Loading file: {fname} as deployment: {deployment}")  # canonical

        address, networks = load_deployed_chains(fname, deployment)
        print(f"Contract address: {address}")
        print()
        print("We need the following chains in Dune:")
        for network in networks:
            print(f"{network}")
        print()


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--fname", type=str, help="File name to load")
    cli.add_argument("--deployments", nargs="*", type=str, help="Deployments to load")
    args = cli.parse_args()
    print_supported_blockchains(args.fname, args.deployments)


if __name__ == "__main__":
    main()
