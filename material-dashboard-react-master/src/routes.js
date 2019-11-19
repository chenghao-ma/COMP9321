// @material-ui/icons
import Dashboard from "@material-ui/icons/Dashboard";
import Person from "@material-ui/icons/Person";
// core components/views for Admin layout
import DashboardPage from "views/Dashboard/Dashboard.js";
import UserProfile from "views/UserProfile/UserProfile.js";
import Predict from "views/Predict/predict.js";
import TableList from "views/TableList/TableList.js";
import Typography from "views/Typography/Typography.js";
import Icons from "views/Icons/Icons.js";
import Maps from "views/Maps/Maps.js";
import NotificationsPage from "views/Notifications/Notifications.js";
// core components/views for RTL layout
import RTLPage from "views/RTLPage/RTLPage.js";
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
