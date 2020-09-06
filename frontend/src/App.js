import React, {Component, Fragment} from "react";
import ReactDOM from "react-dom";
import {
    HashRouter as Router,
    Route,
    Switch,
    Redirect
} from "react-router-dom";


import Header from "./Header";
import ListBrokers from "./ListBrokers";
import RegisterNewBroker from "./RegisterNewBroker";
import {transitions, positions, Provider as AlertProvider} from 'react-alert'
import AlertTemplate from 'react-alert-template-basic'

const options = {
    // you can also just use 'bottom center'
    position: positions.BOTTOM_CENTER,
    timeout: 5000,
    offset: '30px',
    // you can also just use 'scale'
    transition: transitions.SCALE
}

class App extends Component {


    render() {
        return (
            <AlertProvider template={AlertTemplate} {...options}>
                <Router>
                    <Fragment>
                        <Header/>
                        <div className="container">
                            <Switch>
                                <Route exact path="/" component={ListBrokers}/>
                                <Route exact path="/sign-up" component={RegisterNewBroker}/>
                            </Switch>
                        </div>
                    </Fragment>
                </Router>
            </AlertProvider>

        );
    }
}

export default App;
