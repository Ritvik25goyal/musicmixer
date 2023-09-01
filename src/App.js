import './App.css';
import Login from './Login';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Root from './Root';
import React, { useState, useEffect } from 'react';


function App() {

  
  return (
    <BrowserRouter>
      <Routes >
        <Route path="/" element={<Login/>} />
        <Route path="/home" element={<Root />}/>
      </Routes>
    </BrowserRouter>
    
  );
}

export default App;
