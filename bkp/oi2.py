import re

def extract_images(xml_text):
    return set(re.findall(r'\[\[(?:Arquivo|File):(.*?)\]\]', xml_text))

with open("SISREG-20260415193614.xml", encoding="utf-8") as f:
    xml = f.read()

images = extract_images(xml)

print(images)