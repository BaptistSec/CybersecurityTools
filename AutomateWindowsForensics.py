import winreg

# Define the Registry keys to scan
keys = [
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run",
    "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run",
    "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
    "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run",
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
            results.append((key, value_name, value_data, value_type))
    except:
        continue

# Output the results to a file
with open("registry_results.txt", "w") as f:
    f.write("Registry key\tValue name\tValue data\tValue type\n")
    for result in results:
        f.write(f"{result[0]}\t{result[1]}\t{result[2]}\t{result[3]}\n")
        
print(f"Results written to registry_results.txt. Total results: {len(results)}")
