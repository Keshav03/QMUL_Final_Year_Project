import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import Header from '../Header/Header.jsx';
import './signup.css';
import { useNavigate } from 'react-router-dom';


function SignUp() {
    let navigate = useNavigate();


    const [userName,setUserName] = useState("");
    const [firstName,setFirstName] = useState("");
    const [lastName,setLastName] = useState("");
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");

    const updateUsername = (event)=>{
        setUserName(event.target.value)
    };

    const updateFirstName = (event)=>{
        setFirstName(event.target.value)
    };

    const updateLastName = (event)=>{
        setLastName(event.target.value)
    };

    const updateEmail = (event)=>{
        setEmail(event.target.value)
    };

    const updatePassword = (event)=>{
        setPassword(event.target.value)
    };

    async function signUp(){
        const formData = new FormData();
        // Change this line
        formData.append('userName', userName);  
        formData.append('firstName', firstName);  
        formData.append('lastName', lastName);  
        formData.append('email', email);  
        formData.append('passowrd', password);  
        let response = await fetch("http://localhost:8000/api/createUser/",{
            method: "POST",
            headers: {
                origin : "http://127.0.0.1:3000"
            },
            mode : "cors",
            body:formData
        })
        .then(response => {
            console.log(response)
            navigate('/signIn')
        }
            )
        .catch(err => alert(err));
    }

  return (
    <div className="signUpWrapper">
        <Header />
        <div className='signUpForm' >
            <p id="title">SIGN UP</p>

            <label className='label'>Username :</label>  
            <input name="uName" placeholder='Enter userName!' className='inputField' onChange = {updateUsername}></input>
            <label className='label'>First Name : </label>  
            <input name="fName" placeholder='Enter First Name!' className='inputField' onChange = {updateFirstName}></input>
            <label  className='label' >Last Name :</label>  
            <input name="lName" placeholder='Enter Last Name!' className='inputField' onChange = {updateLastName}></input>
            <label  className='label'>Email :</label>  
            <input name="email" placeholder='Enter Email Address!' className='inputField' onChange = {updateEmail}></input>
            <label  className='label'>Password : </label>  
            <input name="pass" placeholder='Enter Password!' className='inputField' onChange = {updatePassword} type="password"></input>
            <button onClick={signUp} id="signup-btn">
                Sign Up
            </button>
        </div>
    </div>
  );
}

export default SignUp;
