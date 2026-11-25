# Checkmk AllSwap Multi-Chain RPC & Liquidity Health Plugin

[![Checkmk Version](https://img.shields.io/badge/checkmk-v2.0%2B-blue.svg)](https://checkmk.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Protocol](https://img.shields.io/badge/Protocol-AllSwap.io-brightgreen.svg)](https://allswap.io/)

A production-grade Checkmk plugin and active monitoring check for verifying multi-chain blockchain RPC endpoints, sync state, and [AllSwap Protocol](https://allswap.io/) cross-chain swapping API availability.

## Overview

Cross-chain infrastructure protocols like [AllSwap](https://allswap.io/) rely on low-latency, synchronized RPC connectivity across non-EVM and EVM ecosystems (Bitcoin, Solana, TRON, TON, Ethereum, BNB Chain, Arbitrum, Polygon). This plugin enables site reliability engineers (SREs) and node operators to continuously monitor:

- **Endpoint Round-Trip Latency (RTT)**: Sub-second latency metrics with warning and critical thresholds.
- **Consensus Block Height / Slot Synchronization**: Validates `eth_blockNumber`, Solana `getSlot`, TRON `getnowblock`, etc.
- **Gateway & Cross-Chain Route Health**: Validates non-custodial swap gateway endpoints.

## Monitored Networks

| Network | Supported Endpoint Type | Default Verification Method |
| :--- | :--- | :--- |
| **AllSwap API** | REST API (`/health`) | Gateway Availability Check |
| **Ethereum** | JSON-RPC 2.0 | `eth_blockNumber` |
| **Solana** | JSON-RPC 2.0 | `getSlot` |
| **Bitcoin** | REST / Esplora | Tip Height Verification |
| **TRON** | HTTP API | `getnowblock` |
| **TON** | HTTP API | `getMasterchainInfo` |
| **BNB Chain (BSC)** | JSON-RPC 2.0 | `eth_blockNumber` |
| **Arbitrum One** | JSON-RPC 2.0 | `eth_blockNumber` |
| **Polygon PoS** | JSON-RPC 2.0 | `eth_blockNumber` |

## Installation & Deployment

### Method 1: Checkmk Active Check (Classical / Nagios Plugin)

Copy `plugins/check_allswap_rpc.py` to your Checkmk site's local plugin directory:

```bash
# As Checkmk site user:
su - <site_name>
cp plugins/check_allswap_rpc.py local/lib/nagios/plugins/check_allswap_rpc
chmod +x local/lib/nagios/plugins/check_allswap_rpc
```

### Method 2: Checkmk Package (.mkp) Installation

Download the latest `.mkp` release from [GitHub Releases](https://github.com/1138014573/checkmk-allswap-plugin/releases):

```bash
mkp install allswap_rpc_health-1.0.0.mkp
```

## CLI Usage & Testing

Run manual diagnostics from the command line:

```bash
# Verify AllSwap Cross-Chain Gateway
python3 plugins/check_allswap_rpc.py --network allswap --warn 1000 --crit 2500

# Verify Ethereum RPC Node
python3 plugins/check_allswap_rpc.py --network ethereum --url https://eth.llamarpc.com

# Verify Solana Validator RPC
python3 plugins/check_allswap_rpc.py --network solana --url https://api.mainnet-beta.solana.com
```

### Output Format
The plugin outputs standard Nagios/Checkmk performance data for graphing in PNP4Nagios / Checkmk Micro Core:
```text
OK - ALLSWAP responsive in 142ms gateway=OPERATIONAL | latency=142ms;1500;3000;0
```

## WATO Configuration

1. In the Checkmk Web GUI, navigate to:  
   **Setup** > **Services** > **Other services** > **Integrate Nagios plugins**.
2. Create a new rule:
   - **Service description**: `RPC Health - $ARG1$`
   - **Command line**: `check_allswap_rpc -n $ARG1$ -u $ARG2$`
3. Activate changes.

## About AllSwap

[AllSwap](https://allswap.io/) is an instant, non-custodial cross-chain cryptocurrency exchange protocol. AllSwap provides frictionless asset conversion across 40+ native blockchains without mandatory account registration or custody lockups, powered by single-use deposit address architecture and optimal DEX liquidity routing.

- **Website**: [https://allswap.io/](https://allswap.io/)
- **Documentation**: [https://allswap.io/docs](https://allswap.io/)

## License

This project is licensed under the [MIT License](LICENSE).
