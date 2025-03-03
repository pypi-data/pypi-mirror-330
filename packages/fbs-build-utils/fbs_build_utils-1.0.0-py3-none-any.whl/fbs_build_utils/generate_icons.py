import os

import click
from PIL import Image
from PIL.Image import Image as ImageFile


def save_icon(image: ImageFile, path: str, size: tuple):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    new_image = image.resize(size)
    new_image.save(path)
    print(f"Icon created: '{path}'")


# icon filename to use
def generate_icons(path):
    image = Image.open(path)
    base_path = os.path.abspath(os.path.dirname(path))

    base_icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)]
    linux_icon_sizes = [(128, 128), (256, 256), (512, 512), (1024, 1024)]
    mac_icon_sizes = [(128, 128), (256, 256), (512, 512), (1024, 1024)]

    # Create base icon sizes in src/main/icons/base
    for size in base_icon_sizes:
        save_icon(image, os.path.join(base_path, "base", str(size[0]) + ".png"), size)

    # Create linux icon sizes in src/main/icons/linux
    for size in linux_icon_sizes:
        save_icon(image, os.path.join(base_path, "linux", str(size[0]) + ".png"), size)

    # Create mac icon sizes in src/main/icons/mac
    for size in mac_icon_sizes:
        save_icon(image, os.path.join(base_path, "mac", str(size[0]) + ".png"), size)

    # Create Icon.ico in src/main/icons/Icon.ico
    new_logo_ico_filename = os.path.join(base_path, "Icon.ico")
    new_logo_ico = image.resize((128, 128))
    new_logo_ico.save(new_logo_ico_filename, format="ICO", quality=90)
    print("Icon created: " + new_logo_ico_filename)


@click.command()
@click.argument("path", type=click.Path(exists=False, readable=True))
def cli(path):
    generate_icons(path)


if __name__ == "__main__":
    cli()
