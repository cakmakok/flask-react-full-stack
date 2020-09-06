import React, { Component } from "react";
import axios from "axios";

export class Test extends Component {
  constructor(props) {
    super(props);
    this.state = {
      nextTodoId: 0,
      newTodoLabel: ""
    };
  }

  componentDidMount() {
    axios
      .get(
        "/brokers"
      )
      .then((data ) => {
      console.log(data)
      }).catch((err) => {console.log(err)});
  }

  render() {
      return (<div> Selam </div>)
  }
}

export default  Test;