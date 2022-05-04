import { Link } from "react-router-dom";
import Header from '../Header/Header.jsx';
import SideNav from "../SideNav/SideNav";
import { useNavigate } from 'react-router-dom';
import ProfileImg from './profileImg.jpg';
import "./profile.css"

import { Navigate } from "react-router-dom";

import { useState, useEffect } from "react";

function Profile(props) {

  const[profile,setProfile] = useState([])
  const[userName,setUserName] = useState("") 
  const[gender,setGender] = useState("") 
  const[firstName,setFirstName] = useState("") 
  const[lastName,setLastName] = useState("") 
  const[email,setEmail] = useState("") 

  const updateUsername = (event) => {
    setUserName(event.target.value);
  };

  const updateGender = (event) => {
    setGender(event.target.value);
  };

  const updateFirstName = (event) => {
    setFirstName(event.target.value);
  };

  const updateLastName = (event) => {
    setLastName(event.target.value);
  };

  const updateEmail = (event) => {
    setEmail(event.target.value);
  };


  useEffect(async() => {
    let response = await fetch("http://127.0.0.1:8000/api/profile/",{
      credentials: 'include',
      method: "GET",
      headers: {
        origin : "http://127.0.0.1:3000"
      },
      mode : "cors",
    })
    .then(response => response.json())
    .then(data => {
      let list = []
      list.push(data)
      setProfile(list)
      setGender(data["gender"])
      setUserName(data["name"])
      setFirstName(data["firstName"])
      setLastName(data["lastName"])
      setEmail(data["email"])
    })
    .catch(err => alert(err))
  }
  ,[]);


  async function updateProfile(){
  
    if (gender != "Male" && gender !== "Female"){
      alert("Gender can be either 'Male' or 'Female' ")
      return
    }

    const formData = new FormData();
    formData.append("name", userName);
    formData.append("gender", gender);


    let response = await fetch("http://127.0.0.1:8000/api/profile/",{
      credentials: 'include',
      method: "POST",
      headers: {
        origin : "http://127.0.0.1:3000"
      },
      mode : "cors",
      body:formData
    })
    .then(response => response.json())
    .then(data => {
      let list = []
      list.push(data)
      setProfile(list)
    })
    .catch(err => alert(err))
  }

if(props.isLoggedIn){  
return (
  <div>

      <Header  logout={props.logout} isLoggedIn={props.isLoggedIn} ></Header>
      <SideNav user={props.user}></SideNav>

      <h2 id="pageTitle">Profile Page</h2>

      {profile.map((item) => (
          <div id="profileWrapper">

        <h3 id="name1">{item.name}</h3>

        <div id="basicInformation">

          <div id="userDetails"> 
            <h4 className="heading">  Basic Information</h4>
            <h4 class="sub-heading">Name</h4>
            <input type="text" value={userName} className="input" onChange={updateUsername} />
            <h4 class="sub-heading">First Name</h4>
            <input type="text" value={firstName} className="input" id="gender" onChange={updateFirstName}/>
            <h4 class="sub-heading">Last Name</h4>
            <input type="text" value={lastName} className="input" id="gender" onChange={updateLastName}/>
            <h4 class="sub-heading">Email</h4>
            <input type="text" value={email} className="input" id="gender" onChange={updateEmail}/>
            <h4 class="sub-heading">Gender</h4>
            <input type="text" value={gender} className="input" id="gender" onChange={updateGender}/>

          </div>

        </div>
        <div id="buttons">
          <button onClick={updateProfile} >Save</button>
        </div>
      </div>
      ))}
  </div>
    );
  }else{
    alert("You are not logged in!")
    return(
      <Navigate to="/"/>
    )

  }
}

export default Profile;
