from seewo_editor.assets import ensure_assets


def initialize_data_directories():
    return ensure_assets()


if __name__ == "__main__":
    initialize_data_directories()
