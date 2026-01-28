"""
Check detected potholes and images
"""
import os
import csv

print("=" * 60)
print("POTHOLE DETECTION STATUS")
print("=" * 60)

# Check detected_potholes folder
images_dir = "detected_potholes"
if os.path.exists(images_dir):
    images = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]
    print(f"\n📁 Images in {images_dir}:")
    print(f"   Total images: {len(images)}")
    if images:
        print(f"\n   Latest 5 images:")
        for img in sorted(images, reverse=True)[:5]:
            size = os.path.getsize(os.path.join(images_dir, img))
            print(f"   - {img} ({size:,} bytes)")
else:
    print(f"\n❌ Folder {images_dir} not found!")

# Check CSV
csv_file = "potholes.csv"
if os.path.exists(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"\n📊 Potholes in CSV:")
        print(f"   Total records: {len(rows)}")
        if rows:
            print(f"\n   Latest 5 records:")
            for row in rows[-5:]:
                img_path = row.get('image_path', 'None')
                conf = row.get('confidence', 'N/A')
                print(f"   - ID {row['id']}: Confidence={conf}, Image={img_path}")
else:
    print(f"\n❌ File {csv_file} not found!")

print("\n" + "=" * 60)
