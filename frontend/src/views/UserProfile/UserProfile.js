import React from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import CustomInput from "components/CustomInput/CustomInput.js";
import Button from "components/CustomButtons/Button.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";
// import all component js files needed
// @material-ui/core components
// antd design components
import {
  message
} from "antd";
import API from "../api.js.js";
const api = new API();

const styles = {
  cardCategoryWhite: {
    color: "rgba(255,255,255,.62)",
    margin: "0",
    fontSize: "14px",
    marginTop: "0",
    marginBottom: "0"
  },
  cardTitleWhite: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none"
  }
};
const userInfo = JSON.parse(localStorage.getItem('userName'));
function changePro_submit() {
  // Defining const with input
  const Orignial_password_value = document.getElementById('Orignial_password').value;
  const password_value = document.getElementById('password').value;
  const password_confirm_value = document.getElementById('password_confirm').value;
  
  // if no input,raise error
  if (Orignial_password_value == '') {
    alert('Please enter the original password.')
    return
  }
  if (Orignial_password_value != userInfo.password) {
    alert('Wrong original password.')
    return
  }
  if (password_value != password_confirm_value) {
    alert('Different confirm password.')
    return
  }
  // got password value and update it in database
  const path = 'auth/login/changePassword/' + userInfo._id;
  console.log(path)
  const headers = {
    Accept: "application/json",
    "Content-Type": "application/json"
  }
  const method = "PUT";
  const body = {
    "password": password_value
  }
  api.apiRequest(path, {
    headers,
    method,
    body: JSON.stringify(body)
  }).then(function (res) {
    console.log(res)
  });
  alert('Successfully change password.');
  localStorage.clear()
  setTimeout("window.location.href='/admin/login'", 1000)
}

const useStyles = makeStyles(styles);

export default function UserProfile() {
  const classes = useStyles();
  return (
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader color="primary">
              <h4 className={classes.cardTitleWhite}>Edit Profile</h4>
              <p className={classes.cardCategoryWhite}>Complete your profile</p>
            </CardHeader>
            <CardBody>
              <GridContainer>
                
                <GridItem xs={12} sm={12} md={3}>
                  <CustomInput
                    labelText={userInfo["first_name"]+' '+userInfo["last_name"]}
                    id="username"
                    formControlProps={{
                      fullWidth: true
                    }}
                    inputProps={{
                      disabled: true
                    }}
                  />
                </GridItem>
                <GridItem xs={12} sm={12} md={4}>
                  <CustomInput
                    labelText={userInfo["email"]}
                    id="email-address"
                    formControlProps={{
                      fullWidth: true
                    }}
                    inputProps={{
                      disabled: true
                    }}
                  />
                </GridItem>
                <GridItem xs={12} sm={12} md={5}>
                  <CustomInput
                    labelText="orignial password"
                    id = "Orignial_password"
                    formControlProps={{
                      fullWidth: true
                    }}
                  />
                </GridItem>
              </GridContainer>
              <GridContainer>
                <GridItem md={4}>
                  <CustomInput
                    id="password"
                    labelText="new password"
                    formControlProps={{
                      fullWidth: true
                    }}
                  />
                  <CustomInput
                   id = "password_confirm"
                   labelText = "confirm your new password"
                   formControlProps={{
                      fullWidth: true
                    }}
                   />
                </GridItem>
              </GridContainer>
            </CardBody>
            <CardFooter>
              <Button color="primary" onClick={() => changePro_submit()}>Update Profile</Button>
              <Button color="danger" onClick={()=>{localStorage.clear();window.location.href='/admin/dashboard'}}  >Logout</Button>
            </CardFooter>
          </Card>
        </GridItem>
      </GridContainer>
  );
}
