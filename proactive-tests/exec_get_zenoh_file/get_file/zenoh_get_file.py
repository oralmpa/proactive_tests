# -*- coding: utf-8 -*-
import sys
import zenoh


def get_file(zenoh_key, local_path):

    try:
        zenoh_config = zenoh.Config()
        zenoh_config.insert_json5("mode", '"client"')
        zenoh_config.insert_json5("connect/endpoints", '["http://146.124.106.200:30471"]')
        zenoh_session = zenoh.open(zenoh_config)
        info = zenoh_session.info()
        zid = str(info.zid())
        routers = [str(router) for router in info.routers_zid()]
        print(f"Connected to Zenoh at {routers}")
        replies = zenoh_session.get(zenoh_key, zenoh.Queue())
        for reply in replies:
            if reply.ok:
                with open(local_path, "wb") as f:
                    f.write(reply.ok.payload)
                print(f"✅ File downloaded from Zenoh to {local_path}")
                return True
        print(f"❌ File not found in Zenoh: {zenoh_key}")
        return False
    except Exception as e:
        print(f"❌ Failed to download file: {e}")
        return False


def main():
    if len(sys.argv) < 3:
        print("❌ Usage: python zenoh_get_file.py <zenoh_key> <local_path>")
        sys.exit(1)

    zenoh_key = sys.argv[1]
    local_path = sys.argv[2]

    print(f"📦 Fetching file from Zenoh key: {zenoh_key}")
    success = get_file(zenoh_key, local_path)

    if success:
        print(f"✅ File successfully written to: {local_path}")
    else:
        print(f"❌ Failed to fetch {zenoh_key}")


if __name__ == '__main__':
    main()
