import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Details = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios.get('/post_data.csv').then((response) => {
      const csv = response.data;
      const rows = csv.split('\n').slice(1);
      const parsedPosts = rows.map((row) => {
        const [content] = row.split(',');
        return { content };
      });
      setPosts(parsedPosts);
    });
  }, []);

  return (
    <div>
      <h1>User Posts</h1>
      {posts.map((post, index) => (
        <div key={index} className="post-card">
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
};

export default Details;
