"""
Fix CSV header to include confidence and image_path columns
"""
import csv

# Read existing data
with open('potholes.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Update header
correct_header = ["id", "latitude", "longitude", "timestamp", "confidence", "image_path"]
rows[0] = correct_header

# Write back
with open('potholes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("✅ CSV header fixed!")
print(f"   Header: {correct_header}")
print(f"   Total rows: {len(rows)}")
