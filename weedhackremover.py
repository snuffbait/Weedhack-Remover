import os
import shutil
import subprocess
import glob
import winreg

def remove_scheduled_task():
    try:
        subprocess.run(
            ['schtasks', '/Delete', '/TN', 'JavaSecurityUpdater', '/F'],
            capture_output=True
        )
        print("[+] Removed scheduled task: JavaSecurityUpdater")
    except:
        print("[-] Could not remove scheduled task (may not exist)")

def remove_persistence_folder():
    folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'SecurityUpdates')
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
        print(f"[+] Removed folder: {folder}")
    else:
        print("[-] SecurityUpdates folder not found")

def remove_defender_exclusion():
    try:
        cmd = "Remove-MpPreference -ExclusionPath 'C:\\Users'"
        subprocess.run(['powershell', '-Command', cmd], capture_output=True)
        print("[+] Removed Defender exclusion for C:\\Users")
    except:
        print("[-] Could not remove Defender exclusion (may need admin)")

def clean_registry():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)

        bad_values = []
        i = 0
        while True:
            try:
                name, data, _ = winreg.EnumValue(key, i)
                if 'SecurityUpdates' in str(data) or 'JavaSecurityUpdater' in name:
                    bad_values.append(name)
                i += 1
            except OSError:
                break

        for name in bad_values:
            winreg.DeleteValue(key, name)
            print(f"[+] Removed registry value: {name}")

        winreg.CloseKey(key)

        if not bad_values:
            print("[-] No malicious registry entries found")
    except:
        print("[-] Could not check registry")

def clean_temp_files():
    temp = os.environ.get('TEMP', '')
    if temp:
        for f in glob.glob(os.path.join(temp, 'lib*.tmp')):
            try:
                os.remove(f)
                print(f"[+] Removed temp file (might be false positive): {f}")
            except:
                pass

def main():
    print("=" * 50)
    print("Weedhack Malware Removal Tool")
    print("=" * 50)
    print()

    remove_scheduled_task()
    remove_persistence_folder()
    remove_defender_exclusion()
    clean_registry()
    clean_temp_files()

    print()
    print("=" * 50)
    print("Removal complete.")
    print()
    print("IMPORTANT: You should also:")
    print("  - Change your Minecraft password")
    print("  - Reset your Discord token (just change your Discord password)")
    print("  - Clear saved passwords in browsers")
    print("  - Check crypto wallets for unauthorized access")
    print("=" * 50)

if __name__ == '__main__':
    main()
