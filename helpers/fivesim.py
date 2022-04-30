import requests
import time
from heapq import nsmallest

class FiveSim:
    def  __init__(self):
        self.token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODI1MDE0MTcsImlhdCI6MTY1MDk2NTQxNywicmF5IjoiOGM0Y2Q4MTMyMGI3ZTNjOTc4MzM1YWE1MGNlMDc0ZTQiLCJzdWIiOjEwNTQxODl9.GDbD0leE6_W12khX1nZWpDtDvwtS_-dcXjv2-gIJk6EvRUjkT2Ji8we-m_tmp6_nhSvNP3wYgp982EJzKUhMPBYAlm5BiLjXS7QlNfo7GbFdbLDslysoGPFmceD8pbcRdq7ClvP91JvKEySemM0YnXQIpPDV3P9rISn2esF-ottTv4yaJDCaf7rarzGqG3e1yio_KoWheJfY_OIMOrQ9aLnDRUtrPkubimPcMvc6CdbTz1vcGz6LzQHnFtJvGDmdfmSdSMYCqNSRF-80HRTjznFvqE0YeBoPfzEVmebdU4JDtS_eop0L6pX6HWnyxHOnVJrx2ZSrwhikFHmqDELAiQ'
        self.api_key = '67537d4ff404477dbff846ae5b491ba5'
        self.product = 'google'
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/json',
        }

    def get_best_providers(self, provider_count = 3):
        print(f'[5sim number searching] for: {self.product}')
        params = (
            ('product', self.product),
        )
        response = requests.get('https://5sim.net/v1/guest/prices', params=params)
        data = response.json()
        data = data[self.product]
        print(f'[5sim number searching] analyzing {len(data.keys())} country')
        reference = {
            'country': '',
            'operator': {
                'title': '',
                'cost': 1000,
                'count': 0
            }
        }
        providers = []
        for country_name in list(data.keys()):
            operator_names = list(data[country_name].keys())
            for operator_name in operator_names:
                operator = data[country_name][operator_name]
                if operator['count'] != 0:
                    if operator['cost'] < reference['operator']['cost']:
                        reference['country'] = country_name
                        reference['cost'] = operator['cost']
                        reference['operator'] = {
                            'title': operator_name,
                            'cost': operator['cost'],
                            'count': operator['count']
                        }
                        providers.append(reference)
        cheapest_providers = []
        for i in range(provider_count):
            count = len(providers)-(i+1)
            cheapest_providers.append(providers[count])
        print(f'[5sim number searching] {provider_count} cheapest providers: {cheapest_providers}')
        return cheapest_providers
    
    def purchase_a_number(self, providers):
        for idx, provider in enumerate(providers):
            print(f'[5sim purchasing number] attempting to purchase {idx+1}th number')
            try:
                res = requests.get('https://5sim.net/v1/user/buy/activation/' + provider['country'] + '/' + provider['operator']['title'] + '/' + self.product, headers=self.headers)
                phone = res.json()
                number = phone['phone']
                status = phone['status']
                print(f'[5sim purchasing number] {number} {status}')   
                break 
            except:
                print(f'[5sim purchasing number] {idx+1}th number is not available to purchase')
                continue
        return phone

    def get_otp(self, id):
        response = requests.get('https://5sim.net/v1/user/check/' + str(id), headers=self.headers)
        response = response.json()
        sms_list = response['sms']
        loop = 0
        otp = False

        while True:
            if response['status'] == 'RECEIVED':
                if len(sms_list) <= 0:
                    print('[checking 5sim inbox] No SMS received yet')
                    print('[checking 5sim inbox] Waiting 20 seconds')
                    time.sleep(20)
                    try:
                        print('[checking 5sim inbox] Checking inbox once again')
                        response = requests.get('https://5sim.net/v1/user/check/' + str(id), headers=self.headers)
                        response = response.json()
                        loop += 1
                        continue
                    except: 
                        print('[checking 5sim inbox] 5sim closed API connection')
                        print('Pleas run this script again')
                        break
                else:
                    print('[checking 5sim inbox] SMS received')
                    otp = sms_list[0]['code']
                    print(f'[checking 5sim inbox] OTP is {otp}')
                    break
            else:
                print('[checking 5sim inbox] Sim expiration: timeout')
                print('[checking 5sim inbox] Need to buy another sim')
                otp = response
                break
        return otp
  