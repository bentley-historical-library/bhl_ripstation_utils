# BHL Born-digital Utilities
Scripts and templates used for born-digital transfers at the Bentley Historical Library. These utilities are primarily used to assist in the transfer of materials from removable media using the BHL's Removable Media Workstations (RMWs) and RipStation.

## Requirements

- Python 3: Required to run all utilities
- Pillow: To adjust images of removable media
- FFmpeg: To validate audio and video files and to create DIPs for audio CDs
- HandBrake CLI: To create DIPs for video DVDs
- bulk_extractor: To scan for PII
- rsync: To copy files on non-Windows machines
- Brunnhilde: To generate reports (non-Windows machines only)

## Installation
`pip install git+https://github.com/bentley-historical-library/bhl_born_digital_utils.git`

## bhl_inventory.csv
A tracking template used for born-digital transfers at the Bentley Historical Library. Many of the utilities detailed below rely on the bhl_inventory.csv. See [README for bhl_inventory.csv](bhl_born_digital_utils/lib/bhl_inventory/README.md).

## bhl_bd_utils.py
This script serves as the entry point to various born-digital transfer utilities. A summary of the script's usage and available actions are below, followed by detailed instructions for each utility. All utilities require, at minimum, an accession number, corresponding to a directory with transferred removable media items, and an action.

Usage: `bhl_bd_utils.py ACCESSION_NUMBER action [options]`

| Action | Description |
| --- | --- |
| -c, --create_transfer | Create a RMW transfer |
| -e, --empty | Check for empty folders and files |
| -m, --missing | Check for missing barcodes and folders |
| -o, --osfiles | Check for and delete system files and directories |
| -s, --structure | Check RipStation output structure |
| -u, --unhide | Unhide folders (Windows workstations only) |
| -b, --bulkextractor | Run bulk_extractor |
| --copy | Copy accession from RMW |
| --move_separations | Move separations |
| --av_media | Separate AV media |
| --rename_files | Rename files with invalid characters |
| --dips | Make DIPs for audio CDs and video DVDs |
| --split_transfer | Split transfer into smaller chunks |
| --brunnhilde | Run Brunnhilde |


### BHL Born Digital Utils Configuration
Many of born-digital transfer utilities make use of a `.bhl_bd_utils` configuration file in the current user's home directory. If a configuration file does not exist, the utility will prompt you to create one. The available settings are detailed below.

| Setting | Description |
| --- | --- |
| input | Directory where accession directories can be found. This should be a local directory. |
| logs | Directory where various program logs will be stored |
| destination | Directory where accessions will be copied to from the RMW |
| separations | Directory where separations will be moved |
| webcam_dir | Directory where images are saved by the RMW's webcam |
| handbrake | Full path to an installed HandBrake CLI executable |
| handbrake_preset | Full path to a HandBrake preset JSON file |
| ffmpeg | Full path to an installed FFmpeg executable |
| bulk_extractor | Full path to an installed bulk_extractor executable |
| brunnhilde | Directory where Brunnhilde reports will be stored |

Some of these settings can be overriden from the command line. For example, an `-i` flag can be passed along with the path to a directory to override the configured input directory. Below are the optional arguments that can be passed to `bhl_bd_utils.py` and the configuration default that they override.

| Argument | Help |
| --- | --- |
| -i, --input | Override `input` |
| -d, --destination | Override `destination` |
| -l, --logs | Override `logs` |
| --separations_dir | Override `separations` |

By default, `bhl_bd_utils.py` assumes that the scripts are being run on transfers on a local RMW directory. In some cases, these scripts may be run on a transfer after it has been copied to the remote `destination` directory. Passing a `--base remote` will override the default behavior and use the configured `destination` directory as the `input` directory.


### Create a RMW transfer
Creates accession and barcode directories, bhl_metadata, and bhl_notices directories within the configured `input` directory.

