import * as React from "react";

import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Button from "@mui/material/Button";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import { common } from '@mui/material/colors';
import { styled } from '@mui/material/styles';

import { useNavigate } from "react-router-dom";

import "../App.css";


const ColorButton = styled(Button)(({ theme }) => ({
  color: "#ffffff",
  backgroundColor: common[500],
  '&:hover': {
    backgroundColor: common[700],
  },
}));


const PositionedMenu = () => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  }

  const handleLogout = () => {
    localStorage.clear();
    window.location.reload();
  };

  return (
    <div>
      <IconButton
        onClick={handleClick}
        size="small"
        sx={{ ml: 2 }}
        aria-controls={open ? "account-menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open ? "true" : undefined}
      >
          <Avatar sx={{ width: 32, height: 32 }}></Avatar>
      </IconButton>
      <Menu
        id="demo-positioned-menu"
        aria-labelledby="demo-positioned-button"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "top",
          horizontal: "left",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "left",
        }}
      >
        <MenuItem id="profile-button" onClick={() => {window.location.replace("http://localhost:3000/profile")}}>Профиль</MenuItem>
        <MenuItem id="logout-button" onClick={handleLogout}>Выйти</MenuItem>
      </Menu>
    </div>
  );
}


const Navbar = () => {
  const [userValidity, setUserValidity] = React.useState(false)
  const navigate = useNavigate();

  const RenderProfileElement = () => {  
    const verifyToken = async () => {
      const userToken = localStorage.getItem("access_token");
      const response = await fetch("http://localhost:8080/api/v1/oauth2/verify_token", {
        method: "POST",
        headers: {"Content-Type": "application/json", "Authorization": `Bearer ${userToken}`}
      })

      if (response.status != 401) {
        setUserValidity(true)
      } else {
        setUserValidity(false)
      }

    }

    try {
      verifyToken();
    } 
    catch (e) {
      alert(e);
    }

    if (userValidity) {
      return (
        <PositionedMenu />
      )
    } else {
      return (
        <Button
          id="sign-in-button"
          variant="contained"
          className="custom-button"
          onClick={handleAuthClick}
        >
          Войти/Зарегистрироваться
        </Button>
      )
    }
  }

  const handleAuthClick = () => {
    navigate("/sign_in");
  }

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <a href="/" className="logo">Главная</a>
      </div>
      <div className="navbar-right">
        <RenderProfileElement />
      </div>
    </nav>
  )
}

export default Navbar;