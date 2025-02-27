import json
import xml.etree.ElementTree as ET
from enum import Enum
from io import BytesIO
from typing import List, Optional

import PIL
import matplotlib.font_manager
from PIL import ImageFont, ImageDraw, Image
from PyPDF2 import PdfMerger
from cairosvg import svg2pdf
from pydantic import BaseModel

from .. import SwitchAI


class Font(Enum):
    HELVETICA = "Helvetica"
    DM_SERIF_TEXT = "DM Serif Text"
    POPPINS = "Poppins"
    OPEN_SANS = "Open Sans"
    INTER = "Inter"
    INDIE_FLOWER = "Indie Flower"


class Size(Enum):
    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"


class Color(Enum):
    GRAY_0 = "#F8F9FA"
    GRAY_3 = "#DEE2E6"
    GRAY_6 = "#868E96"
    GRAY_9 = "#212529"

    RED_0 = "#FFF5F5"
    RED_3 = "#FFA8A8"
    RED_6 = "#FA5252"
    RED_9 = "#C92A2A"

    PINK_0 = "#FFF0F6"
    PINK_3 = "#FAA2C1"
    PINK_6 = "#E64980"
    PINK_9 = "#A61E4D"

    GRAPE_0 = "#F8F0FC"
    GRAPE_3 = "#E599F7"
    GRAPE_6 = "#BE4BDB"
    GRAPE_9 = "#862E9C"

    VIOLET_0 = "#F3F0FF"
    VIOLET_3 = "#B197FC"
    VIOLET_6 = "#7950F2"
    VIOLET_9 = "#5F3DC4"

    INDIGO_0 = "#EDF2FF"
    INDIGO_3 = "#91A7FF"
    INDIGO_6 = "#4C6EF5"
    INDIGO_9 = "#364FC7"

    BLUE_0 = "#E7F5FF"
    BLUE_3 = "#74C0FC"
    BLUE_6 = "#228BE6"
    BLUE_9 = "#1864AB"

    CYAN_0 = "#E3FAFC"
    CYAN_3 = "#66D9E8"
    CYAN_6 = "#15AABF"
    CYAN_9 = "#0B7285"

    TEAL_0 = "#E6FCF5"
    TEAL_3 = "#63E6BE"
    TEAL_6 = "#12B886"
    TEAL_9 = "#087F5B"

    GREEN_0 = "#EBFBEE"
    GREEN_3 = "#8CE99A"
    GREEN_6 = "#40C057"
    GREEN_9 = "#2B8A3E"

    LIME_0 = "#F4FCE3"
    LIME_3 = "#C0EB75"
    LIME_6 = "#82C91E"
    LIME_9 = "#5C940D"

    YELLOW_0 = "#FFF9DB"
    YELLOW_3 = "#FFE066"
    YELLOW_6 = "#FAB005"
    YELLOW_9 = "#E67700"

    ORANGE_0 = "#FFF4E6"
    ORANGE_3 = "#FFC078"
    ORANGE_6 = "#FD7E14"
    ORANGE_9 = "#D9480F"


class Position(Enum):
    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"


class Image(BaseModel):
    description: str
    position: Position


class Text(BaseModel):
    value: str
    font: Font
    color: Color
    size: Size
    position: Position
    bold: bool


class Slide(BaseModel):
    background_color: Color
    text: Text
    sub_text: Optional[Text]
    image: Optional[Image]


class SlidesModel(BaseModel):
    slides: List[Slide]


