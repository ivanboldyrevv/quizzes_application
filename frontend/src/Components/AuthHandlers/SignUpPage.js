import * as React from "react";

import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import FormLabel from "@mui/material/FormLabel";
import FormControl from "@mui/material/FormControl";

import { parseJwt } from "./AuthUtils";

import "../styles.css";
import "../../App.css";


const RegistrationCard = () => {
  
  const handleSubmit = async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://localhost:8080/api/v1/oauth2/sign_up", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({"username": username, "password": password}),
    })
        
    const data = await response.json();
            
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);

    const decoded = parseJwt(data.access_token);
    
    localStorage.setItem("username", decoded.username);
    localStorage.setItem("userId", decoded.sub);

    const qresponse = await fetch("http://localhost:8080/api/v1/quizzes/add_user", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        "user_id": localStorage.getItem("userId"),
        "username": localStorage.getItem("username")
      })
    })
    const qdata = await qresponse.json();
    console.log(qdata);

    window.location.replace("http://localhost:3000/");
  }

  return (
    <React.Fragment>
      <CardContent>
        <Stack
          spacing={2}
        >          
          <FormControl>
              <FormLabel htmlFor="email">Email</FormLabel>
                  <TextField
                    id="username"
                    type="username"
                    name="username"
                    placeholder="username"
                    autoFocus
                    required
                    fullWidth
                    variant="outlined"
                  />
          </FormControl>
          <FormControl>
              <FormLabel htmlFor="password">Password</FormLabel>
                <TextField
                  className="text-form"
                  name="password"
                  placeholder="••••••"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  autoFocus
                  required
                  fullWidth
                  variant="outlined"
                />
          </FormControl>
          <Button
                type="submit"
                className="black-button"
                fullWidth
                variant="contained"
                onClick={handleSubmit}
          >
              Зарегистрироваться
          </Button>          
        </Stack>
      </CardContent>
    </React.Fragment>
  );
}

function SignUpPage() {
    return (
      <div className="sign-container">
        <div className="sign-form">
          <RegistrationCard />
        </div>        
      </div>
    )
}

export default SignUpPage;
