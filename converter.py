import glob
import os
import subprocess
import config


# Set animated as true if file is a video format.
def gen_command(input_file: str, dest_path: str, output_file: str, animated: bool):
    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)
    if not animated:
        return ["convert", input_file, output_file]
    else:
        return ["ffmpeg", "-i", input_file, output_file]


if __name__ == '__main__':
    # Verify path, if not empty continue
    if config.source_path == "":
        print("Source path cannot be empty, please verify config.py")
    else:
        # Get the list of files and their length
        a_file_list = sorted(glob.glob(config.source_path + "/*.**"))
        a_len = len(a_file_list)
        c_file_list = list(f for f in a_file_list
                           if os.path.splitext(f)[1] in config.img_types or os.path.splitext(f)[1] in config.vid_types)
        c_len = len(c_file_list)
        print("Converting {} out of {} files".format(c_len, a_len))
        # Set the parameters to be used in the conversion
        count = 0
        for i_file in c_file_list:
            if_longpath, if_ext = os.path.splitext(i_file)  # Long path without extension and extension respectively
            if_shortname = (os.path.basename(i_file).replace(if_ext, ""))  # Only the file's shortname
            a_file = True if if_ext in config.vid_types else False  # Boolean, true if file is video, false if it isn't
            o_file = (
                config.destination_path + "/" + if_shortname + config.p_img_ext if a_file is False else if_shortname + config.p_vid_ext
            )
            # Conversion
            count += 1
            if o_file not in glob.glob(config.destination_path + "/*.**"):
                subprocess.call(gen_command(i_file, config.destination_path, o_file, a_file))
                print("{}/{}: Converted {} to {}".format(count, c_len, i_file, o_file))
            else:
                print("Skipping \"{}\". Already exists.".format(i_file))
        # Post conversion
        copy_bool = (True if input(
            "Copy remaining files? [Y/n]: ").upper() == "Y" else False
                     ) if config.autocopy == "" else config.autocopy
        for file in list(set(a_file_list) - set(c_file_list)):
            if file.replace(config.source_path, config.destination_path) not in glob.glob(config.destination_path + "/*.**"):
                print("Copying {} to {}".format(file, file.replace(config.source_path, config.destination_path)))
                subprocess.call(["cp", file, file.replace(config.source_path, config.destination_path)])
            else:
                print("Skipping \"{}\". Already exists.".format(file))
        print("Done.")
