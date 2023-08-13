import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import os

# Get the absolute path of the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
requirements_file = os.path.join(current_directory, "requirements.txt")

def main():
    st.title("Location Details Finder")

    # Input for coordinates
    coordinates = []
    
    lat = st.number_input(f"Enter Latitude for Coordinate:")
    lon = st.number_input(f"Enter Longitude for Coordinate:")
    coordinates.append((lat, lon))

    if st.button("Find Details"):
        # Scrape location details for the given coordinates
        scraped_locations = scrape_location_details(coordinates)

        # Display the scraped location details in Streamlit
        if scraped_locations:
            st.write("Scraped Location Details:")
            for location in scraped_locations:
                st.write(location)
        else:
            st.write("No location details found within the specified coordinates.")

def scrape_location_details(coordinates):
    # Set up the Selenium web driver (you need to download the appropriate driver for your browser)
    # For Chrome, download the chromedriver executable: https://sites.google.com/a/chromium.org/chromedriver/downloads
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")  # To run Chrome in headless mode
    #driver = webdriver.Chrome(options=chrome_options)

    # API key for Google Maps
    headers = {
        "authorization": st.secrets["AUTH_KEY"],
        "content-type": "application/json",
    }

    # Implement the logic for scraping location details within the provided coordinates
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    location_details = []

    for lat, lon in coordinates:
        # Send API request to Google Maps API
        params = {
            "location": f"{lat},{lon}",
            "radius": "1000",  # 1000 meters (adjust the radius as needed)
            "key": st.secrets["AUTH_KEY"],
        }
        response = requests.get(base_url, params=params)

        # Wait for the API response (you might need to add a longer wait time based on your internet speed)
        time.sleep(5)

        # Process the API response and extract location details
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK":
                for result in data["results"]:
                    name = result["name"]
                    rating = result.get("rating", 0)
                    user_ratings_total = result.get("user_ratings_total", 0)
                    if rating < 4 and user_ratings_total <= 1000:
                        address = result.get("vicinity", "")
                        location_details.append(f"[Name: {name}   Rating: {rating}   Total Reviews: {user_ratings_total}   Address: {address}]")
                    
            else:
                print("Error:", data["status"])
        else:
            print("Failed to fetch location details.")
    
    # Close the browser
    #driver.quit()

    # Return the list of scraped location details
    return location_details

if __name__ == "__main__":
    main()