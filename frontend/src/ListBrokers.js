import React, {Component} from "react";
import axios from "axios";

export class ListBrokers extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            brokers: []
        };
    }

    componentDidMount() {
        this.setState({loading: true})
        axios
            .get(
                "/brokers"
            )
            .then((res) => {
                this.setState({loading: false, brokers: res.data})

            }).catch((err) => {
            this.setState({loading: false})
        });
    }

    render() {
        const brokers = this.state.brokers;
        const loading = this.state.loading;
        return (

            <div>

                <h2> Registered Brokers </h2>

                {loading
                    ?
                    <div className="spinner-border text-info" role="status">
                        <span className="sr-only">Loading...</span>
                    </div>
                    :
                        brokers
                        ?
                        <table className="table table-responsive table-striped">
                            <thead>
                            <tr>
                                <th>First Name</th>
                                <th>Last Name</th>
                                <th>E-Mail</th>
                                <th>Address</th>
                                <th>Agency Name</th>
                                <th>Agency Domain</th>
                                <th/>
                            </tr>
                            </thead>
                            <tbody>
                            {brokers.map(broker => (
                                <tr key={broker.id}>
                                    <td>{broker.firstname}</td>
                                    <td>{broker.lastname}</td>
                                    <td>{broker.email}</td>
                                    <td>{broker.address}</td>
                                    <td>{broker.agency_name}</td>
                                    <td>{broker.agency_domain}</td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                            :
                            <div>No broker found</div>
                }
            </div>
        )
    }
}

export default ListBrokers;