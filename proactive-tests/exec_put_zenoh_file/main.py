import sys
from put_file.zenoh_put_file import put_file

def main():
    if len(sys.argv) < 3:
        print("❌ Usage: python zenoh_put_main.py <local_path> <zenoh_key>")
        sys.exit(1)

    local_path = sys.argv[1]
    zenoh_key = sys.argv[2]

    print(f"🚀 Uploading {local_path} → {zenoh_key}")
    success = put_file(zenoh_key, local_path)

    if success:
        print(f"✅ Upload completed: {local_path} → {zenoh_key}")
    else:
        print("❌ Upload failed")

if __name__ == '__main__':
    main()
