import React,{useState,useEffect} from "react";
import Sidebar from "../src/Components/sidebar/Sidebar";
import Container from "../src/Components/Container/container";
import Player from '../src/Components/Player';
import axios from 'axios';

function Root() {
  const [topTracks, setTopTracks] = useState([]);
  var accessToken ="BQBoJnhbfkgB56ouzGuCHJ4ByQzawGHkBTAdnx7G8b1_NQXfHmPW_VvndPJ8K3zYzc2uiqSIZxY7kPrUNZt5OMZPE9oy1mrsiLSTP1Cevdajbp12RfMLQhjfjNggjRXupFN5Ov1779kZk-lOhDbUxd2coGv7tPaZVIrAnCdmGH5DkC8cml4NpLNmJtyQbVh_mVvBXpbPTu93fmjIJP3FWguKX55-gCcSNv8jTFmGt-5SOSq8GOVk5V0YP2StjucCRh7zKA"
  var auth = "BQBoJnhbfkgB56ouzGuCHJ4ByQzawGHkBTAdnx7G8b1_NQXfHmPW_VvndPJ8K3zYzc2uiqSIZxY7kPrUNZt5OMZPE9oy1mrsiLSTP1Cevdajbp12RfMLQhjfjNggjRXupFN5Ov1779kZk-lOhDbUxd2coGv7tPaZVIrAnCdmGH5DkC8cml4NpLNmJtyQbVh_mVvBXpbPTu93fmjIJP3FWguKX55-gCcSNv8jTFmGt-5SOSq8GOVk5V0YP2StjucCRh7zKA"

  useEffect(() => {
    const fetchTopTracks = async () => {
      try {
        const response = await axios.get('https://api.spotify.com/v1/me/top/tracks', {
          headers: {
            Authorization: `Bearer ${auth}`,
          },
        });
        setTopTracks(response.data.items);
      } catch (error) {
        console.error('Error fetching top tracks:', error);
      }
    };

    fetchTopTracks();
  }, [auth])


  const topTracksuri = topTracks.map((track) => track.uri);
  console.log(topTracksuri)
  
  console.log(topTracks)
  return (
    <>
      <div className="App">
        <Sidebar />
        <div className="empty"></div>
        <div className="Content">
          <Container />
          <Container />
          <Container />
          <Container />
          <Container />
        </div>
      </div>
      <div className='footer'>
        <Player accessToken={accessToken} trackUri={topTracksuri[1]} />
      </div>
    </>
  )
}

export default Root