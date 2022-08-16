import unittest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException        
import os
import time

pathThisFile = os.path.dirname(os.path.realpath(__file__))  # This file path
pathCorrectFile= os.path.join(pathThisFile,'correctImage.png')
pathIncorrectFile= os.path.join(pathThisFile,'incorrectImage.pdf')

class TestsUserInterface(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    self.vars = {}
    self.driver.get("http://localhost:5000/")
  
  def test_correctImage(self):
    assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Predicción de juegos"
    self.driver.find_element(By.NAME, "predict_image").send_keys(pathCorrectFile)
    self.driver.find_element(By.ID, "inputPredict").click()
    time.sleep(2)
    assert self.driver.find_element(By.ID, "gameImage").is_displayed()
    assert self.driver.find_element(By.ID, "predictedGameData").is_displayed()

  def test_incorrectImageUploaded(self):
    assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Predicción de juegos"
    self.driver.find_element(By.NAME, "predict_image").send_keys(pathIncorrectFile)    
    self.driver.find_element(By.ID, "inputPredict").click()
    time.sleep(2)
    assert self.driver.switch_to.alert.text == "Se debe seleccionar una imagen"

  def test_noImageUploaded(self):
    assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Predicción de juegos"
    self.driver.find_element(By.ID, "inputPredict").click()
    assert self.driver.switch_to.alert.text == "Se debe seleccionar una imagen"

  def tearDown(self):
    self.driver.quit()
  
if __name__ == "__main__":
  unittest.main()