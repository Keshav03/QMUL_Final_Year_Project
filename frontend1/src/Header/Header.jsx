import logo from "../images/logo.png";
import "./header.css";
import { Link } from "react-router-dom";

import { useState, useEffect } from "react";

// import SignUp from './SignUp';
// import SignIn from './SignIn';
function Header(props) {
  const [isLoggedIn,setUserName] = useState(props.isLoggedIn);

  const [search,setSearch] = useState("")
  

  const updateSearch = (event) => {
    setSearch(event.target.value);
  };


return (
      <div className="header-container">
        <header className="header">
          <h1 id="headerTitle">GamePire</h1>



          <input placeholder="Enter Video Games" id="searchBar" onChange={updateSearch}></input>
          <button className="submit" onClick={()=> props.searchRecommendation(search)}>Submit</button>
          <div className="nav">

            <Link to="/" className="link">
              Home
            </Link>

            {!props.isLoggedIn? 
            <>
              <Link to="/signin" className="link">
                Login
              </Link>:
            </>:

            <button onClick={props.logout} className="link">
              Logout
            </button>

            }


          </div>
        </header>
      </div>
    );
  
}

export default Header;
