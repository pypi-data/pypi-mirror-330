import pdfplumber
import re

# Dictionary for base numbers
somali_numbers = {
    1: "hal", 2: "laba", 3: "saddex", 4: "afar", 5: "shan",
    6: "lix", 7: "toddoba", 8: "sideed", 9: "sagaal", 10: "toban",
    11: "kow iyo toban", 12: "toban iyo laba", 13: "toban iyo saddex",
    14: "toban iyo afar", 15: "toban iyo shan", 16: "toban iyo lix",
    17: "toban iyo toddoba", 18: "toban iyo sideed", 19: "toban iyo sagaal",
    20: "labaatan", 30: "soddon", 40: "afartan", 50: "konton",
    60: "lixdan", 70: "todobaatan", 80: "sideetan", 90: "sagaashan",
    100: "boqol", 1000: "kun", 1000000: "malyan", 1000000000: "bilyan"
}

def number_to_somali(number):
    if number in somali_numbers:
        return somali_numbers[number]
    
    # Handle numbers between 21-99
    if number < 100:
        tens = (number // 10) * 10
        ones = number % 10
        return somali_numbers[tens] + (" iyo " + somali_numbers[ones] if ones else "")

    # Handle numbers between 100-999 (Fixes "kow boqol" issue)
    if number < 1000:
        hundreds = number // 100
        remainder = number % 100
        if hundreds == 1:
            return "boqol" + (" " + number_to_somali(remainder) if remainder else "")
        else:
            return somali_numbers[hundreds] + " boqol" + (" iyo " + number_to_somali(remainder) if remainder else "")

    # Handle numbers between 1,000-999,999 (Fixes "hal kun" issue)
    if number < 1000000:
        thousands = number // 1000
        remainder = number % 1000
        if thousands == 1:
            return "kun" + ("  " + number_to_somali(remainder) if remainder else "")
        else:
            return number_to_somali(thousands) + " kun" + (" iyo " + number_to_somali(remainder) if remainder else "")

    # Handle millions (1,000,000 - 999,999,999)
    if number < 1000000000:
        millions = number // 1000000
        remainder = number % 1000000
        return number_to_somali(millions) + " malyan" + (" iyo " + number_to_somali(remainder) if remainder else "")

    # Handle billions (1,000,000,000+)
    billions = number // 1000000000
    remainder = number % 1000000000
    return number_to_somali(billions) + " bilyan" + (" iyo " + number_to_somali(remainder) if remainder else "")

def replace_numbers_with_somali(text):
    if not text:
        return text
    
    # Find all numbers in the text
    numbers = re.findall(r'\d+', text)

    # Replace each number with its Somali equivalent
    for num in numbers:
        somali_word = number_to_somali(int(num))
        text = text.replace(num, somali_word)

    return text

def process_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # Replace numbers in the text
    processed_text = replace_numbers_with_somali(text)

    return processed_text
