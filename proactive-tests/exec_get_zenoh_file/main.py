import sys
from get_file.zenoh_get_file import get_file

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <zenoh_key> <local_path>")
        return

    zenoh_key = sys.argv[1]
    local_path = sys.argv[2]

    print(f"Getting from Zenoh key: {zenoh_key}")
    success = get_file(zenoh_key, local_path)

    if success:
        print(f"Downloaded to {local_path}")
    else:
        print(f"Download failed")

if __name__ == '__main__':
    main()
