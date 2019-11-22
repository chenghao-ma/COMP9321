
import React,{Component} from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import CustomInput from "components/CustomInput/CustomInput.js";
import Button from "components/CustomButtons/Button.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardIcon from "components/Card/CardIcon.js";
import CardBody from "components/Card/CardBody.js";

import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import CardFooter from "components/Card/CardFooter.js";
// import {Button, Card, CardBody, CardHeader, Col, CustomInput, Form, FormGroup, Input, Label, Row} from 'reactstrap';
import { Col,  Form, FormGroup, Label, Input, FormText } from 'reactstrap';
import axios from 'axios';
import Typography from '@material-ui/core/Typography';

// import {
//     Col,
//     Form,
//     FormGroup,
//     Input,
//     Label,
//     Row,
//     Button,
//     FormText
//   } from 'reactstrap';
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
  
const useStyles = makeStyles(styles);
export default class PredictModel extends Component{

    constructor(props) {
        super(props);
        this.state = {
          
            Price:'',
            ageRating: '',
            genres: '',
            size: '',
            prediction:'',
        };
    
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.getPrediction= this.getPrediction.bind(this);
      }
    
      getPrediction()
      {
        this.setState({
            prediction: '1145125251'
        })
        console.log("set State")
        console.log(this.state)
    }
      handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        })
        // console.log(this.state.value)
      }
    handleSubmit = event => {
        event.preventDefault();
    
        // const user = {
        //   genres: this.state.genres,
        //   Price:this.state.Price,
        //   ageRating: this.state.ageRating,
        //   size: this.state.size,
          

        // };
    
        // axios.post(`https://jsonplaceholder.typicode.com/users`, { user })
        //   .then(res => {
        //     console.log(res);
        //     console.log(res.data);
        //   })
       this.getPrediction()
      }
    
  
    
render(){
  return (
        
    <div >
       <Form onSubmit={this.handleSubmit}>

       
      <GridContainer className="justify-content-center">
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader >
              <h4 className={useStyles.cardTitleWhite}>Model Prediction</h4>
    
            </CardHeader>
            <CardBody  style = {{fontSize:'20px'}}>
              <GridContainer >
               
                <GridItem xs={12} sm={12} md={5}>
                < FormText >*Price </ FormText>
                <Input
                    id="Price"
                    name="Price" 
                    required
                    // value={this.state.Price} 
                    onChange={this.handleChange}
                 
                  />
            
                </GridItem>
                <GridItem xs={12} sm={12} md={5}>
                    < FormText>*ageRating </ FormText>

                  <Input
                    required 
                    id="ageRating"
                    name="ageRating" 
                    // value={this.state.value} 
                    onChange={this.handleChange}
                 
                  />
                </GridItem>
               
              </GridContainer>
              <br>
              </br>
              <GridContainer>
                <GridItem xs={12} sm={12} md={5}>
                < FormText>*Genres </ FormText>
                <Input
                
                    id="genres"
                    name="genres"
                    required
                    onChange={this.handleChange}
                 
                  />
                </GridItem>
                <GridItem xs={12} sm={12} md={5}>
                < FormText>*size </ FormText>
                <Input
            
                    id="size"
                    name="size"
                    required
                    onChange={this.handleChange}
                 
                  />
                </GridItem>
              
              </GridContainer>
           </CardBody>
           
           <Button type="submit" >Start Prediting</Button>
          </Card>

          </GridItem >
  
                    </GridContainer> 
                    </Form>
      <Card>
      <CardActionArea>
        <CardHeader>
        <Typography>
       
       Prediction result
     </Typography>
        </CardHeader>
        <CardContent>
            
          <Typography variant="body2" color="textSecondary" component="p">
           you prediction result is :{this.state.prediction}
          </Typography>
        </CardContent>
      </CardActionArea>
    
    </Card>
{/* 
 <Card  md={20}>

            <Form>
                <FormGroup row>
                    <Label >Email</Label>
                    <Col  >
                    <Input   type="email" name="email" id="exampleEmail" placeholder="with a placeholder" />
                    </Col>
                </FormGroup>
                <FormGroup row>
                
                </FormGroup>
                
                </Form>
                </Card>  */}
            
   </div>
  );
}
}