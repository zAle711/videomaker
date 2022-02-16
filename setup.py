import pathlib

MAIN_FOLDER = pathlib.Path().parent.resolve()

DOWNLOAD_FOLDER = MAIN_FOLDER.joinpath('download')
OUTPUT_FOLDER = MAIN_FOLDER.joinpath('output')
TEST_FOLDER = MAIN_FOLDER.joinpath('test')
TEMP_FOLDER = MAIN_FOLDER.joinpath('temp')

DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok= True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok= True)
TEST_FOLDER.mkdir(parents=True, exist_ok= True)
TEMP_FOLDER.mkdir(parents=True, exist_ok= True)
