from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run without a GUI
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

# Scrape User Profile Data
def scrape_twitter_data(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Scrape username
        username = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'h1[role="heading"] span'))).text
        
        # Scrape profile name (real name)
        profile_name = ""
        try:
            profile_name = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[data-testid="UserName"] span'))).text
        except:
            profile_name = "Name not available"
        
        # Scrape bio
        bio = ""
        try:
            bio = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[data-testid="UserDescription"]'))).text
        except:
            bio = "No bio available"
        
        # Scrape following count
        try:
            following = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@href,"/following")]/span[1]/span'))).text
        except:
            following = "Following count not found"
        
        # Scrape followers count using the updated XPath based on your HTML snippet
        try:
            followers = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@href,"/WhatsApp/verified_followers")]/span[1]'))).text
        except:
            followers = "Followers count not found"

        # Scrape profile image URL (from div with class css-175oi2r)
        profile_image_url = ""
        try:
            profile_image_url = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.css-175oi2r img'))).get_attribute('src')
        except:
            profile_image_url = "Profile image not found"

        # Optional fields (location and website)
        location = "Location not found"
        website = "Website not found"

        try:
            location = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="UserLocation"]').text
        except:
            pass
        
        try:
            website = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="UserUrl"]').get_attribute('href')
        except:
            pass

        user_data = {
            "username": username,
            "profile_name": profile_name,
            "bio": bio,
            "following": following,
            "followers": followers,
            "location": location,
            "website": website,
            "profile_image_url": profile_image_url
        }

        # Save user data to CSV
        pd.DataFrame([user_data]).to_csv('user_data.csv', index=False)

        return user_data

    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

# Scrape Posts
def scrape_posts(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    posts_data = []

    try:
        posts = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'article')))[:20]
        
        for post in posts:
            content = post.text
            posts_data.append({"content": content})
        
        # Save posts to CSV
        pd.DataFrame(posts_data).to_csv('post_data.csv', index=False)

    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

    return posts_data

# Flask route
@app.route('/scrape', methods=['POST'])
def scrape_twitter():
    try:
        data = request.json
        twitter_url = data.get('url')

        if not twitter_url:
            return jsonify({"error": "URL is required"}), 400

        driver = init_driver()
        user_data = scrape_twitter_data(driver, twitter_url)

        if "error" in user_data:
            driver.quit()
            return jsonify(user_data), 500

        posts_data = scrape_posts(driver, twitter_url)
        driver.quit()

        return jsonify({
            "user_data": user_data,
            "posts_data": posts_data
        }), 200

    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"Error occurred: {error_msg}")
        return jsonify({"error": "An error occurred", "details": error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)