Requirements:
- This script uses [Pillow](https://github.com/python-pillow/Pillow) to adjust images of removable media. 
- bhl_notice uses [JsBarcode](https://github.com/lindell/JsBarcode) CDN to a render Codabar barcode in the HTML document.  

`bhl_bd_utils.py ACCESSION_NUMBER -c/--create_transfer [--metadata_off] [--notices_off]`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| -c, --create_transfer | Create a RMW transfer |
| --metadata_off | Turn off creating bhl_metadata directory inside barcode folders |
| --notices_off | Turn off creating bhl_notices inside accession folder |

Acknowledgments: This utility is developed based on CollectionSetup.exe by [Matt Adair](https://github.com/umadair).

### Check for empty folders and files
Checks for empty directories and 0-byte files in a source directory and prints the results to the terminal

`bhl_bd_utils.py ACCESSION_NUMBER -e/--empty`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| -e, --empty | Check for empty folders and files |

### Check for missing barcodes and folders
Parses the bhl_inventory.csv and subdirectories for a source directory, compares the results, and lists barcodes that are in the bhl_inventory.csv but not in the source directory and subdirectories in the source directory that are not accounted for in the bhl_inventory.csv

`bhl_bd_utils.py ACCESSION_NUMBER -m/--missing`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| -m, --missing | Check for missing barcodes and folders |

### Check for and delete system files and directories
Checks for and deletes operating system files and directories in a source path. Operating system files checked include Thumbs.db, .DS_Store, Desktop DB, and Desktop DF. Operating system directories checked include .Trashes, .Spotlight-V100, and .fseventsd. The script will print all found files and directories to the terminal to confirm deletion. Optional arguments can turn off deleting Thumbs.db, .DS_Store, Desktop DB/DF, and directories (.Trashes, .Spotlight-V100, and .fseventsd).

`bhl_bd_utils.py ACCESSION_NUMBER -o/--osfiles [--thumbsdb_off] [--dsstore_off] [--desktopdbdf_off] [--dirs_off]`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| -o, --osfiles | Check for and delete system files |
| --thumbsdb_off | Turn off deleting Thumbs.db files |
| --dsstore_off | Turn off deleting .DS_Store files |
| --desktopdbdf_off | Turn off deleting Desktop DB and Desktop DF files |
| --dirs_off | Turn off deleting .Trashes, .Spotlight-V100, and .fseventsd folders |

### Check RipStation output structure
Checks RipStation output structure, including checking to ensure that .mp4 and .wav DIPs have been made for video DVDs and audio CDs, respectively, that photos of removable media exist when applicable, and that .wav and .mp4 files are valid. Optional arguments can turn off validating .wav and .mp4 files.

Requirements: This script uses ffmpeg to validate .wav and .mp4 files.

`bhl_bd_utils.py ACCESSION_NUMBER -s/--structure [--validation_off]`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| --validation_off | Turn off validating .wav (audio CDs) and .mp4 (video DVDs) |

### Unhide folders
Unhide hidden sub-directories in a directory. Note: This removes the Windows -H (hidden) and -S (system) attributes from directories, and as such is only applicable on Windows machines.

`bhl_bd_utils.py ACCESSION_NUMBER -u/--unhide`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| -u, --unhide | Unhide folders |

### Run bulk_extractor
This script will run bulk_extractor from the command line. Currently, scanning for exif metadata generated from images is turned off, and bulk_extractor will use its `accts` scanner to search for PII such as Social Security numbers, credit card numbers, telephone numbers, and email addresses. Reports generated by bulk_extractor will be stored in the configured logs directory. In order to save time, resources, and to avoid false positives, bulk_extractor is not run on audio CDs or video DVDs. bulk_extractor reports are stored in subdirectories for each piece of removable media scanned. Following scanning, all empty reports are deleted, leaving only reports that had one or more hit. On Windows machines, the utility uses the `bulk_extractor` configuraiton setting, corresponding to an exact path to a bulk_extract executable, and on other operating systems assumes that `bulk_extractor` is available on the system path.

`bhl_bd_utils.py ACCESSION_NUMBER -b/--bulkextractor`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| -b, --bulkextractor | Run bulk_extractor |

### Copy accession from RMW
This utility copies a directory using robocopy (on Windows) or rsync (on other operating systems). Its primary purpose is to copy accessions from a removable media workstation to a network storage location. It uses the configured defaults for `input` and `destination`, but can optionally be overriden by passing either an `-i` and/or `-d` argument. This utility will create a log file of the form `[accession_number]_[timestamp].txt` in the configured `logs` directory.

`bhl_bd_utils.py ACCESSION_NUMBER --copy`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| --copy | Copy accession from RMW |

### Move separations
This utility moves separated directories to the configured `separations` directory. The script parses the bhl_inventory.csv in a given source directory to identify media that has been marked as separated by a `separation` column with a value of `y`, and then moves the `_barcode` directory from within the source directory to an `[accession]_separations` directory in the given destination. It optionally takes a `--separations_dir` argument to override the configured `separations` directory.

`bhl_bd_utils.py ACCESSION_NUMBER --move_separations`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| --move_separations | Move separations |

### Separate AV media
This utility moves audio-formatted CDs and video-formatted DVDs into their own directory so that AV content can be processed using Archivematica's automation-tools and data content can be sent to Archivematica's backlog. The script parses the bhl_inventory.csv in a given source directory to identify media with a `media_type` that begins with `audio` or `video` and then moves those barcode directories into a new directory named `[accession]_audiovisual` in the source directory's parent directory. For example, given a source directory of `/path/to/source/1234`, the script will move audiovisual media into `/path/to/source/1234_audiovisual`.

`bhl_bd_utils.py ACCESSION_NUMBER --av_media [-a/-accession ACCESSION]`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| --av_media | Separate AV media |

### Rename files
This utility replaces 'invalid' characters in a filename with an underscore. The script is based heavily off of [Archivematica's sanitize_names.py](https://github.com/artefactual/archivematica/blob/stable/1.9.x/src/MCPClient/lib/clientScripts/sanitize_names.py). The `rename_files` utility allows several more characters in a filename than Archivematica, as its primary use case is to resolve issues with running bagit.py on directories that contain files with certain invalid characters. The utility prints out a list of files that will be renamed and asks for confirmation. This script should be used sparingly, and only after bagging attempts on Windows and Linux filesystems have failed.

`bhl_bd_utils.py ACCESSION_NUMBER --rename_files`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| --rename_files | Rename files |

## Make DIPs
This utility makes access derivatives (DIPs) for audio CDs and video DVDs to be uploaded to the Bentley Digital Media Library. Its primary use case is to make DIPs in batch for media transferred using the RipStation, but can also be used for media transferred using the RMWs. The utility parses the bhl_inventory.csv in a given accession directory to identify all audio CDs and video DVDs that have (1) been successfully transferred and (2) do not have an existing access derivative. The utility then does the following depending on the media type:

- Audio CD: Concatenates all of the individual `.wav` tracks from an audio CD into a single `[barcode].wav` file using FFmpeg. On Windows machines, the utility uses the `ffmpeg` configuration setting, corresponding to an exact path to an FFmpeg executable, and on other operating systems assumes that `ffmpeg` is available on the system path.
- Video DVD: Uses the HandBrake CLI to scan an `.iso` disc image and make an `.mp4` for each title found on the disc. The utility uses the  `handbrake_preset` configuration, which corresponds to the exact path to a HandBrake preset JSON file, to specify the settings for encoding mp4s. If there are multiple disc images (e.g., for media imaged on an RMW using FTK Imager) it will first make a temporary concatenated `.iso` before generating access derivatives. On Windows machines, the utility uses the `handbrake` configuration setting, corresponding to an exact path to a HandBrakeCLI executable, and on other operating systems assumes that `HandBrakeCLI` is available on the system path.

`bhl_bd_utils.py ACCESSION_NUMBER --dips`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| --dips | Make DIPs |

## Split Transfer
This utility splits a transfer into multiple smaller chunks. This is especially useful for transfer with more than 10,000 files, which can cause problems in Archivematica. The utility counts the number of files in each item within a transfer and then moves items into directories of fewer than the split size, which defaults to 5,000 files and can be modified by passing a `--split_size` parameter. The utility keeps individual items whole (i.e., it will not move some subdirectories from one item into chunk and other subdirectories into another chunk). As a result, it is best suited to transfers of many small-to-medium size items, rather than a transfer of one large item (e.g., a single hard drive with 10s of thousands of files). The chunk directories are created inside the transfer directory and are appended with a three-digit sequence. For example, a transfer `172345` with 12,234 files would be split into about 3 chunks: `172345-001`, `172345-002`, `172345-003`

`bhl_bd_utils.py ACCESSION_NUMBER --split_transfer [--split_size INT]`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| --split_transfer | Split transfer into smaller chunks |
| --split_size | Maximum file count for each chunk (optional; defaults to 5,000) |

## Run Brunnhilde
This utility runs [Brunnhilde](https://github.com/tw4l/brunnhilde) to generate reports on the contents of a given transfer. The utility is configured to run Brunnhilde with the `-z` (decompress and scan archived files) and `-n` (skip virus scan) options. The outputs of this scan include a CSV output from Siegfried, a tree report of the transfer's directory structure, and an HTML report with aggregate statistics for the transfer including detailed information about file formats, unidentified files, last modified dates, and duplicate files. Reports will be output to the configured `brunnhilde` directory and will be copied to the transfer's `metadata\submissionDocumentation` directory once Brunnhilde has finished.

This utility can only be run from a Linux or macOS machine.

`bhl_bd_utils.py ACCESSION_NUMBER --brunnhilde`

| Argument | Help |
| --- | --- |
| ACCESSION_NUMBER | The accession number |
| --brunnhilde | Run Brunnhilde |
