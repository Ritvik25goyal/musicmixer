import React, { useEffect } from 'react'
import SpotifyPlayer from 'react-spotify-web-playback'
export default function Player({ accessToken, trackUri }) {
    const [play , setPlay] = React.useState(false)

    useEffect(() => setPlay(true), [trackUri])
    if (!accessToken) return null
  return <SpotifyPlayer
        token={accessToken}
        showSaveIcon
        callback={state => {
            if (!state.isPlaying) setPlay(false)
        }}
        uris={trackUri ? [trackUri] : []}
        play={play}
        styles={{
            activeColor: '#fff',
            bgColor: '#333',
            color: '#fff',
            loaderColor: '#fff',
            sliderColor: '#1cb954',
            trackArtistColor: '#ccc',
            trackNameColor: '#fff',
          }}
        
     />
}
