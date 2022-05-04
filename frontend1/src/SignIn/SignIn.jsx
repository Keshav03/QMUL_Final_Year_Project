import "./signin.css";
import { useEffect, useState } from "react";
import Header from "../Header/Header.jsx";

import { Route, Redirect } from 'react-router'
import Home from "../Home/Home";
import { Navigate } from "react-router-dom";


function SignIn(props) {

  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(props.isLoggedIn);

  const updateUsername = (event) => {
    setUserName(event.target.value);
  };

  const updatePassword = (event) => {
    setPassword(event.target.value);
  };

  if(!props.isLoggedIn){
      return (
          <div className="signInWrapper">
      <Header logout={props.logout} isLoggedIn={isLoggedIn} />

 
      <div className="sigInForm">
        <p id="title">LOGIN</p>

        <label className="label">Username</label>
        <input
          name="uName"
          placeholder="Enter userName!"
          className="inputField"
          onChange={updateUsername}
          ></input>

        <label className="label">Password</label>
        <input
          name="pass"
          placeholder="Enter Password!"
          className="inputField"
          onChange={updatePassword}
          type="password"
          ></input>
        <button onClick={()=> props.login(userName,password)} id="signin-btn">
          Sign In
        </button>
      </div>
    </div>
  );
    }else{
         return (
           <div>
              <Navigate to="/"/>
           </div>
          )
}
}

export default SignIn;
