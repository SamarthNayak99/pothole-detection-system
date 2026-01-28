"""
Fix all image paths in CSV to include 'detected_potholes/' prefix
"""
import csv
import os

CSV_FILE = "potholes.csv"
BACKUP_FILE = "potholes_before_path_fix.csv"

print("=" * 60)
print("FIXING IMAGE PATHS IN CSV")
print("=" * 60)

# Create backup
print(f"\n📁 Creating backup: {BACKUP_FILE}")
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'r') as f:
        content = f.read()
    with open(BACKUP_FILE, 'w') as f:
        f.write(content)
    print("✅ Backup created!")
else:
    print("❌ CSV file not found!")
    exit(1)

# Read CSV
print(f"\n📖 Reading {CSV_FILE}...")
with open(CSV_FILE, 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"✅ Found {len(rows)} potholes")

# Fix image paths
fixed_count = 0
for row in rows:
    image_path = row.get('image_path', '')
    
    if image_path and image_path.strip():
        # Check if path already has 'detected_potholes/'
        if not image_path.startswith('detected_potholes/'):
            # Add prefix
            row['image_path'] = f"detected_potholes/{image_path}"
            fixed_count += 1

print(f"\n🔧 Fixed {fixed_count} image paths")

# Write back to CSV
print(f"\n💾 Writing updated CSV...")
with open(CSV_FILE, 'w', newline='') as f:
    fieldnames = ['id', 'latitude', 'longitude', 'timestamp', 'confidence', 'image_path']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("✅ CSV updated successfully!")

# Show sample of fixed paths
print(f"\n📊 Sample of fixed paths:")
count = 0
for row in rows:
    if row.get('image_path', '').startswith('detected_potholes/'):
        print(f"   Pothole #{row['id']}: {row['image_path']}")
        count += 1
        if count >= 5:
            break

print("\n" + "=" * 60)
print("✅ COMPLETE! All image paths fixed!")
print("=" * 60)
print(f"\n📝 Summary:")
print(f"   - Total potholes: {len(rows)}")
print(f"   - Paths fixed: {fixed_count}")
print(f"   - Backup saved: {BACKUP_FILE}")
print(f"\n🗺️ Now refresh the map page - images should load!")
