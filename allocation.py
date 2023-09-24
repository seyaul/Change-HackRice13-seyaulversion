import numpy as np


balance = {"Liquid": 0, "ST Fixed Income": 0, "LT Fixed Income": 0, "ETF": 0, "Tech": 0, "CurrRetirement": 0}


user = {"Salary": None, "Age": None, "Plan": 'Default'}

deposit = 0


young_default = np.array([0, 10, 20, 70])
mid_age_default = np.array([0, 25, 35, 40])
old_default = np.array([80, 0, 20, 0])
to_interpolate = [young_default, mid_age_default, old_default]
ages = [18,42,65]


high_risk_LT = np.array([0, 10, 20, 70])/100
high_risk_ST = np.array([50, 0, 0, 50])/100
low_risk_LT = np.array([0, 70, 25, 5])/100
low_risk_ST = np.array([80, 0, 20, 0])/100
   
def interpolate_plan(vectors, positions, target_position):
    # Find the two nearest positions to the target position
    idx = np.searchsorted(positions, target_position, side="right")
    left_position = positions[idx - 1]
    right_position = positions[idx]


    # Calculate the interpolation weight
    weight = (target_position - left_position) / (right_position - left_position)


    # Interpolate between the vectors
    interpolated_vector = (
        (1 - weight) * vectors[idx - 1] + weight * vectors[idx]
    )


    return interpolated_vector

def allocate(balance, deposit, user):
    if balance["Liquid"] < user["Salary"] / 2:
        needed = user["Salary"] / 2 - balance["Liquid"]
        if deposit < needed:
            balance["Liquid"] += deposit
            return balance
        else:
            balance["Liquid"] += needed
            deposit -= needed


    if balance["CurrRetirement"] < 21500:
        if deposit < 21500 - balance["CurrRetirement"]:
            balance["CurrRetirement"] += deposit
            return balance
        else:
            deposit -= (21500 - balance["CurrRetirement"])
            balance["CurrRetirement"] = 21500
    if(user["Plan"] == "Default"):    
        interpolated_plan = interpolate_plan(to_interpolate, ages, user["Age"]) / 100
        balance["ST Fixed Income"] += interpolated_plan[0]*deposit
        balance["LT Fixed Income"] += interpolated_plan[1]*deposit
        balance["ETF"] += interpolated_plan[2]*deposit
        balance["Tech"] += interpolated_plan[3]*deposit


        return balance
   
    if(user["Plan"] == "High Risk Long Term"):
        balance["ST Fixed Income"] += high_risk_LT[0]*deposit
        balance["LT Fixed Income"] += high_risk_LT[1]*deposit
        balance["ETF"] += high_risk_LT[2]*deposit
        balance["Tech"] += high_risk_LT[3]*deposit
   
    elif(user["Plan"] == "Low Risk Long Term"):
        balance["ST Fixed Income"] += low_risk_LT[0]*deposit
        balance["LT Fixed Income"] += low_risk_LT[1]*deposit
        balance["ETF"] += low_risk_LT[2]*deposit
        balance["Tech"] += low_risk_LT[3]*deposit


    elif(user["Plan"] == "High Risk Short Term"):
        balance["ST Fixed Income"] += high_risk_ST[0]*deposit
        balance["LT Fixed Income"] += high_risk_ST[1]*deposit
        balance["ETF"] += high_risk_ST[2]*deposit
        balance["Tech"] += high_risk_ST[3]*deposit


    elif(user["Plan"] == "Low Risk Short Term"):
        balance["ST Fixed Income"] += low_risk_ST[0]*deposit
        balance["LT Fixed Income"] += low_risk_ST[1]*deposit
        balance["ETF"] += low_risk_ST[2]*deposit
        balance["Tech"] += low_risk_ST[3]*deposit


    return balance