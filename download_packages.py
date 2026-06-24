import os
import re
import sys
import subprocess

def download_package(requirement, platform, dest_dir):
    # Base command for pip download
    cmd = [
        sys.executable, "-m", "pip", "download",
        requirement,
        "--platform", platform,
        "--only-binary=:all:",
        "-d", dest_dir
    ]
    # Run the command and capture output
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return True, result.stdout
    else:
        return False, result.stderr

def main():
    requirements_file = "requirements.txt"
    dest_dir = "./packages"
    
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found.", file=sys.stderr)
        sys.exit(1)
        
    os.makedirs(dest_dir, exist_ok=True)
    
    # Read requirements file lines
    with open(requirements_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]
        
    platforms = ["win_amd64", "manylinux2014_x86_64"]
    
    # Regex to split package name and extras from version constraints
    # Example: "uvicorn[standard]==0.30.6" -> "uvicorn[standard]", "==0.30.6"
    # Example: "confluent-kafka" -> "confluent-kafka", ""
    pattern = re.compile(r"^([^>=<~!]+)(.*)$")
    
    for platform in platforms:
        platform_name = "WINDOWS" if "win" in platform else "LINUX"
        print("\n" + "="*50)
        print(f"Downloading {platform_name} packages ({platform})...")
        print("="*50)
        
        for line in lines:
            if not line or line.startswith("#"):
                continue
                
            print(f"\n[+] Processing: {line}")
            success, output = download_package(line, platform, dest_dir)
            if success:
                print(f"    Success: {line} downloaded successfully.")
            else:
                # If download failed, parse version constraints and fallback to latest
                match = pattern.match(line)
                if match:
                    pkg_base, version_spec = match.groups()
                    pkg_base = pkg_base.strip()
                    version_spec = version_spec.strip()
                    
                    if version_spec:
                        print(f"    Warning: Failed to download exact version '{line}'.")
                        print(f"    Attempting fallback to the latest version of '{pkg_base}'...")
                        fallback_success, fallback_output = download_package(pkg_base, platform, dest_dir)
                        if fallback_success:
                            print(f"    Success: Downloaded the latest version of '{pkg_base}' instead.")
                        else:
                            print(f"    ERROR: Failed to download '{pkg_base}' (latest version).")
                            print(f"    Details:\n{fallback_output.strip()}", file=sys.stderr)
                    else:
                        print(f"    ERROR: Failed to download '{line}'.")
                        print(f"    Details:\n{output.strip()}", file=sys.stderr)
                else:
                    print(f"    ERROR: Failed to download '{line}'.")
                    print(f"    Details:\n{output.strip()}", file=sys.stderr)

    print("\n" + "="*50)
    print("Done! All available packages are inside the 'packages' folder.")
    print("="*50)

if __name__ == "__main__":
    main()
