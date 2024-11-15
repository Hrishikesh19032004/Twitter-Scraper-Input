# Twitter Scraping Flask App

## Project Overview
This project is a Flask-based web application designed to scrape public Twitter profiles for key user information such as username, bio, follower and following counts, location, and website URL. The application uses **Selenium** to interact with dynamically loaded web elements and extract the desired data. The scraped data is then saved in a CSV file and returned as a JSON response via a Flask API.

## Features
- **Dynamic Data Scraping**: Uses Selenium to interact with dynamic elements on Twitter pages.
- **Flask API**: Provides an endpoint to scrape data from Twitter by submitting a URL.
- **CSV Export**: Saves scraped user data to a CSV file for later use.
- **Error Handling**: Includes robust error handling for missing or inaccessible elements.
- **CORS Support**: Ensures cross-origin requests are handled, making it easy to integrate the API into other applications.

---

## Technologies Used
- **Python**: Core programming language.
- **Flask**: Web framework to create the API.
- **Selenium**: For web scraping and automating browser actions.
- **Pandas**: For data manipulation and exporting results to CSV.
- **Chrome WebDriver**: Enables Selenium to control Chrome browser.
- **Flask-CORS**: Allows handling cross-origin resource sharing.

---

## How It Works

### 1. **Selenium for Web Scraping**
Selenium automates browser actions such as:
- Opening the Twitter URL.
- Waiting for specific elements like the username, bio, followers, and following counts.
- Extracting text from these elements.

Selenium uses a **headless Chrome browser** to run in the background without a graphical interface.

### 2. **Scraping Process**
- **Dynamic Loading**: Twitter's content is loaded dynamically. Selenium waits for elements to load using explicit waits (`WebDriverWait` with `ExpectedConditions`).
- **Element Identification**:
    - **Username**: `h1[role="heading"] span`
    - **Bio**: `div[data-testid="UserDescription"]`
    - **Following Count**: `//a[contains(@href, '/following')]//span`
    - **Followers Count**: `//a[contains(@href, '/followers')]//span`
    - **Location**: `span[data-testid="UserLocation"]`
    - **Website**: `a[data-testid="UserUrl"]`

If an element is missing, a custom message like `"Followers count not found"` is returned.

---

## Project Structure
```
Twitter-Scraping/
│
├── app.py                  # Main Flask app with scraping endpoint
├── requirements.txt        # Project dependencies
├── user_data.csv           # CSV file for storing scraped user data
├── README.md               # Project documentation
└── chromedriver.exe        # Chrome WebDriver executable
```

---

## API Endpoint

### `/scrape` (POST)
#### Request Body:
```json
{
  "url": "https://twitter.com/username"
}
```

#### Response:
- **Success**:
    ```json
    {
      "user_data": {
        "username": "Sample User",
        "bio": "User bio here",
        "following": "456",
        "followers": "1234",
        "location": "Sample Location",
        "website": "https://samplewebsite.com"
      }
    }
    ```
- **Error**:
    ```json
    {
      "error": "An error occurred",
      "details": "Error message here"
    }
    ```

---

## Setup Instructions

### 1. **Prerequisites**
- Python 3.x
- Chrome Browser
- Chrome WebDriver (compatible with your Chrome version)

### 2. **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/twitter-scraping.git
   cd twitter-scraping
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. **Run the Application**
Start the Flask server:
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`.

---

## How Selenium Works in This Project
1. **WebDriver Initialization**:
    - Chrome WebDriver is launched in headless mode.
    - It navigates to the provided Twitter URL.

2. **Dynamic Content Handling**:
    - Selenium waits for the required elements to appear on the page.
    - Explicit waits ensure that elements like `followers` and `bio` are loaded before attempting to scrape.

3. **Data Extraction**:
    - Elements are located using CSS selectors or XPath.
    - Text values are extracted and stored in a dictionary.

4. **Error Handling**:
    - Missing elements are handled gracefully, returning a message like `"Location not found"`.

5. **Data Export**:
    - The scraped data is saved to a `user_data.csv` file using Pandas.

---

## Potential Issues and Solutions
- **Twitter Layout Changes**:
  - If Twitter changes its HTML structure, the CSS selectors or XPaths will need to be updated.
  
- **Rate Limiting**:
  - Twitter might block repeated scraping attempts. Use delays or API keys for higher access limits.
  
- **Element Not Found Errors**:
  - Ensure dynamic waits are sufficient or increase timeout values.

---

## Future Improvements
- Add support for scraping tweets.
- Implement a retry mechanism for transient errors.
- Use Twitter’s official API for enhanced reliability (if available).

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author
Hrishikesh Dhuri - 2024  
For support, contact: `hrishikesh.email@example.com`
