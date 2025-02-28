import requests
import csv
from csv import writer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from geopy.geocoders import Nominatim
import argparse


class Weather:

    def __init__(self, city, date, endDate = None):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (optional)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver = driver
        self.date = date
        self.city = city
        self.end_date = endDate 

    def __setup(self):
        geolocator = Nominatim(user_agent="my_geocoder_12345")  # Use a unique user_agent
        location = geolocator.geocode(self.city, exactly_one=True)
        if location:
            location_box = location.raw['boundingbox'] # Returns [South, North, West, East]
            return location_box
        else:
            raise Exception("Location not found. Please check city name.")


    def __get_url(self, location_box):
        north = location_box[1] + ","
        west = location_box[2] + ","
        south = location_box[0] + ","
        east = location_box[3]
        # Target URL
        url = "https://www.ncei.noaa.gov/access/search/data-search/local-climatological-data?bbox=" + north + west + south + east + "&pageNum=1&startDate=" + self.date + "T00:00:00&endDate=" + self.date + "T23:59:59"
        return url
    
    def __clear_files(self):
        # clearing both files before appending to them
            filename1 = "yearlyContent.csv"
            f1 = open(filename1, "w+")
            f1.close()
            filename2 = "dayContent.csv"
            f2 = open(filename2, "w+")
            f2.close()
            filename3 = "dateRangeContent.csv"
            f3 = open(filename3, "w+")
            f3.close()

    def __create_links(self, url):
        self.driver.get(url)  # Ensure page is fully reloaded
        # throw exception if url/NOAA is down
        self.driver.refresh()  # Force refresh to avoid caching issues

        try:
            # Wait for the elements to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-header")))
            
            # Find all links inside elements with class "card-header"
            links = self.driver.find_elements(By.CSS_SELECTOR, ".card-header a")
            links_set = set()
            # Extract and print hrefs
            if links:
                for link in links:
                    links_set.add(link.get_attribute("href"))
                    # print()
            else:
                self.driver.quit()
                raise Exception("No data.")
            
             # Close the browser
            self.driver.quit()
            return links_set
            
        except Exception as e:
            print(e)

    def __get_yearly_content(self, links_set):
        self.__clear_files()
        if links_set:
            for l in links_set:
                req = requests.get(l)
                url_content = req.content
                csv_file = open('./yearlyContent.csv', 'ab')
                csv_file.write(url_content)
                csv_file.close()
        else:
            raise Exception("Please try again.")

    def __get_daily_content(self, links_set):
        try:
            total_rows = len(links_set)
            seen = False
            firstRow = False
            with open('./dayContent.csv', 'a') as wt_csv_file:
                with open('./yearlyContent.csv', 'r') as r_csv_file:
                    reader = csv.DictReader(r_csv_file)
                    write_file = writer(wt_csv_file)
                    for row in reader:
                        if firstRow == False:
                            write_file.writerow(row)
                            firstRow = True
                        if (self.date in row["DATE"]):
                            write_file.writerow(row.values())
                            seen = True
                        elif (seen == True):
                            total_rows -= 1
                            if (total_rows <= 0):
                                break
                            else:
                                seen = False
                        else:
                            continue
            print("Done (daily-hourly data)")
        except Exception as e:
            print("Error:", e)

    def __get_links(self):
        location_box = self.__setup()
        url = self.__get_url(location_box)
        links = self.__create_links(url)
        return links


    def __get_hourly_range(self, links_set):
        try:
            total_sections = len(links_set)
            found_start_row = False
            found_end_row = False
            first_row = False
            with open('./dateRangeContent.csv', 'a') as wt_csv_file:
                with open('./yearlyContent.csv', 'r') as r_csv_file:
                    reader = csv.DictReader(r_csv_file)
                    write_file = writer(wt_csv_file)
                    for row in reader:
                        if total_sections <= 0:
                            break
                        if first_row == False:
                            write_file.writerow(row)
                            first_row = True
                        if (self.date in row["DATE"]):
                            found_start_row = True
                        if found_start_row and (not found_end_row) and self.end_date not in row["DATE"]:
                            write_file.writerow(row.values())
                        
                        if self.end_date in row["DATE"]:
                            write_file.writerow(row.values())
                            found_end_row = True
                        elif found_end_row:
                            total_sections -= 1
                            found_start_row = False
                            found_end_row = False
                
            print("Done (data in a date range).")
        except Exception as e:
            print("Error:", e)
        
    def generate_hourly_data(self):
        links = self.__get_links()
        self.__get_yearly_content(links)
        self.__get_daily_content(links)
    
    def generate_yearly_hourly_data(self):
        links = self.__get_links()
        self.__get_yearly_content(links)

    def generate_hourly_data_range(self):
        links = self.__get_links()
        self.__get_yearly_content(links)
        self.__get_hourly_range(links)
            
def main():
    parser = argparse.ArgumentParser()
    # # can run the file and user not input a city or date
    parser.add_argument("city", type=str, help="Enter the city or state")
    parser.add_argument("date", type=str, help="Enter the date (YYYY-MM-DD)")
    parser.add_argument('--endDate', type=str, default=None, help="Enter the optional end date (YYYY-MM-DD)")
    args = parser.parse_args()

    w = Weather(args.city, args.date, args.endDate)
    if (args.endDate != None):
        w.generate_hourly_data_range()
    else:
        w.generate_hourly_data()


if __name__ == '__main__':
    main()
