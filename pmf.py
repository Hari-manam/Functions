def dice_pmf():
    return {i: 1/6 for i in range(1, 7)}

print(dice_pmf())

def dice_cmf():
    return {i: i/6 for i in range(1, 7)}

print(dice_cmf())

def dice_pdf():
    return {i: 1/6 for i in range(1, 7)}

print(dice_pdf())