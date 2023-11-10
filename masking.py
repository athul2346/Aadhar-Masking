import io,os
import re
import cv2
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image,ImageDraw


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"YOUR VISION API KEY JSON FILE"
source_folder = r'F:\\my code\\vision api\\input\\'
dest_folder=r'F:\\my code\\vision api\\realinput'
output_folder=r"F:\\my code\\vision api\\output\\"
unmasked=r'F:\\my code\\vision api\\unmasked'

for filename in os.listdir(source_folder):
    if filename.endswith('.jpg') or filename.endswith('.tif') or filename.endswith('.bmp') or filename.endswith('.png'):
        try:
            image = Image.open(os.path.join(source_folder, filename))
            image = image.convert('RGB')
            new_filename = os.path.splitext(filename)[0] + '.jpg'
            image.save(os.path.join(dest_folder, new_filename))
        except OSError:
            print(filename)
# # Instantiates a client
client = vision.ImageAnnotatorClient()
for filename in os.listdir(dest_folder):
    if filename.endswith('.jpg') or filename.endswith('.tiff') or filename.endswith('.bmp') or filename.endswith('.png'):
        # Read the image file
        with io.open(os.path.join(dest_folder, filename), 'rb') as image_file:
            print(filename)
            content = image_file.read()
    image = types.Image(content=content)

# Performs OCR on the image
    response = client.text_detection(image=image)

# Extracts text and bounding boxes from response
    texts = response.text_annotations
    # print(texts)
    if len(texts)==0:
        image = Image.open(os.path.join(dest_folder, filename))
        image.save(os.path.join(unmasked, filename))
    else:  
        boxes = [text.bounding_poly.vertices for text in texts]
        aadhaar_= re.compile(r'\b\d{4}\u0020\d{4}\u0020\d{4}\b')
        aadhaar_num = ''
        for text in texts:
            match = re.search(aadhaar_, text.description)
            if match:
                aadhaar_num = match.group()
            # print(aadhaar_num)
                break
        
        # print(aadhaar_num)
        # aadhaar_num=aadhaar_num.replace(aadhaar_num[:9],'**** ****') 
        

    # Uses regex to find Aadhaar numbers
        aadhaar_pattern = re.compile(r'\b\d{4}\u0020\d{4}')
        # masked_text = response.full_text_annotation.text
        aadhaar_numbers = []
        for match in aadhaar_pattern.findall(aadhaar_num):
        # # Remove the spaces from the Aadhaar number
        # aadhaar_number = match.replace(" ", "")
            aadhaar_numbers.append(match)
        # Mask the Aadhaar number
        # masked_text = masked_text.replace(match, '**** **** ' + aadhaar_number[-4:])
        # print(aadhaar_numbers)
        if len(aadhaar_numbers)==0:
            # image = Image.open(os.path.join(dest_folder, filename))
            # image.save(os.path.join(unmasked, filename))
            title = texts[0].description
            # print(title)
            new = title.split()
            # print(new)
            new = [i.lower() for i in new]
            if "आधार" in new  or "ఆధార్" in new or "আধাৰ" in new or "આધાર" in new or "ಆಧಾರ" in new or "ആധാർ" in new or "अधर" in new or "ஆதார்" in new or "aadhar" in new or "aadhaar" in new:
                if "vid" in new or "vid:" in new or "unique" in new or "authenticate" in new or "enrollment" in new:
                    image = Image.open(os.path.join(dest_folder, filename))
                    image.save(os.path.join(output_folder, filename))  
                else:
                    image = Image.open(os.path.join(dest_folder, filename))
                    image.save(os.path.join(unmasked, filename))   
                    print("No aadhar found")
            else:
                image = Image.open(os.path.join(dest_folder, filename))
                image.save(os.path.join(unmasked, filename))   
                print("No aadhar found")
        else:
            final=[]
            for item in aadhaar_numbers:
                final.append(item.split())

            def flatten(lst):
                result = []
                for item in lst:
                    if isinstance(item, list):
                        result.extend(flatten(item))
                    else:
                        result.append(item)
                return result

            flatten_list=flatten(final)
            boxes=[]
            for text in texts:
            # print(text)
                for element in flatten_list:
                    if text.description==element:
                        boxes.append(text)

            with Image.open(os.path.join(dest_folder, filename)) as im:
                draw = ImageDraw.Draw(im)
                for text in boxes:
                    vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
                    draw.polygon(vertices, outline='red',fill=(255, 255, 255, 255))
                im.save(r"F:\\my code\\vision api\\output\\"+str(filename))