from helpers.scraper import Scraper
from helpers.fivesim import FiveSim
import time
from helpers.user import generate_user_info, randomize

class Google:
    def __init__(self):
        self.url = 'https://accounts.google.com/signup/v2/webcreateaccount?service=youtube&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den-GB%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en-GB&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp&nogm=true'

    def create_new_gmail(self, user, phone_info):
        scraper = Scraper(self.url)
        scraper.element_click_by_xpath("//button[contains(text(), 'Create a new Gmail address instead')]")
        print('[Google form] clicked: "Create a new Gmail address instead" button')
        scraper.element_send_keys('input[id=firstName]', user['firstname'])
        print('[Google form] first name: filling up')
        scraper.element_send_keys('input[id=lastName]', user['lastname'])
        print('[Google form] second name: filling up')
        scraper.element_send_keys('input[id=username]', user['username'])
        print('[Google form] username: filling up')
        scraper.element_click('input[name=Passwd]')
        time.sleep(2)
        page_source = scraper.driver.page_source
        search_text = "That username is taken"
        print('[Google form] username name: checking availability')
        while search_text in page_source:
            try:
                print('[Google form] username: Not available, trying a new one')
                username = str.lower(randomize('-l',10)) + randomize('-n',4)
                user['username'] = username
                scraper.element_clear('input[id=username]')
                scraper.element_send_keys('input[id=username]', user['username'])
                scraper.element_click('input[name=Passwd]')
                time.sleep(2)
                page_source = scraper.driver.page_source
                continue
            except: 
                print('[Google form] username: available to use')    
                break
        print('[Google form] password: filling up')
        scraper.element_send_keys('input[name=Passwd]', user['password'])
        print('[Google form] confirm password: filling up')
        scraper.element_send_keys('input[name=ConfirmPasswd]', user['password'])
        print('[Google form] going next page')
        scraper.element_click_by_xpath("//button[contains(text(),'Next')]")
        print('[Google form] phone: filling up')        
        scraper.element_send_keys('input[type=tel]', phone_info['phone'])
        print('[Google form] going next page')
        scraper.element_click_by_xpath("//button[contains(text(),'Next')]")
        time.sleep(5)

        sim = FiveSim()
        otp = sim.get_otp(phone_info['id'])

        if type(otp) == dict:
            exit()
        if type(otp) == str:
            print('[Google form] OTP: filling up')
            scraper.element_send_keys('input[type=tel]', otp)
            print('[Google form] OTP: Verifying')
            scraper.element_click_by_xpath("//button[contains(text(),'Verify')]")
            
        print('[Google form] birth day: filling up')
        scraper.element_send_keys('input[id=day]', user['dob']['day'])
        print('[Google form] birth month: filling up')
        scraper.select_dropdown('select[id=month]', user['dob']['month'])
        print('[Google form] birth year: filling up')
        scraper.element_send_keys('input[id=day]', user['dob']['year'])
        print('[Google form] gender: filling up')
        scraper.select_dropdown('select[id=gender]', user['gender'])
        print('[Google form] going next page')
        scraper.element_click_by_xpath("//button[contains(text(),'Next')]")
        print('[Google form] skipping additional phone settings for now')
        scraper.element_click_by_xpath("//button[contains(text(),'Skip')]")
        print('[Google form] Accepting terms & conditions')
        scraper.element_click_by_xpath("//button[contains(text(),'I agree')]")
        time.sleep(5)
        print('Account created succesfully!')

        
        