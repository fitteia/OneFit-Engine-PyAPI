import os
import json
import argparse
import shutil
from ofe import ofe

def main():
    parser = argparse.ArgumentParser()

    # Add arguments or options
    parser.add_argument(
        "--clean", 
        action="store_true",
        default=False,
        help="Remove dowload folder"
    )

    parser.add_argument(
        "input_file", 
        type=str, 
        help="Input file"
    )

    parser.add_argument(
        "--function", 
        type=str,
        default= ofe.FUNCTION,
        help="Fitting function"
    )

    parser.add_argument(
        "--autox", 
        action="store_true",
        default=False,
        help="autox"
    )
    parser.add_argument(
        "--autoy", 
        action="store_true",
        default=False,
        help="autoy"
    )

    parser.add_argument(
        "--logx", 
        action="store_true",
        default=False,
        help="logx"
    )

    parser.add_argument(
        "--logy", 
        action="store_true",
        default=False,
        help="logy"
    )
    
    # Parse the arguments
    args = parser.parse_args()

    # Use the arguments in your script
    file_path = args.input_file
    force_clean = args.clean
    autox = args.autox
    autoy = args.autoy
    logx = args.logx
    logy = args.logy
    function = args.function

    ofe.set_PARAMS("function",function)

    if file_path.endswith(".hdf5"):
        ofe.set_PARAMS("stelar-hdf5","yes")

    if autox:
        ofe.set_PARAMS("autox","yes")

    if autoy:
        ofe.set_PARAMS("autoy","yes")
        
    if logx:
        ofe.set_PARAMS("logx","yes")

    if logy:
        ofe.set_PARAMS("logy","yes")

    print(ofe.PARAMS)

    DOWNLOAD_FOLDER = "/tmp/ofe"
    
    json_file = ofe.fit(file_path,DOWNLOAD_FOLDER)

    if force_clean:
        shutil.rmtree(json_file.get("tmp_folder"))
        print(f"Folder {json_file.get("tmp_folder")} removed.")
    else:
        print(f"Folder {json_file.get("tmp_folder")} not removed.")


if __name__ == "__main__":
    main()