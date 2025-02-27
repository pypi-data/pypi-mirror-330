import os
import stat
import uuid
import requests
import toml
import subprocess

def fast_reverse_proxy(port: int):
    """
    Set up a Fast Reverse Proxy configuration
    
    Args:
        port (int): Local port to proxy

    """
    # Generate random ID
    random_id = str(uuid.uuid4()).replace('-', '')[:24]
    
    # Set up cache directory
    cache_dir = os.path.expanduser('~/.cache/mw/bin')
    os.makedirs(cache_dir, exist_ok=True)
    
    # Download frpc if not exists
    frpc_path = os.path.join(cache_dir, 'frpc')
    if not os.path.exists(frpc_path):
        response = requests.get('https://heywhale-public.oss-cn-shanghai.aliyuncs.com/frp-0.61.0/frpc')
        with open(frpc_path, 'wb') as f:
            f.write(response.content)
        # Make executable
        os.chmod(frpc_path, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

    # Create frpc.toml config in the same cache directory
    config_path = os.path.join(cache_dir, 'frpc.toml')
    HEYWHALE_FRP_SITE = os.getenv("HEYWHALE_FRP_SITE", "frp.heywhale.com")
    # Create frpc.toml config
    config = {
        'serverAddr': 'klab-frps-service',
        'serverPort': 8080,
        'proxies': [{
            'name': 'web',
            'type': 'http', 
            'localPort': port,
            'customDomains': [f'{random_id}.{HEYWHALE_FRP_SITE}']
        }]
    }
    
    with open(config_path, 'w') as f:
        toml.dump(config, f)
    
    # Get the proxy URL
    proxy_url = f'http://{random_id}.{HEYWHALE_FRP_SITE}'
    
    # Execute frpc command
    try:
        process = subprocess.Popen(
            [frpc_path, '-c', config_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        print(f"FRP proxy URL: {proxy_url}")
        
        # Wait for the process to complete and capture output
        stdout, stderr = process.communicate()
                
        if process.returncode != 0:
            raise RuntimeError(
                f"FRP proxy process exited with code {process.returncode}\n"
                f"stdout: {stdout}\n"
                f"stderr: {stderr}"
            )
        
        # Print the output if needed
        if stdout:
            print("Process output:", stdout)
        if stderr:
            print("Process errors:", stderr)

    except Exception as e:
        raise RuntimeError(f"Error setting up FRP proxy: {str(e)}")