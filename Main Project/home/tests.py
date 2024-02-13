# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LoginTestCase(TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome() 
#         self.driver.implicitly_wait(10)  

#     def tearDown(self):
#         self.driver.quit() 

#     def test_login(self):
#         self.driver.get('http://127.0.0.1:8000/login/')

#         username_input = self.driver.find_element(By.NAME, 'username')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.ID, 'login')

#         username_input.send_keys('gayathri')
#         password_input.send_keys('gayathri@123')
#         login_button.click()
#         print("user loggedin successfully")


#from django.test import LiveServerTestCasefrom django.test import LiveServerTestCase


# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class WorkerRegistrationTest(TestCase):

#     def setUp(self):
#         self.selenium = webdriver.Chrome()
#         super(WorkerRegistrationTest, self).setUp()

#     def tearDown(self):
#         self.selenium.quit()
#         super(WorkerRegistrationTest, self).tearDown()

#     def login(self, username, password):
       
#         self.selenium.get('http://127.0.0.1:8000/login/')

        
#         wait = WebDriverWait(self.selenium, 10)

#         username_input = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
#         password_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
#         login_button = wait.until(EC.presence_of_element_located((By.ID, 'login')))

       
#         username_input.send_keys(username)
#         password_input.send_keys(password)

      
#         login_button.click()
#         print("user loggedin successfully")

      
#         wait.until(EC.url_contains("/agentpage/"))  

#     def test_worker_registration_after_login(self):
       
#         self.login(username="goutham", password="goutham@123")

       
#         self.selenium.get('http://127.0.0.1:8000/addworker')

        
#         wait = WebDriverWait(self.selenium, 10)

#         name_input = wait.until(EC.presence_of_element_located((By.ID, "name")))
#         name_input.send_keys("John Doe")

#         nationality_input = wait.until(EC.presence_of_element_located((By.ID, "nationality")))
#         nationality_input.send_keys("Country")

      
#         registration_form = wait.until(EC.presence_of_element_located((By.ID, "registrationForm")))
#         registration_form.submit()

       
#         self.selenium.get('http://127.0.0.1:8000/viewworker')
#         print("Agent add worker successfully")



# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class BookingSeleniumTest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.get("http://127.0.0.1:8000/login") 

#     def tearDown(self):
#         self.driver.quit()

#     def login(self, username, password):
#         username_input = self.driver.find_element(By.NAME, "username")
#         password_input = self.driver.find_element(By.NAME, "password")
#         login_button = self.driver.find_element(By.ID, "login")

#         username_input.send_keys(username)
#         password_input.send_keys(password)
#         login_button.click()
#         print("user loggedin successfully")

       
#         WebDriverWait(self.driver, 10).until(EC.url_contains("/accounts/profile"))

#     def navigate_to_agent_request_page(self, worker_id, agent_id):
#         agent_link = self.driver.find_element(By.XPATH, f"//a[@href='/agent_contact/{agent_id}/{worker_id}/']")
#         agent_link.click()

      
#         WebDriverWait(self.driver, 10).until(EC.url_contains("/agent_contact"))

#     def test_booking_process(self):
        
#         self.login(username="gayathri", password="gayathri@123")

       
#         user_page_link = self.driver.find_element(By.ID, "worker-list-link")
#         user_page_link.click()

        
#         WebDriverWait(self.driver, 10).until(EC.url_contains("/worker_list"))

       
#         set_agent_button = self.driver.find_element(By.ID,"worker")
#         set_agent_button.click()

       
#         send_request_button = self.driver.find_element(By.ID, "sendMessageBtn")
#         send_request_button.click()

       
#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bookingModal")))

       
#         duration_input = self.driver.find_element(By.ID, "duration")
#         duration_input.send_keys("5")

#         duration_unit_select = self.driver.find_element(By.ID, "durationUnit")
#         duration_unit_select.send_keys("Months")

        
#         book_worker_button = self.driver.find_element(By.ID, "book")
#         book_worker_button.click()
#         print("Employer book worker successfully")

# if __name__ == "__main__":
#     unittest.main()



# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# class PoliceSeleniumTest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.get("http://127.0.0.1:8000/login") 

#     def tearDown(self):
#         self.driver.quit()

#     def login_to_police_page(self, username, password):
       
#         username_input = self.driver.find_element(By.NAME, "username")
#         password_input = self.driver.find_element(By.NAME, "password")
#         login_button = self.driver.find_element(By.ID, "login")

#         username_input.send_keys(username)
#         password_input.send_keys(password)
#         login_button.click()
#         print("user loggedin successfully")


       
#         WebDriverWait(self.driver, 10).until(EC.url_contains("/policepage"))

#     def test_verify_worker(self):
      
#         self.login_to_police_page(username="gokul", password="gokul@123")

        
#         user_page_link = self.driver.find_element(By.ID, "worker-list-link")
#         user_page_link.click()

      
#         WebDriverWait(self.driver, 10).until(EC.url_contains("/workerprofile"))

      
#         view_button = self.driver.find_element(By.ID, "view")
#         view_button.click()
#         WebDriverWait(self.driver, 10).until(EC.url_contains("/viewprofile"))

#         verify_button = self.driver.find_element(By.ID, "veri")
#         verify_button.click()
#         print("police verify worker successfully")
       

   
#         time.sleep(5) 
    

# if __name__ == "__main__":
#     unittest.main()
