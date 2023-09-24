import allocation
import numpy as np
import pandas as pd

MEAN_COL = 3018

def monthly_deposit_withdraw(user):
    monthly_withdraw = MEAN_COL + 250 *np.random.standard_normal()
    monthly_deposit = user["Salary"]/12
    return monthly_withdraw, monthly_deposit

def compound_allocate(balance, user):
    
    monthly_withdraw, monthly_deposit = monthly_deposit_withdraw(user)
    allocation.balance["Liquid"] -= monthly_withdraw
    allocation.allocate(allocation.balance, monthly_deposit, user)

    return allocation.balance