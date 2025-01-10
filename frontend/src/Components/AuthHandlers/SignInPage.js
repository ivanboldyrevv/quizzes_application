import * as React from "react";

import Link from "@mui/material/Link";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import FormLabel from "@mui/material/FormLabel";
import FormControl from "@mui/material/FormControl";
import Stack from "@mui/material/Stack";

import { parseJwt } from "./AuthUtils";

import "../styles.css";


function handleClick() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const fetchToken = async () => {
        try {
            const response = await fetch("http://localhost:8080/api/v1/oauth2/sign_in", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({"username": username, "password": password})
            })
    
            const data = await response.json();
            
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);

            const decoded = parseJwt(data.access_token);

            localStorage.setItem("username", decoded.username);
            localStorage.setItem("userId", decoded.sub);

            window.location.replace("http://localhost:3000/");

        }
        catch (e) {
            alert(e);
        }
    }

    fetchToken();
}


const SignInCard = () => {
    return (  
        <React.Fragment>
          <CardContent>
              <Stack spacing={2}>            
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
                        onClick={handleClick}
                  >
                      Войти
                  </Button>
                  <p>Нету аккаунта? <Link href="/sign_up">Зарегистрироваться</Link></p>
              </Stack>
          </CardContent>
        </React.Fragment>
  )
};


function SignInPage() {
    return (
        <div className="sign-container">
            <div className="sign-form">
                <SignInCard />
            </div>
        </div>
    )
}

export default SignInPage;
