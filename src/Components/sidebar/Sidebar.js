import React from "react";
import styled from "styled-components";
export default function Sidebar() {
  return (
    <Container>
      <div className="top__links">
        <ul>
          <li>
            <span>Home</span>
          </li>
          <li>
            <span>Recommended Songs</span>
          </li>
          <li>
            <span>Recommended Artists</span>
          </li>
        </ul>
      </div>
    </Container>
  );
}

const Container = styled.div`
  background-color: grey;
  color: #b3b3b3;
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 20%;
  position: fixed;
  .top__links {
    display: flex;
    flex-direction: column;
    .logo {
      text-align: center;
      margin: 1rem 0;
      img {
        max-inline-size: 80%;
        block-size: auto;
      }
    }
    ul {
      list-style-type: none;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      padding: 1rem;
      li {
        display: flex;
        gap: 1rem;
        cursor: pointer;
        transition: 0.3s ease-in-out;
        &:hover {
          color: white;
        }
      }
    }
  }
`;