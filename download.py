"""Model downloader script"""

from parlai.core.build_data import download_models

download_models(opt={'datapath': '.'}, fnames=['md_gender_classifier.tgz'],
        model_folder='md_gender')
