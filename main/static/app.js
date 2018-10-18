'use strict';

const e = React.createElement;

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    return(
      <div>
        <h1>rendered</h1>
        <button>Test</button>
      </div>
    );
  }
}

const domContainer = document.querySelector('#like_button_container');
ReactDOM.render(< Main />, domContainer);