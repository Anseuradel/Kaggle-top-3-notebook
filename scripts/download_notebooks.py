import os
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

COMPETITIONS = [
    "manga-sales-prediction",  # replace with your target competitions
]

TOP_K = 3
BASE_DIR = "Kaggle-top-3-notebook"

api = KaggleApi()
api.authenticate()

def fetch_notebooks(competition):
    kernels = api.kernels_list(competition=competition, sort_by='voteCount', page_size=TOP_K)

    for i, kernel in enumerate(kernels[:TOP_K], start=1):
        folder_name = f"{i}_{competition.replace('-', '_')}"
        os.makedirs(os.path.join(BASE_DIR, folder_name), exist_ok=True)

        print(f"⬇️ Downloading: {kernel.ref}")
        api.kernels_pull(kernel.ref, path=os.path.join(BASE_DIR, folder_name), metadata=False)

        # Rename the notebook file to match the folder
        files = os.listdir(os.path.join(BASE_DIR, folder_name))
        for file in files:
            if file.endswith(".ipynb"):
                src = os.path.join(BASE_DIR, folder_name, file)
                dst = os.path.join(BASE_DIR, folder_name, f"{folder_name}.ipynb")
                os.rename(src, dst)

def main():
    for comp in COMPETITIONS:
        fetch_notebooks(comp)

if __name__ == "__main__":
    main()
