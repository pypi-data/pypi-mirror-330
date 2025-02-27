def compound_interest(principal, rate, years):
    return principal * (1 + rate) ** years

def investment_return(principal, rate, years):
    return compound_interest(principal, rate, years)