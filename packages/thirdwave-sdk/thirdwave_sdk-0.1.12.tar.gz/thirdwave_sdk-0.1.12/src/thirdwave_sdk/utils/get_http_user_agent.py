import platform

SDK_NAME="thirdwave-python-sdk"
SDK_VERSION="0.1.12"

def get_http_user_agent() -> str:
    python_version = platform.python_version()
    os_info = f"{platform.system()}; {platform.machine()}"
        
    return f"{SDK_NAME}/{SDK_VERSION} Python/{python_version} ({os_info})"
