import tarfile
import os
import io

info_dict = {
    'title': 'AllSwap Multi-Chain RPC & API Health Monitor',
    'name': 'allswap_rpc_health',
    'version': '1.0.0',
    'version.min_required': '2.0.0',
    'version.packaged': '2.2.0p1',
    'author': 'AllSwap Protocol Core Team',
    'download_url': 'https://github.com/1138014573/checkmk-allswap-plugin',
    'description': 'Production active monitoring check for verifying multi-chain RPC endpoints and AllSwap cross-chain liquidity health.',
    'files': {
        'active_checks': ['check_allswap_rpc']
    },
    'num_files': 1
}

output_mkp = "d:/www/js/ie9.cc/checkmk-allswap-plugin/allswap_rpc_health-1.0.0.mkp"

with tarfile.open(output_mkp, "w:gz") as tar:
    info_bytes = repr(info_dict).encode('utf-8')
    tarinfo = tarfile.TarInfo(name="info")
    tarinfo.size = len(info_bytes)
    tar.addfile(tarinfo, io.BytesIO(info_bytes))
    
    plugin_path = "d:/www/js/ie9.cc/checkmk-allswap-plugin/plugins/check_allswap_rpc.py"
    with open(plugin_path, "rb") as f:
        plugin_bytes = f.read()
    p_info = tarfile.TarInfo(name="active_checks/check_allswap_rpc")
    p_info.size = len(plugin_bytes)
    p_info.mode = 0o755
    tar.addfile(p_info, io.BytesIO(plugin_bytes))

print(f"Successfully generated {output_mkp} (Size: {os.path.getsize(output_mkp)} bytes)")
