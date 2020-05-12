'use strict';

const e = React.createElement;

class Main extends React.Component {
  constructor(props){
    super(props);
  }






  render(){
    return(
        <div> test </div>
      )
   }
 }

const domContainer = document.querySelector('#react_main_container');
ReactDOM.render(< Main />, domContainer);