import React,{Component} from "react";
import classNames from "classnames";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";

import Hidden from "@material-ui/core/Hidden";
import Poppers from "@material-ui/core/Popper";
import Divider from "@material-ui/core/Divider";
// @material-ui/icons
import Person from "@material-ui/icons/Person";

import Dashboard from "@material-ui/icons/Dashboard";
import Search from "@material-ui/icons/Search";
// core components
import CustomInput from "components/CustomInput/CustomInput.js";
import Button from "components/CustomButtons/Button.js";

import styles from "assets/jss/material-dashboard-react/components/headerLinksStyle.js";

const useStyles = makeStyles(styles);

export default class AdminNavbarLinks extends Component{

  render(){
    // const useStyles = useStyles();
    // const [openNotification, setOpenNotification] = React.useState(null);
    // const [openProfile, setOpenProfile] = React.useState(null);
    // const handleClickNotification = event => {
    //   if (openNotification && openNotification.contains(event.target)) {
    //     setOpenNotification(null);
    //   } else {
    //     setOpenNotification(event.currentTarget);
    //   }
    // };
    // const handleCloseNotification = () => {
    //   setOpenNotification(null);
    // };
  //  handleClickProfile= event => {
  //     if (openProfile && openProfile.contains(event.target)) {
  //       setOpenProfile(null);
  //     } else {
  //       setOpenProfile(event.currentTarget);
  //     }
  //   };
    // const handleCloseProfile = () => {
    //   setOpenProfile(null);
    // };
  return (
    <div>
      {/* <div className={useStyles.searchWrapper}>
        <CustomInput
          formControlProps={{
            className: useStyles.margin + " " + useStyles.search
          }}
          inputProps={{
            placeholder: "Search",
            inputProps: {
              "aria-label": "Search"
            }
          }}
        />
        <Button color="white" aria-label="edit" justIcon round>
          <Search />
        </Button>
      </div> */}
     
      <Button
        color={window.innerWidth > 959 ? "transparent" : "white"}
        justIcon={window.innerWidth > 959}
        simple={!(window.innerWidth > 959)}
        aria-label="Dashboard"
        className={useStyles.buttonLink}
      >
        <Dashboard className={useStyles.icons} />
        <Hidden mdUp implementation="css">
          <p className={useStyles.linkText}>Dashboard</p>
        </Hidden>
      </Button>
      <Button
        color={window.innerWidth > 959 ? "transparent" : "white"}
        justIcon={window.innerWidth > 959}
        simple={!(window.innerWidth > 959)}
        aria-label="Dashboard"
        className={useStyles.buttonLink}
      >
          <Person className={useStyles.icons} />
        {/* <Hidden mdUp implementation="css">
          <p className={useStyles.linkText}>Login</p>
        </Hidden> */}
      </Button>

      {/* <div className={useStyles.manager}>
        {/* <Button
          color={window.innerWidth > 959 ? "transparent" : "white"}
          justIcon={window.innerWidth > 959}
          simple={!(window.innerWidth > 959)}
          // aria-owns={openProfile ? "profile-menu-list-grow" : null}
          aria-haspopup="true"
          // onClick={handleClickProfile}
          className={useStyles.buttonLink}
        >
          <Person className={useStyles.icons} />
          <Hidden mdUp implementation="css">
            <p className={useStyles.linkText}>Profile</p>
          </Hidden>
        </Button> */}
        {/* <Poppers
          open={Boolean(openProfile)}
          anchorEl={openProfile}
          transition
          disablePortal
          className={
            classNames({ [useStyles.popperClose]: !openProfile }) +
            " " +
            useStyles.popperNav
          }
        >
          {({ TransitionProps, placement }) => (
            <Grow
              {...TransitionProps}
              id="profile-menu-list-grow"
              style={{
                transformOrigin:
                  placement === "bottom" ? "center top" : "center bottom"
              }}
            >
              <Paper>
                <ClickAwayListener onClickAway={handleCloseProfile}>
                  <MenuList role="menu">
                    <MenuItem
                      onClick={handleCloseProfile}
                      className={useStyles.dropdownItem}
                    >
                      Profile
                    </MenuItem>
                    <MenuItem
                      onClick={handleCloseProfile}
                      className={useStyles.dropdownItem}
                    >
                      Settings
                    </MenuItem>
                    <Divider light />
                    <MenuItem
                      onClick={handleCloseProfile}
                      className={useStyles.dropdownItem}
                    >
                      Logout
                    </MenuItem>
                  </MenuList>
                </ClickAwayListener>
              </Paper>
            </Grow>
          )}
        </Poppers> */}
      {/* </div> */} 
    </div>
  );
}
}