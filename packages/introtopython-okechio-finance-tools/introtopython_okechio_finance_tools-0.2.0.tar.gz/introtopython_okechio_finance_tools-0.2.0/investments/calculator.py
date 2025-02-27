def calculate_roi(initial: int, final: int):
    return(final - initial)/ initial

def project_growth(initial, growth_rate, years):
    return initial * (1 + growth_rate) ** years

#underscore before a variable name means for developers not to mess with the variable. That is, it's kinda a secret variable
_my_secret_variable = 58