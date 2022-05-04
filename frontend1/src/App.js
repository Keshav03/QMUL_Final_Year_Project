import "./App.css";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import Header from "./Header/Header.jsx";
import SignUp from "./SignUp/SignUp.jsx";
import SignIn from "./SignIn/SignIn.jsx";
import Home from "./Home/Home.jsx";
import Profile from "./Profile/Profile";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function App() {

  const [isLoggedIn, setIsLoggedIn] = useState();
  const [user,setUser] = useState("Anonymous")
  const [gameList,setGameList] = useState([]);
  const [recommendList,setRecommendList] = useState([]);

  async function logout(){

    let response = await fetch("http://127.0.0.1:8000/api/logout/",{
      credentials: 'include',
      method: "POST",
      headers: {
        origin : "http://127.0.0.1:3000"
      },
      mode : "cors",
      body:{}
    })
    .then(response => response.json())
    .then(data => {
      setIsLoggedIn(false)
      setUser("Anonymous")
     
      
  })
    .catch(err => alert(err));
  }

  async function login(userName,password) {
    const formData = new FormData();
    formData.append("userName", userName);
    formData.append("password", password);

    let response = await fetch("http://127.0.0.1:8000/api/login/", {
      credentials: "include",
      method: "POST",
      headers: {
        origin: "http://127.0.0.1:3000",
      },
      mode: "cors",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        setIsLoggedIn(data.isLoggedIn);
        setUser(data.username);
      })
      .catch((err) => alert(err));
  }

  async function searchRecommendation(name) {
    const formData = new FormData();
    if (name == ""){
      alert("Empty String! Please enter a game")
      return
    }

    formData.append("name", name);

    let response = await fetch("http://127.0.0.1:8000/api/recommend/", {
      credentials: "include",
      method: "POST",
      headers: {
        origin: "http://127.0.0.1:3000",
      },
      mode: "cors",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        var list =[]
        for (let i in data["top5"]){
          list.push(data["top5"][i])
        }
        console.log(list)
        setRecommendList(list)
      })
    
}

  useEffect( async() => {
    let response = await fetch("http://127.0.0.1:8000/api/login/",{
      credentials: 'include',
      method: "POST",
      headers: {
        origin : "http://127.0.0.1:3000"
      },
      mode : "cors",
      body:{}
    })
    .then(response => response.json())
    .then(data => {
        setIsLoggedIn(data.isLoggedIn)
        setUser(data.username)
    })
    .catch(err => alert("Something Wrong Happened! Cannot log in!"))
  }
  ,[])


  return (
    <div className="App">
      <Router>
        <Routes>
          <Route exact path="/" element={<Home isLoggedIn={isLoggedIn} user={user} logout={logout} gameList={gameList} searchRecommendation={searchRecommendation}  recommendList={recommendList}/>}>
            
          </Route>
          <Route exact path="/signup" element={<SignUp isLoggedIn={isLoggedIn} user={user}/>}>
            
          </Route>
          <Route exact path="/signin" element={<SignIn isLoggedIn={isLoggedIn} user={user} logout={logout} login={login} />}>
            
          </Route>
          <Route exact path="/profile" element={<Profile  isLoggedIn={isLoggedIn} user={user} logout={logout}/>}>
            
          </Route>
        </Routes>
      </Router>
    </div>

  
  );
}

export default App;
