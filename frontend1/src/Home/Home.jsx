import Header from '../Header/Header.jsx';
import SideNav from "../SideNav/SideNav";
import Recommendation from "../Games/Recommendation";

import { useEffect, useState } from "react";


function Home(props) {

return (
  <div className="container">

      <Header  logout={props.logout} isLoggedIn={props.isLoggedIn} searchRecommendation={props.searchRecommendation}></Header>
      <SideNav user={props.user}></SideNav>
      <Recommendation user={props.user} gameList={props.gameList} recommendList={props.recommendList} isLoggedIn={props.isLoggedIn}></Recommendation>

  </div>
    );
  
}

export default Home;
