// @material-ui/icons
import Dashboard from "@material-ui/icons/Dashboard";
import Person from "@material-ui/icons/Person";
// core components/views for Admin layout
import DashboardPage from "views/Dashboard/Dashboard.js";
import UserProfile from "views/UserProfile/UserProfile.js";
import Predict from "views/Predict/predict.js";

import SignupPage from "views/Signup/SignupPage.js";
import Fingerprint from "@material-ui/icons/Fingerprint";
import LibraryBooks from "@material-ui/icons/LibraryBooks";
import ExitToApp from "@material-ui/icons/ExitToApp";
import LoginPage from "views/Login/LoginPage.js";


if (localStorage.getItem("userName")==null) {
  var dashboardRoutes = 
    [{
        path: "/dashboard",
        name: "Dashboard",
        icon: Dashboard,
        component: DashboardPage,
        layout: "/admin"
      },
      {
        path: "/predict",
        name: "Predict",
        icon: LibraryBooks,
        component: Predict,
        layout: "/admin"
      },
      {
        path: "/signup",
        name: "Sign Up",
        icon: Fingerprint,
        component: SignupPage,
        layout: "/admin"
      },
      {
        path: "/login",
        name: "Login",
        icon: ExitToApp,
        component: LoginPage,
        layout: "/admin"
      },]
}else{
  var dashboardRoutes = 
    [{
        path: "/dashboard",
        name: "Dashboard",
        icon: Dashboard,
        component: DashboardPage,
        layout: "/admin"
      },
      {
        path: "/predict",
        name: "Predict",
        icon: LibraryBooks,
        component: Predict,
        layout: "/admin"
      },
      {
        path: "/user",
        name: "User Profile",
        icon: Person,
        component: UserProfile,
        layout: "/admin"
      },]
  
}



export default dashboardRoutes;
