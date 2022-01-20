import glob
import os
import subprocess
import config


def gen_command(i_file, i_file_ext, n_file_ext, animated=False):
    if not animated:
        return ["convert", i_file, (file.replace(i_file_ext, n_file_ext))]
    elif animated:
        return ["ffmpeg", "-i", i_file, (file.replace(i_file_ext, n_file_ext))]


if __name__ == '__main__':
    if config.source_path == "":
        print("Source path is empty, please verify config.py")
    else:
        a_file_list = sorted(glob.glob(config.source_path + "/*.**"))
        c_file_list = list(f for f in a_file_list if os.path.splitext(f)[1] in config.img_types or os.path.splitext(f)[1] in config.vid_types)
        c_len, a_len = len(c_file_list), len(a_file_list)
        print(f"Converting {c_len}/{a_len} files...")
        count = 0
        for index, file in enumerate(c_file_list):
            f_ext = os.path.splitext(file)[1]
            if f_ext in config.img_types:
                count += 1
                subprocess.call(gen_command(file, f_ext, config.preferred_img_ext, False))
                print(f"{count}/{c_len}: Converted \"{file}\" to \"{config.preferred_img_ext}\"...")
            elif f_ext in config.vid_types:
                count += 1
                print(gen_command(file, f_ext, config.preferred_vid_ext, True))
                print(f"{count}/{c_len}: Converted \"{file}\" to \"{config.preferred_vid_ext}\"...")
            print("Done.")