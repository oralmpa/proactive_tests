import zenoh

zenoh_config = zenoh.Config()
zenoh_config.insert_json5("mode", '"client"')
zenoh_config.insert_json5("connect/endpoints", '["tcp/zenoh16:17447"]')

# Open Zenoh session
zenoh_session = zenoh.open(zenoh_config)


def delete_file(zenoh_key):
    """
    Delete a file from Zenoh.
    :param zenoh_key: The Zenoh key of the file.
    """
    try:
        pub = zenoh_session.declare_publisher(zenoh_key)
        pub.delete()
        print(f"✅ File deleted from Zenoh: {zenoh_key}")
        return True
    except Exception as e:
        print(f"❌ Failed to delete file: {e}")
        return False