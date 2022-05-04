import "./recommendation.css";
import { useState, useEffect } from "react";

function Recommendation(props) {
  const [rate, setRate] = useState(0);
  const [gameList, setGameList] = useState([]);
  const [likedGame, setLikedGame] = useState([]);

  const updateRate = (event) => {
    setRate(event.target.value);
  };

  console.log(props.isLoggedIn)
  

  async function getGames() {
    let response = fetch("http://127.0.0.1:8000/api/csvToJson/", {
        credentials: "include",
        method: "GET",
        headers: {
          origin: "http://127.0.0.1:3000",
        },
        mode: "cors",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.gameList)
          // var arr = [];
          // while (arr.length < 10) {
          //   var r = Math.floor(Math.random() * data.gameList.length);
          //   if (arr.indexOf(r) === -1) arr.push(r);
          // }
          // var newList = [];
          // arr.map((index) => {
          //   newList.push(data.gameList[index]);
          // });
          setGameList(data.gameList);
        })
        .catch((err) => alert("Information cannot be retrieved!"));
  }

  async function rateGame(gameid) {
    
    if(rate<0 || rate> 5){
      alert("Rating should be a value between 0 & 5 ")
      return
    }

    const formData = new FormData();
    formData.append("gameid", gameid)
    formData.append("rating", rate);




    let response = await fetch("http://127.0.0.1:8000/api/rate/", {
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
        getGames()
      })
      .catch((err) => alert("You need to be logged in to like game!"));
  }







  useEffect(() => {
    if(props.isLoggedIn){
      getGames()
    }

  }, [props.isLoggedIn]);




    return (
      <div className="recommendation">
        {props.recommendList.length == 0 ? (
          <div>
              <p id="Msg">Enter a game in the search bar to look for simillar game!</p>
          </div>
        ) : (
          <div>
            <h2 className="heading1">Recommendation <span class="span">Based on Search</span></h2>
            <div className="recommendedGameWrapper">
              
            {props.recommendList.map((item) => (
              
              <div className="games">
              <div className="gameImageGrid">
                <img
                  src={require(`../images/games/${item.image}`)}
                  alt=""
                  className="gameImg"
                />
              </div>
              <p className="gameTitle">{item.name}</p>

              <p className="gameInfo">
                {item.genre} ~ {item.year} ~ {item.publisher}
              </p>


              </div>
            ))}

            </div>
          </div>
        )}
        
        {gameList.length == 0 ? (
          <div>
            <h1 id="loadingMsg">LOADING...</h1>
          </div>
        ) : (
          <div>
            
            <h2 className="heading">Explore Video Games</h2>


          <div className="exploreGameWrapper">
          {gameList.map((item) => (
            <div className="games">
              <div className="gameImageGrid">
                <img
                  src={require(`../images/games/${item.image}`)}
                  alt=""
                  className="gameImg"
                />
              </div>
              <p className="gameTitle">{item.name}</p>

              <p className="gameInfo">
                {item.genre} ~ {item.year} ~ {item.publisher}
              </p>
              <div id="rateDiv">
                <p>Your rating : {item.rating}</p>
                <input type="number" min="1" max="5" name="rating" onChange={updateRate} ></input>

                <button
                  onClick={() => rateGame(item.gameid)}
                  className="likeBtn"
                >
                  {" "}
                  Rate{" "}
                </button>
              </div>
            </div>
          ))}
        </div>

          </div>
        )}


      </div>
    )
      

}

export default Recommendation;
