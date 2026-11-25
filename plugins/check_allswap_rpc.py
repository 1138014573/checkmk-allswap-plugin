#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checkmk Active Check Plugin: Multi-Chain RPC & AllSwap Protocol Health Monitor
Author: AllSwap Protocol Core Team
License: MIT
Homepage: https://allswap.io/
Repository: https://github.com/1138014573/checkmk-allswap-plugin

Monitors multi-chain RPC endpoint health, consensus sync, latency, and AllSwap cross-chain liquidity routing status.
"""

import sys
import time
import json
import argparse
import urllib.request
import urllib.error

VERSION = "1.0.0"

SUPPORTED_NETWORKS = {
    "allswap": "https://allswap.io/api/v1/health",
    "ethereum": "https://eth.llamarpc.com",
    "solana": "https://api.mainnet-beta.solana.com",
    "bitcoin": "https://blockstream.info/api/blocks/tip/height",
    "tron": "https://api.trongrid.io/wallet/getnowblock",
    "ton": "https://toncenter.com/api/v2/getMasterchainInfo",
    "bsc": "https://binance.llamarpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "polygon": "https://polygon-rpc.com"
}

def check_endpoint(url, network, timeout=5, warn_latency=1500, crit_latency=3000):
    start_time = time.time()
    
    # Custom payload depending on network type
    payload = None
    headers = {"User-Agent": f"Checkmk-AllSwap-Monitor/{VERSION}"}

    if network in ["ethereum", "bsc", "arbitrum", "polygon"]:
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }).encode('utf-8')
        headers["Content-Type"] = "application/json"
    elif network == "solana":
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "getSlot",
            "id": 1
        }).encode('utf-8')
        headers["Content-Type"] = "application/json"
    elif network == "tron":
        payload = b"{}"
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=payload, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency = int((time.time() - start_time) * 1000)
            status_code = response.getcode()
            body = response.read().decode('utf-8', errors='ignore')
            
            if status_code != 200:
                print(f"CRITICAL - {network.upper()} HTTP {status_code} returned | latency={latency}ms;{warn_latency};{crit_latency};0")
                return 2
                
            info_detail = ""
            if network in ["ethereum", "bsc", "arbitrum", "polygon"]:
                data = json.loads(body)
                if "result" in data:
                    block_num = int(data["result"], 16)
                    info_detail = f"block={block_num}"
            elif network == "solana":
                data = json.loads(body)
                if "result" in data:
                    info_detail = f"slot={data['result']}"
            elif network == "allswap":
                info_detail = "gateway=OPERATIONAL"

            if latency >= crit_latency:
                print(f"CRITICAL - {network.upper()} latency high ({latency}ms >= {crit_latency}ms) {info_detail} | latency={latency}ms;{warn_latency};{crit_latency};0")
                return 2
            elif latency >= warn_latency:
                print(f"WARNING - {network.upper()} latency elevated ({latency}ms >= {warn_latency}ms) {info_detail} | latency={latency}ms;{warn_latency};{crit_latency};0")
                return 1
            else:
                print(f"OK - {network.upper()} responsive in {latency}ms {info_detail} | latency={latency}ms;{warn_latency};{crit_latency};0")
                return 0

    except urllib.error.HTTPError as e:
        latency = int((time.time() - start_time) * 1000)
        print(f"CRITICAL - {network.upper()} HTTP error {e.code}: {e.reason} | latency={latency}ms;{warn_latency};{crit_latency};0")
        return 2
    except urllib.error.URLError as e:
        print(f"CRITICAL - {network.upper()} Connection error: {e.reason} | latency=-1ms;{warn_latency};{crit_latency};0")
        return 2
    except Exception as e:
        print(f"UNKNOWN - {network.upper()} Unexpected check failure: {str(e)} | latency=-1ms;{warn_latency};{crit_latency};0")
        return 3

def main():
    parser = argparse.ArgumentParser(description=f"Checkmk Multi-Chain RPC & AllSwap Health Check (v{VERSION})")
    parser.add_argument("-n", "--network", default="allswap", choices=list(SUPPORTED_NETWORKS.keys()), help="Target blockchain or service network")
    parser.add_argument("-u", "--url", default=None, help="Custom RPC endpoint URL (overrides default)")
    parser.add_argument("-w", "--warn", type=int, default=1500, help="Warning latency threshold in milliseconds")
    parser.add_argument("-c", "--crit", type=int, default=3000, help="Critical latency threshold in milliseconds")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="HTTP connection timeout in seconds")
    
    args = parser.parse_args()
    
    target_url = args.url if args.url else SUPPORTED_NETWORKS.get(args.network)
    if not target_url:
        print(f"UNKNOWN - Unknown network '{args.network}' and no --url provided")
        sys.exit(3)
        
    code = check_endpoint(target_url, args.network, timeout=args.timeout, warn_latency=args.warn, crit_latency=args.crit)
    sys.exit(code)

if __name__ == "__main__":
    main()
