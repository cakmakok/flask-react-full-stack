import React, {Component} from "react";
import axios from "axios";
import {withAlert} from 'react-alert'

export class RegisterNewBroker extends Component {

    constructor(props) {
        super(props);
        this.state = {
            firstname: "",
            lastname: "",
            email: "",
            address: "",
            loading: false
        };

    }

    onChange = e => {
        this.setState({[e.target.name]: e.target.value})
    }

    onSubmit = e => {
        e.preventDefault();
        this.setState({loading: true})
        const alert = this.props.alert;

        const {firstname, lastname, email, address} = this.state;
        const newBroker = {firstname, lastname, email, address};

        axios.post("/signup", newBroker).then(res => {
            console.log(res)
            alert.show(res.data)
            this.setState({loading: false})

            this.props.history.push("/");
        }).catch(err => {
            console.log(err)
            this.setState({loading: false})
            alert.show(err.response.data)
        })
    };

    render() {
        const loading = this.state.loading
        return (
            <>
                <h2>Sign up for New Broker</h2>
                <form onSubmit={this.onSubmit}>
                    <fieldset>
                        <div className="form-group">
                            <label>First Name</label>
                            <input
                                className="form-control"
                                type="text"
                                name="firstname"
                                required={true}
                                onChange={this.onChange}
                                value={this.state.firstname}
                            />
                        </div>
                        <div className="form-group">
                            <label>Last Name</label>
                            <input
                                className="form-control"
                                type="text"
                                name="lastname"
                                required={true}
                                onChange={this.onChange}
                                value={this.state.lastname}
                            />
                        </div>
                        <div className="form-group">
                            <label>E-Mail</label>
                            <input
                                className="form-control"
                                type="email"
                                name="email"
                                required={true}
                                onChange={this.onChange}
                                value={this.state.email}
                            />
                        </div>
                        <div className="form-group">
                            <label>Address</label>
                            <input
                                className="form-control"
                                type="text"
                                name="address"
                                required={true}
                                onChange={this.onChange}
                                value={this.state.address}
                            />
                        </div>
                    </fieldset>
                    {
                        loading ?
                            <button class="btn btn-primary" type="button" disabled>
                                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                Loading...
                            </button>
                            :
                            <button type="submit" className="btn btn-primary">Submit</button>

                    }

                </form>

            </>
        )
    }
}

export default withAlert()(RegisterNewBroker);