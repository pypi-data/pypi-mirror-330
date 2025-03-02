# currency_to_words/__init__.py

from utils.methods import convert_two_digits, convert_three_digits

def convert_currency_to_words(amount, case_type='title'):
    """Convert a numeric amount to words (Indian numbering system) with case handling"""

    def num_to_words(n):
        """Convert a number to words for Indian currency system"""
        if n == 0:
            return "Zero"

        crore = n // 10000000
        n %= 10000000

        lakh = n // 100000
        n %= 100000

        thousand = n // 1000
        n %= 1000

        hundred = n

        words = []
        if crore > 0:
            words.append(convert_two_digits(crore) + " Crore")
        if lakh > 0:
            words.append(convert_two_digits(lakh) + " Lakh")
        if thousand > 0:
            words.append(convert_two_digits(thousand) + " Thousand")
        if hundred > 0:
            words.append(convert_three_digits(hundred))

        return ' '.join(words).strip()

    rupees = int(amount)
    paise = round((amount - rupees) * 100)

    rupees_in_words = num_to_words(rupees)

    if paise > 0:
        paise_in_words = num_to_words(paise)
        result = f"{rupees_in_words} Rupees and {paise_in_words} Paise"
    else:
        result = f"{rupees_in_words} Rupees"

    # Apply the case transformation based on the case_type parameter
    if case_type == 'uppercase':
        result = result.upper()  # Convert all text to uppercase
    elif case_type == 'lowercase':
        result = result.lower()  # Convert all text to lowercase
    elif case_type == 'title':
        result = result.title()  # Capitalize the first letter of each word
    elif case_type == 'capitalize':
        result = result.capitalize()  # Capitalize the first letter of the first word
    elif case_type == 'sentence':
        result = result[0].upper() + result[1:].lower()  # Sentence case (capitalize the first letter only)
    elif case_type == 'alternating':
        result = ''.join([char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(result)])  # Alternating case
    elif case_type == 'upper_camel':
        result = ' '.join([word.capitalize() for word in result.split()])  # Upper Camel Case (Pascal Case)
    elif case_type == 'lower_camel':
        words = result.split()
        result = words[0].lower() + ' '.join([word.capitalize() for word in words[1:]])  # Lower Camel Case

    return result