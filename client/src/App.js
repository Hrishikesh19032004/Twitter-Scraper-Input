import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';  // Import the updated CSS

const App = () => {
  const [url, setUrl] = useState('');
  const [userData, setUserData] = useState(null);

  const handleScrape = async () => {
    try {
      const response = await axios.post('http://localhost:5000/scrape', { url });
      if (response.data.user_data) {
        setUserData(response.data.user_data);  // Make sure you're setting the correct part of the response
      } else {
        console.error("No user data returned");
      }
    } catch (error) {
      console.error('Error scraping:', error);
    }
  };

  return (
    <Router>
      <div className="app-container">
        <h1 className="app-header">Twitter Scraper</h1>
        <div className="input-container">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter Twitter URL"
            className="url-input"
          />
          <button onClick={handleScrape} className="scrape-button">
            Scrape
          </button>
        </div>

        {userData && (
          <div className="profile-card">
            <img src={userData.profile_image_url} alt="Profile" className="profile-image" />
            <div className="profile-info">
              <h2>{userData.profile_name}</h2>
              <p className="bio">{userData.bio}</p>
              <p><strong>Followers:</strong> {userData.followers}</p>
              <p><strong>Following:</strong> {userData.following}</p>
              <p><strong>Location:</strong> {userData.location}</p>
              <p><strong>Website:</strong> <a href={userData.website} target="_blank" rel="noopener noreferrer">{userData.website}</a></p>
              <Link to="/posts">
                <button className="view-posts-button">View Posts</button>
              </Link>
            </div>
          </div>
        )}
      </div>
    </Router>
  );
};

export default App;