class SlideMaker:
    def __init__(self, chat_client: SwitchAI, image_generation_client: SwitchAI):
        self.chat_client = chat_client
        self.image_generation_client = image_generation_client

    def generate_slides(self, description: str, output_path: str = None):
        # response = self.chat_client.chat(
        #     messages=[{"role": "user", "content": description}], response_format=SlidesModel
        # )
        # json_content = json.loads(response.choices[0].message.content)
        # print(json_content)

        json_content = {
            "slides": [
                {
                    "background_color": "#212529",
                    "text": {
                        "value": "The History of the Internet",
                        "font": "DM Serif Text",
                        "color": "#EDF2FF",
                        "size": "xl",
                        "position": "center",
                        "bold": True,
                    },
                    "sub_text": None,
                    "image": None,
                },
                {
                    "background_color": "#F8F9FA",
                    "text": {
                        "value": "The Early Beginnings (1960s - 1980s)",
                        "font": "Open Sans",
                        "color": "#212529",
                        "size": "lg",
                        "position": "top_left",
                        "bold": True,
                    },
                    "sub_text": {
                        "value": '💡 Concept: Ideas of a "galactic network" came to life in the 1960s.\n🔗 ARPANET: The first operational packet-switching network introduced in 1969.\n🎓 Academia: Early internet primarily connected scientific and military institutions.',
                        "font": "Open Sans",
                        "color": "#868E96",
                        "size": "md",
                        "position": "center",
                        "bold": False,
                    },
                    "image": None,
                },
                {
                    "background_color": "#212529",
                    "text": {
                        "value": "The World Wide Web (1990s)",
                        "font": "Poppins",
                        "color": "#EDF2FF",
                        "size": "lg",
                        "position": "top_left",
                        "bold": True,
                    },
                    "sub_text": {
                        "value": "🌐 Invention: Tim Berners-Lee created the World Wide Web in 1989.\n🖥️ Browsers: Mosaic became the first popular graphical web browser in 1993.\n🌍 Boom: Rapid growth in websites and users during the late '90s.",
                        "font": "Poppins",
                        "color": "#DEE2E6",
                        "size": "md",
                        "position": "center",
                        "bold": False,
                    },
                    "image": {"description": "A mosaic-inspired web browser interface", "position": "bottom_right"},
                },
                {
                    "background_color": "#F8F9FA",
                    "text": {
                        "value": "The Dot-com Era (Late 1990s - early 2000s)",
                        "font": "Open Sans",
                        "color": "#212529",
                        "size": "lg",
                        "position": "top_left",
                        "bold": True,
                    },
                    "sub_text": {
                        "value": "💥 Boom: Surge in technology and internet businesses.\n📉 Bust: The dot-com bubble burst in the early 2000s, causing many companies to fail.\n🖲️ Survivors: Giants like Amazon and eBay emerged stronger.",
                        "font": "Open Sans",
                        "color": "#868E96",
                        "size": "md",
                        "position": "center",
                        "bold": False,
                    },
                    "image": None,
                },
                {
                    "background_color": "#212529",
                    "text": {
                        "value": "The Rise of Social Media and Mobile Internet (2000s)",
                        "font": "Poppins",
                        "color": "#EDF2FF",
                        "size": "lg",
                        "position": "top_left",
                        "bold": True,
                    },
                    "sub_text": {
                        "value": "📱 Mobility: Smartphones made internet access more personal and portable.\n🌐 Social Platforms: Facebook, Twitter, and other platforms redefined the web.\n🔝 Flashpoint: These platforms accelerated user interactivity and content sharing.",
                        "font": "Poppins",
                        "color": "#DEE2E6",
                        "size": "md",
                        "position": "center",
                        "bold": False,
                    },
                    "image": {
                        "description": "A hand holding a smartphone displaying popular social media icons",
                        "position": "bottom_right",
                    },
                },
                {
                    "background_color": "#F8F9FA",
                    "text": {
                        "value": "Towards a Connected Future (2010s - Present)",
                        "font": "Open Sans",
                        "color": "#212529",
                        "size": "lg",
                        "position": "top_left",
                        "bold": True,
                    },
                    "sub_text": {
                        "value": "🔗 IoT: Internet of Things seamlessly connects daily objects.\n☁️ Cloud Computing: Revolutionizes data storage and accessibility.\n📈 Growth: The internet's reach and impact continues to expand globally.",
                        "font": "Open Sans",
                        "color": "#868E96",
                        "size": "md",
                        "position": "center",
                        "bold": False,
                    },
                    "image": None,
                },
                {
                    "background_color": "#212529",
                    "text": {
                        "value": "Thank You!",
                        "font": "DM Serif Text",
                        "color": "#EDF2FF",
                        "size": "xl",
                        "position": "center",
                        "bold": True,
                    },
                    "sub_text": None,
                    "image": None,
                },
            ]
        }

        self.create_pdf(json_content, output_path)

    def create_pdf(self, json_content, output_path):
        if output_path is None:
            output_path = "slides.pdf"

        pdf_pages = []
        for slide in json_content["slides"]:
            svg_page = self.render_slide(slide)
            pdf_buffer = BytesIO()
            svg2pdf(bytestring=svg_page.encode("utf-8"), write_to=pdf_buffer)
            pdf_buffer.seek(0)
            pdf_pages.append(pdf_buffer)

        merger = PdfMerger()
        for pdf_page in pdf_pages:
            merger.append(pdf_page)

        with open(output_path, "wb") as f:
            merger.write(f)

        for pdf_page in pdf_pages:
            pdf_page.close()

    def render_slide(self, slide):
        page = f"""<svg width="1920" height="1080" viewBox="0 0 1920 1080" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="1920" height="1080" fill="{slide["background_color"]}"/>
                   </svg>"""

        root = ET.fromstring(page)
        ET.register_namespace("", "http://www.w3.org/2000/svg")

        text = slide["text"]
        last_y = self.add_text_element(
            root,
            text["value"],
            Position(text["position"]),
            96,
            text["font"],
            text["color"],
            margin=64,
            bold=text["bold"],
        )

        if slide["sub_text"]:
            sub_text = slide["sub_text"]
            last_y = self.add_text_element(
                root,
                sub_text["value"],
                Position(sub_text["position"]),
                48,
                sub_text["font"],
                sub_text["color"],
                margin=64,
                bold=sub_text["bold"],
                last_y=last_y,
            )

        page = ET.tostring(root).decode()
        return page

    def add_text_element(
        self,
        rt,
        text,
        position,
        font_size,
        font,
        fill,
        margin=0,
        bold=False,
        max_width=1920,
        max_height=1080,
        last_y=0,
    ):
        text_width, text_height = self.get_text_bbox(text, font, font_size)

        if max_width != 1920:
            if text_width > max_width - margin:
                wrapped_text = self.wrap_text(text, font, font_size, max_width - margin)
            else:
                wrapped_text = [text]
        else:
            if text_width > max_width - 2 * margin:
                wrapped_text = self.wrap_text(text, font, font_size, max_width - 2 * margin)
            else:
                wrapped_text = [text]

        x, y = 0, last_y
        if position == Position.TOP_LEFT:
            x, y = margin, text_height + margin + last_y
        elif position == Position.CENTER:
            x = (max_width - min(text_width, max_width)) / 2

            total_text_height = (len(wrapped_text) - 1) * text_height
            y = (max_height - total_text_height) / 2

            if len(wrapped_text) == 1:
                y += text_height / 2
        else:
            print("Position not supported.")

        for line in wrapped_text:
            element = ET.Element(
                "text",
                attrib={
                    "x": str(x),
                    "y": str(y),
                    "font-size": str(font_size),
                    "font-family": font,
                    "fill": fill,
                    "font-weight": "bold" if bold else "normal",
                },
            )
            element.text = line
            rt.append(element)

            y += text_height * 1.2

        return y

    def resize_and_crop(self, img, target_size):
        target_width, target_height = target_size
        img_aspect = img.width / img.height
        target_aspect = target_width / target_height

        if img_aspect > target_aspect:
            new_height = target_height
            new_width = int(new_height * img_aspect)
        else:
            new_width = target_width
            new_height = int(new_width / img_aspect)

        img = img.resize((new_width, new_height))

        left = (new_width - target_width) / 2
        top = (new_height - target_height) / 2
        right = left + target_width
        bottom = top + target_height

        img = img.crop((left, top, right, bottom))

        return img

    def get_font_path(self, target_font_name):
        font_paths = matplotlib.font_manager.findSystemFonts(fontext="ttf")

        for path in font_paths:
            try:
                font_name = matplotlib.font_manager.FontProperties(fname=path).get_name()
                if font_name.lower() in target_font_name.lower():
                    return path
            except RuntimeError:
                pass
        return None

    def wrap_text(self, text, font, font_size, max_width):
        lines = []
        words = text.split(" ")
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + " " + word
            test_width, _ = self.get_text_bbox(test_line, font, font_size)
            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        return lines

    def get_text_bbox(self, text, font, font_size):
        font_path = self.get_font_path(font)

        if font_path:
            font = ImageFont.truetype(font_path, size=font_size)
        else:
            font = ImageFont.load_default(size=font_size)

        dummy_image = PIL.Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(dummy_image)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        return text_width, text_height
