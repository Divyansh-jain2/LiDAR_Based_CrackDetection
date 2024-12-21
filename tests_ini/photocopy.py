base_path = "/home/admin/dp/integration/runs/seg"
runs_dir = "/home/admin/dp/integration/runs"
csv_file = "/path/to/your/csv_file.csv"  

latest_dir = max(
    (os.path.join(base_path, d) for d in os.listdir(base_path) if d.startswith("predict")),
    key=os.path.getctime
)

os.makedirs(runs_dir, exist_ok=True)

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    filenames = [row[0] for row in reader]

for filename in filenames:
    src = os.path.join(latest_dir, filename)
    dest = os.path.join(runs_dir, filename)

    if os.path.exists(src):
        shutil.copy(src, dest)
        print(f"Copied: {filename}")
    else:
        print(f"File not found: {filename}")

print("All specified images have been copied!")