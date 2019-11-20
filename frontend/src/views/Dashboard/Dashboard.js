import React, { Component } from 'react'
// react plugin for creating charts
import ChartistGraph from "react-chartist";
// @material-ui/core
import { makeStyles } from "@material-ui/core/styles";
import Icon from "@material-ui/core/Icon";
// @material-ui/icons
import Store from "@material-ui/icons/Store";
import Warning from "@material-ui/icons/Warning";
import DateRange from "@material-ui/icons/DateRange";
import LocalOffer from "@material-ui/icons/LocalOffer";
import Update from "@material-ui/icons/Update";
import ArrowUpward from "@material-ui/icons/ArrowUpward";
import AccessTime from "@material-ui/icons/AccessTime";
import Accessibility from "@material-ui/icons/Accessibility";
import BugReport from "@material-ui/icons/BugReport";
import Code from "@material-ui/icons/Code";
import Cloud from "@material-ui/icons/Cloud";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Table from "components/Table/Table.js";
import Tasks from "components/Tasks/Tasks.js";
import CustomTabs from "components/CustomTabs/CustomTabs.js";
import Danger from "components/Typography/Danger.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardIcon from "components/Card/CardIcon.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

import tesdImage from "assets/img/cover.jpeg";
import ReactSVG from 'react-svg'
import { Avatar } from '@material-ui/core';
import ImageIcon from '@material-ui/icons/Image';
import { bugs, website, server } from "variables/general.js";

import {
  dailySalesChart,
  emailsSubscriptionChart,
  completedTasksChart
} from "variables/charts.js";

import styles from "assets/jss/material-dashboard-react/views/dashboardStyle.js";
import API from "../api.js";
const api = new API();
const useStyles = makeStyles(styles);

export default class Dashboard extends Component{

  constructor(props) {
    super(props);
    this.state = {
      isLoading:true,
      topTen:[],
      avgUserRating:null,
      dateVsAppSize:null,
      category:null,
      countGeners:null,
    };

    
  }

  async componentWillMount() {
    var path = 'show/getTopTen';
    // console.log(path)
    var headers = {
      Accept: "application/json",
      "Content-Type": "application/json"
    }
    const method = "GET";
    await api.apiRequest(path, {
      headers,
      method,
    }).then((res) => {
      console.log(res.result);
      var result  = [];
      res.result.forEach(element => {
        let resultObj = [];
        let icon = <CardMedia>
          < Avatar src={element["Icon URL"]} alt="..." />
          </CardMedia>
        // console.log(element["Icon URL"]);
        let name = element["Name"];
        let rating = element["Rating"];
        let genres = element["Genres"];
        let size = element["App Size"];
        let price = element["Price"];
        resultObj = [icon,name,rating,genres,size,price]
        result.push(resultObj);
      })
      this.setState({topTen:result})
    });
      
    path = 'show/dateVsAppSize';
    await api.apiRequest(path, {
        headers,
        method,
      }).then((res) => {
        console.log(res.result)
        this.setState({
          dateVsAppSize: require('./dateVsAppSize.svg')
        })
      });
    path = 'show/avgUserRating';
    await api.apiRequest(path, {
      headers,
      method,
    }).then((res) => {
      console.log(res.result)
      this.setState({
        avgUserRating: require('./avgUserRating.svg')
      })
    });
    path = 'show/category';
    await api.apiRequest(path, {
      headers,
      method,
    }).then((res) => {
      console.log(res.result)
      this.setState({
        categoryChart: require('./categoryChart.svg')
      })
    });
    path = 'show/countGeners';
    await api.apiRequest(path, {
      headers,
      method,
    }).then((res) => {
      console.log(res.result)
      this.setState({
        countGeners: require('./countGeners.svg')
      })
    });
    // console.log(result)
    this.setState({isLoading:false})
      // console.log(this.state.topTen[0][0])
    
    };

  render(){
    const { isLoading, ...res} = this.state;
        if (isLoading) {
            return (<div> Loading
            </div>
            )
        }
    return (

      <div>
        <GridContainer>
        
          <GridItem xs={12} sm={12} md={12}>
            <Card>
              <CardHeader color="warning">
                <h4 className={useStyles.cardTitleWhite}>Top Rating APPS</h4>
                <p className={useStyles.cardCategoryWhite}>
                  {/* 1th September, 2016 */}
                </p>
              </CardHeader>

              <CardBody>
                <Table
                  tableHeaderColor="warning"
                  tableHead={["Logo", "Name","Average User Rating", "Genres", "Size","Price"]}
                  tableData={this.state.topTen}
                />
              </CardBody>
            </Card>
          </GridItem>
        </GridContainer>

        < GridContainer direction = "column"
        alignItems = "center"
        justify = "center" >
          <GridItem xs={12} sm={12} md={7}>
          <Card>
        <CardActionArea>
          <ReactSVG src = {this.state.dateVsAppSize} />
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              Date & APP Size
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              With the development of technology, the size of game app is becoming larger and larger.
            </Typography>
          </CardContent>
        </CardActionArea>
      
      </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={7}>
          <Card>
        <CardActionArea>
          <ReactSVG src = {this.state.avgUserRating} />
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              Average User Rating
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              This graph shows the count of different ratings. Most game apps are rated around 4.5
            </Typography>
          </CardContent>
        </CardActionArea>
      
      </Card>
          </GridItem>
          
        <GridItem xs={12} sm={12} md={8}>
          <Card>
        <CardActionArea>
          <ReactSVG src = {this.state.categoryChart} />
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              Category Pie Chart
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              This is a pie chart shows the category distribution in this dataset.
            </Typography>
          </CardContent>
        </CardActionArea>
      
      </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={6}>
          <Card>
        <CardActionArea>
          <ReactSVG src = {this.state.countGeners} />
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              Count how many geners in this dataset.
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging
              across all continents except Antarctica
            </Typography>
          </CardContent>
        </CardActionArea>
      
      </Card>
          </GridItem>
        </GridContainer>
      </div>
    );
  }

  }