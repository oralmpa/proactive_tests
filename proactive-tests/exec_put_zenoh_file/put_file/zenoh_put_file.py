import sys
import zenoh


# ✅ Open Zenoh session
zenoh_config = zenoh.Config()
zenoh_config.insert_json5("mode", '"client"')
zenoh_config.insert_json5("connect/endpoints", '["tcp/zenoh16:17447"]')
zenoh_session = zenoh.open(zenoh_config)

info = zenoh_session.info()
zid = str(info.zid())
routers = [str(router) for router in info.routers_zid()]
print(f"✅ Connected to Zenoh at {routers}")


def put_file(zenoh_key, local_path):
    """
    Upload a file to Zenoh.
    :param zenoh_key: The Zenoh key where the file will be stored.
    :param local_path: Path to the local file.
    """
    try:
        with open(local_path, "rb") as f:
            content = f.read()

        pub = zenoh_session.declare_publisher(zenoh_key)
        pub.put(content)
        print(f"✅ File uploaded to Zenoh: {zenoh_key}")
        return True
    except Exception as e:
        print(f"❌ Failed to upload file: {e}")
        return False


def main():
    if len(sys.argv) < 3:
        print("❌ Usage: python zenoh_put_file.py <local_path> <zenoh_key>")
        sys.exit(1)

    local_path = sys.argv[1]
    zenoh_key = sys.argv[2]

    print(f"🚀 Uploading {local_path} to Zenoh key: {zenoh_key}")
    success = put_file(zenoh_key, local_path)

    if success:
        print(f"✅ Upload completed: {local_path} -> {zenoh_key}")
    else:
        print("❌ Upload failed")


if __name__ == '__main__':
    main()
