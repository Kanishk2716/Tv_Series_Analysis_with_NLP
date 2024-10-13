from glob import glob  # This imports the glob function directly
import pandas as pd

def load_subtitles_dataset(dataset_path):
    # Use glob directly to find all .ass files in the specified dataset_path
    subtitles_path = glob(dataset_path + '/*.ass')

    scripts = []
    episodes_num = []

    for path in subtitles_path:
        # Read Lines
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = lines[27:]  # Skip the first 27 lines as per your structure
            lines = [",".join(line.split(',')[9:]) for line in lines]

        lines = [line.replace('\\N', ' ') for line in lines]
        script = " ".join(lines)

        # Extract the episode number from the file name
        episode = int(path.split('-')[-1].split('.')[0].strip())

        scripts.append(script)
        episodes_num.append(episode)

    # Create a DataFrame from the collected episode numbers and scripts
    df = pd.DataFrame.from_dict({"episode": episodes_num, "script": scripts})
    return df
