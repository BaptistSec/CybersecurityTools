import winreg
import datetime

# Define the Registry keys to scan
keys = [
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run",
    "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run",
    "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
    "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run",
]

# Define a list of known good values
whitelist = [
    ("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", "Windows Defender", r"C:\Program Files\Windows Defender\MSASCuiL.exe"),
    ("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", "OneDrive", r"C:\Users\Username\AppData\Local\Microsoft\OneDrive\OneDrive.exe /background"),
]

# Create a list to store the results
results = []

# Loop through each Registry key and extract the values
for key in keys:
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ)
        num_values = winreg.QueryInfoKey(registry_key)[1]
        for i in range(num_values):
            value_name, value_data, value_type = winreg.EnumValue(registry_key, i)
            results.append((key, value_name, value_data, value_type, datetime.datetime.now()))
    except:
        continue

# Output the results to a file
with open("registry_results.txt", "w") as f:
    f.write("Registry key\tValue name\tValue data\tValue type\tTimestamp\n")
    for result in results:
        f.write(f"{result[0]}\t{result[1]}\t{result[2]}\t{result[3]}\t{result[4]}\n")
        
print(f"Results written to registry_results.txt. Total results: {len(results)}")

# Compare the results to the whitelist and output any deviations to a separate file
deviations = []
for result in results:
    if (result[0], result[1], result[2]) not in whitelist:
        deviations.append(result)

if deviations:
    with open("registry_deviations.txt", "w") as f:
        f.write("Registry key\tValue name\tValue data\tValue type\tTimestamp\n")
        for deviation in deviations:
            f.write(f"{deviation[0]}\t{deviation[1]}\t{deviation[2]}\t{deviation[3]}\t{deviation[4]}\n")
    print(f"Deviations from whitelist detected. Deviations written to registry_deviations.txt. Total deviations: {len(deviations)}")
else:
    print("No deviations from whitelist detected.")
