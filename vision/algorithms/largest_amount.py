from vision.constants import CASH_FIELDS


def find_largest_amount(lines, index):
    # check for the presence of the word "cash". When a person pays by
    # cash, they usually make a payment that is equal to or more the total.
    # This will be useful so we don't pick the largest amount, but the second
    # largest amount
    cash_used = False
    for line in lines:
        for word in line:
            if word.text.upper() in CASH_FIELDS:
                cash_used = True

    # The most important part of the receipt of the total.
    # If we could not find it, try a weaker alterative

    # scan the document for the highest money amount
    amounts = []
    for line in lines[index:]:
        for word in line:
            if word.is_money():
                amounts.append(word)

    if amounts:
        amounts = list(filter(lambda x: x.numeric_money_amount() is not None, amounts))
        amounts.sort(key=lambda x: x.numeric_money_amount(), reverse=True)
        if cash_used and len(amounts) > 1:
            return amounts[1]

        return amounts[0]

    return None
