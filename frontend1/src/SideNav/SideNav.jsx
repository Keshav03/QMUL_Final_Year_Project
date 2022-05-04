import "./sideNav.css";
import { useEffect, useState } from "react";
import Header from "../Header/Header.jsx";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import ProfileImg from './profileImg.jpg';

function SideNav(props) {

  const [userName, setUserName] = useState("");
  const [name,setName] = useState("")
  const [isLoggedIn,setIsLoggedIn] = useState(props.isLoggedIn)


  return(
              <div className="sideNav">

                <h2 id="greeting" >Welcome Back , <br/> <span id="username"> {props.user}</span> </h2>

                <nav>
      
                    <Link to="/Profile" className="sLink">Profile</Link>
    
                </nav>

              </div>
  )    

}

export default SideNav;
