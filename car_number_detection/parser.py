import xml.etree.ElementTree as ET
import pandas as pd
import cv2 as cv
import requests
import os
import cloudscraper

scraper = cloudscraper.create_scraper()


def writer(full_name, url):
    with open(full_name, 'wb') as handler:
        img_data = scraper.get(url, stream=True)

        if not img_data.ok:
            return 1
        handler.write(img_data.content)
        return img_data


def parse_from_file():
    tree = ET.parse("example.xml")
    root = tree.getroot()
    save_path = "data/examples"

    names = []
    numbers = []
    images = []
    for i, child in enumerate(root):
        url = child[1].text
        url_plate = child[2].text

        filename = f'{i}.jpg'
        filename_plate = f"{i}_plate.png"
        full_name = os.path.join(save_path, filename)
        full_name_plate = os.path.join(save_path, filename_plate)

        img_data = writer(full_name, url)
        img_plate_data = writer(full_name_plate, url_plate)

        names.append(full_name)
        images.append(img_data)
        numbers.append(child[0].text)

        dict_ = {"names": names, "numbers": numbers}
        df = pd.DataFrame(data=dict_)
        df.to_csv("data.csv", index=False)


def automatic_parser():
    save_path = "data/examples"

    for i in range(406, 1000):
        url = "http://img03.platesmania.com/170705/o/10077" + str(i) + ".jpg"
        filename = f'{i}.jpg'
        full_name = os.path.join(save_path, filename)
        img_data = writer(full_name, url)


if __name__ == "__main__":
    automatic_parser()