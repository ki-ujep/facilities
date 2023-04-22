import os
import shutil
import argparse

def copy_files(root_dir, attachments_target, pictures_target):
    # Iterate through the root directory
    for device_folder in os.listdir(root_dir):
        device_path = os.path.join(root_dir, device_folder)

        # Ensure that the item is a directory
        if not os.path.isdir(device_path):
            continue

        # Iterate through the device directory
        for subfolder in os.listdir(device_path):
            subfolder_path = os.path.join(device_path, subfolder)

            # Ensure that the item is a directory
            if not os.path.isdir(subfolder_path):
                continue

            # Copy the Attachments and Pictures to their respective target folders
            if subfolder == 'Attachments':
                for file in os.listdir(subfolder_path):
                    src_path = os.path.join(subfolder_path, file)
                    dest_path = os.path.join(attachments_target, file)
                    shutil.copy(src_path, dest_path)

            elif subfolder == 'Pictures':
                for file in os.listdir(subfolder_path):
                    src_path = os.path.join(subfolder_path, file)
                    dest_path = os.path.join(pictures_target, file)
                    shutil.copy(src_path, dest_path)

    # Print a success message
    print("All Attachments and Pictures copied successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy Attachments and Pictures from device folders.")
    parser.add_argument("-rd", "--root_dir", type=str, required=True,
                        help="The root directory containing device folders.")
    parser.add_argument("-at", "--attachments_target", type=str, required=True,
                        help="The target directory for Attachments.")
    parser.add_argument("-pt", "--pictures_target", type=str, required=True,
                        help="The target directory for Pictures.")

    args = parser.parse_args()

    copy_files(args.root_dir, args.attachments_target, args.pictures_target)

