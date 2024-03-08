from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass, field
import json
import os

with open("careers.json") as f:
    content = f.read()
    data = json.loads(content)

career_data = data["careers"]["careerData"]
# Example of Career Data
# career_data = [
#     {
#         "title": "Police Officer",
#         "salary": 3000,
#         "taxes": 580,
#         "mortgagePayment": 400,
#         "schoolLoanPayment": 0,
#         "carLoanPayment": 100,
#         "creditCardPayment": 60,
#         "retailPayment": 50,
#         "otherExpenses": 690,
#         "savings": 520,
#         "childPerExpense": 160,
#         "mortgageLiability": 46000,
#         "schoolLoanLiability": 0,
#         "carLoanLiability": 5000,
#         "creditCardLiability": 2000,
#         "retailDebtLiability": 1000
#     },
#     {
#         "title": "Lawyer",
#         "salary": 7500,
#         "taxes": 1830,
#         "mortgagePayment": 1100,
#         "schoolLoanPayment": 390,
#         "carLoanPayment": 220,
#         "creditCardPayment": 180,
#         "retailPayment": 50,
#         "otherExpenses": 1650,
#         "savings": 400,
#         "childPerExpense": 380,
#         "mortgageLiability": 115000,
#         "schoolLoanLiability": 78000,
#         "carLoanLiability": 11000,
#         "creditCardLiability": 6000,
#         "retailDebtLiability": 1000
#     }
# ]

@dataclass
class Career:
    title: str
    salary: int
    taxes: int
    mortgagePayment: int
    schoolLoanPayment: int
    carLoanPayment: int
    creditCardPayment: int
    retailPayment: int
    otherExpenses: int
    savings: int
    childPerExpense: int
    mortgageLiability: int
    schoolLoanLiability: int
    carLoanLiability: int
    creditCardLiability: int
    retailDebtLiability: int

    @property
    def liability(self) -> int:
        return (
            self.mortgageLiability +
            self.schoolLoanLiability +
            self.carLoanLiability +
            self.creditCardLiability +
            self.retailDebtLiability
        )
    
    @property
    def expenses(self) -> int:
        return (
            self.taxes +
            self.mortgagePayment + 
            self.schoolLoanPayment +
            self.carLoanPayment + 
            self.creditCardPayment +
            self.retailPayment +
            self.otherExpenses
        )
    @property
    def payDay(self) -> int:
        return self.salary - self.expenses

    @property
    def id_name(self) -> str:
        return self.title.replace(' ', '_')

def create_career_card(career: Career, template_path: str):
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    avatar_path = f'avatars/{career.id_name}.png'
    if not os.path.exists(avatar_path):
        avatar_path = f'avatars/default_career.png'
    avatar = Image.open(avatar_path)
    avatar = avatar.resize((50, 50), Image.ANTIALIAS)
    white_background = Image.new("RGB", avatar.size, "white")
    alpha_mask = avatar.getchannel('A')
    avatar = Image.composite(avatar, white_background, alpha_mask)

    image.paste(avatar, (175, 95))

    heading_font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", size=24)
    font1 = ImageFont.truetype("./fonts/Roboto-Bold.ttf", size=28)
    font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", size=12)

    current_h = 10
    current_h += 40

    fields = [
        'title',
        'salary',
        'childPerExpense',
        'expenses',
        'liability',
        'savings',
        'payDay'
    ]

    for key in fields:
        value = career.__getattribute__(key)
        if key == 'title':
            text_font = heading_font
            text = value
            text_size = draw.textsize(text, font=text_font)
            x_position = (400 - text_size[0]) / 2
            position = (x_position, 40)
            text_color = "black"
        elif key == 'salary':
            text_font = font1
            text = f"${value:,.0f}"
            text_size = draw.textsize(text, font=text_font)
            x_position = (165 - text_size[0]) / 2
            position = (x_position, 215)
            text_color = "white"
        elif key == 'expenses':
            text_font = font1
            text = f"${value:,.0f}"
            text_size = draw.textsize(text, font=text_font)
            x_position = (400 - text_size[0]) / 2
            position = (x_position, 215)
            text_color = "white"
        elif key == 'payDay':
            text_font = font1
            text = f"${value:,.0f}"
            text_size = draw.textsize(text, font=text_font)
            x_position = (625 - text_size[0]) / 2
            position = (x_position, 215)
            text_color = "white"
        elif key == 'liability':
            text_font = font1
            text = f"${value:,.0f}"
            text_size = draw.textsize(text, font=text_font)
            x_position = (270 - text_size[0]) / 2
            position = (x_position, 320)
            text_color = "white"
        elif key == 'savings':
            text_font = font1
            text = f"${value:,.0f}"
            text_size = draw.textsize(text, font=text_font)
            x_position = (625 - text_size[0]) / 2
            position = (x_position, 320)
            text_color = "white"
        elif key == 'childPerExpense':
            text_font = font1
            text = f"${value:,.0f}"
            text_size = draw.textsize(text, font=text_font)
            x_position = (400 - text_size[0]) / 2
            position = (x_position, 435)
            text_color = "white"
        else:
            text_font = font
            text = f"{key}: ${value}"
            position = (10, current_h)
            text_color = "black"
        draw.text(position, text, font=text_font, fill=text_color)
        current_h += 30
    return image
template_path = "/Users/anhv/Downloads/career_template.png"
saved_image_paths = []

for career in career_data:
    profession = career["title"]  # Extracting the title of the profession
    card_image = create_career_card(Career(**career), template_path)
    image_path = f"careers/{profession.replace(' ', '_')}_card.png"
    card_image.save(image_path)
    saved_image_paths.append(image_path)

# Print or return the paths of the saved images
print(saved_image_paths)