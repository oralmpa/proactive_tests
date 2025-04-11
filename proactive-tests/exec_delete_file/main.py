import sys
from delete_file.zenoh_delete_file import delete_file  # replace with actual filename if modularized

def main():

    zenoh_key = sys.argv[1]

    print(f"🗑️ Attempting to delete from Zenoh key: {zenoh_key}")
    success = delete_file(zenoh_key)

    if success:
        print(f"✅ Deleted: {zenoh_key}")
    else:
        print("❌ Deletion failed")

if __name__ == '__main__':
    main()
