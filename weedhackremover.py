import os
import shutil
import subprocess
import glob
import winreg

def killtask():
    subprocess.run(['schtasks', '/Delete', '/TN', 'JavaSecurityUpdater', '/F'], capture_output=True)

def killfolder():
    folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'SecurityUpdates')
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)

def cleanregistry():
    subprocess.run(
        ['powershell', '-Command', "Remove-MpPreference -ExclusionPath 'C:\\Users'"],
        capture_output=True
    )

def cleanregistry():
    keyp = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyp, 0, winreg.KEY_ALL_ACCESS)
    badval = []
    i = 0
    while True:
        try:
            name, data, _ = winreg.EnumValue(key, i)
            if 'SecurityUpdates' in str(data) or 'JavaSecurityUpdater' in name:
                badval.append(name)
            i += 1
        except OSError:
            break
    for name in badval:
        winreg.DeleteValue(key, name)
    winreg.CloseKey(key)

def cleantemp():
    temp = os.environ.get('TEMP', '')
    if temp:
        for f in glob.glob(os.path.join(temp, 'lib*.tmp')):
            try:
                os.remove(f)
            except:
                pass

def main():
    killtask()
    killfolder()
    cleanregistry()
    cleanregistry()
    cleantemp()
    print(
        "\nRemoval complete.\n"
        "\nImportant, please take the following steps:\n"
        "  1 Change your Minecraft password immediately\n"
        "  2 Reset your Discord password to invalidate your token\n"
        "  3 Go to Discord User Settings > Devices and remove any unrecognized sessions\n"
        "  4 Sign out of all Gmail sessions via Google Account > Security > Your Devices\n"
        "  5 Change your Steam password and deauthorize all devices in Steam settings\n"
        "  6 Clear all saved passwords from your browsers\n"
        "  7 Review your crypto wallets for any unauthorized transactions"
    )

if __name__ == '__main__':
    main()
