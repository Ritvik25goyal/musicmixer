import React, { useState, useEffect } from "react";
import Sidebar from "../src/Components/sidebar/Sidebar";
import Container from "../src/Components/Container/container";
import Player from '../src/Components/Player';
import axios from 'axios';
import Card from "./Components/Card/Cards";



function Root() {
  const [playtrack, setplaytrack] = useState([]);
  const [accessToken, setAccessToken] = useState('');
  const [currentsong, setcurrentsong] = useState([]);
  const [genreRecommendations, setGenreRecommendations] = useState({});
  useEffect(() => {
    axios
      .get('http://127.0.0.1:8000/genre_recommendations/')
      .then((response) => {
        console.log(response.data);
        setAccessToken(response.data.access_token);
        setGenreRecommendations(response.data.genre_recommendation || {});
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);
  
  


  console.log(currentsong)
    return (
      <>
        <div className="App">
          <Sidebar />
          <div className="Content">
            {Object.keys(genreRecommendations).map((genre) => (
              <div key={genre}>
                <h2>{genre}</h2>
                {genreRecommendations[genre]?.tracks?.map((track) => (
                  <div key={track.album.id}>
                    <Card
                      image={track.album.images[1].url}
                      title={track.album.name}
                      description={track.album.artists[0].name}
                    />
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
        <div className='footer'>
          {/* Make sure to pass the correct props to the Player component */}
          <Player accessToken={accessToken} trackUri={currentsong} />
        </div>
      </>
    );
  }
export default Root