import datasets
from datasets import load_dataset
import os
from PIL import Image

# We assume that the dataset contains annotations in YOLO format!
# Additionally, we also assume that images are in PIL format, so we don't need to convert them
def download_dataset(url: str, save_dir: str, **kwargs) -> datasets.dataset_dict.DatasetDict:
    dataset = load_dataset(url, **kwargs)
    os.makedirs(save_dir, exist_ok=True)
    data_file = open(os.path.join(save_dir, 'data.yaml'), 'w')
    for split in dataset.keys():
        split_dir = os.path.join(save_dir, split)
        images_dir = os.path.join(split_dir, 'images')
        labels_dir = os.path.join(split_dir, 'labels')
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        data_file.write(f"{split}: {split_dir}\n")

        for i, example in enumerate(dataset[split]):
            img = example['image']
            img.save(os.path.join(images_dir, f"{split}_{i}.jpg"))

            with open(os.path.join(labels_dir, f"{split}_{i}.txt"), 'w') as f:
                    f.write(f"{example['objects']['category'][0]} {' '.join(str(item) for item in example['objects']['bbox'])}\n")

    dataset_classes = dataset['train'].features['objects'].feature['category'].names
    data_file.write(f"nc: {len(dataset_classes)}\n")
    data_file.write(f"names: {dataset_classes}\n")
    data_file.close()