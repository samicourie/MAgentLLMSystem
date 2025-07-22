import io
import base64
import xml.etree.ElementTree as ET


# Convert PIL image to base64 string
def convert_image_to_base64(img_obj):
    buffer = io.BytesIO()
    img_obj.save(buffer, format='JPEG')
    base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return base64_str


# Split an image with bounding box and a bit of margin
def split_image(image_obj, x_start, x_end, y_start, y_end, margin=0.05):
    width, height = image_obj.size

    part_x_start = int(max(0, x_start-margin) * width)
    part_x_end = int(min(x_end+margin, 1) * width)
    part_y_start = int(max(y_start-margin, 0) * height)
    part_y_end = int(min(y_end+margin, 1) * height)

    box = (part_x_start, part_y_start, part_x_end, part_y_end)
    cropped_part = image_obj.crop(box)
    return cropped_part


# Parse XML Response and return a JSON object of it
def parse_llm_response(xml_string):
    root = ET.fromstring(xml_string.strip())
    result = {}

    for child in root:
        category = child.tag
        prediction = child.find('prediction').text
        confidence = float(child.find('confidence').text)
        result[category] = {
            'prediction': prediction,
            'confidence': confidence
        }

    return result
