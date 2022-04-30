import requests
from helpers.fivesim import FiveSim 
from helpers.name import ArabicName
from helpers.google import Google
from helpers.scraper import Scraper
from helpers.user import randomize, generate_user_info
from helpers.csv import export_to_csv

if __name__ == '__main__':
    sim = FiveSim()
    providers = sim.get_best_providers()
    phone_info = sim.purchase_a_number(providers)
    
    name = ArabicName()
    arabic_name = name.generate_a_name()
    user = generate_user_info(arabic_name)

    mail = Google()
    mail.create_new_gmail(user, phone_info)

    export_to_csv(user, phone_info)