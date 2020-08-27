'use strict';

import ViewTable from '/Components/ViewTable'

const e = React.createElement;

class ViewTable1 extends React.Component {
	constructor(props){
		super(props);

	}


	render(){
		return (
			<div>
				<span> View Table </span>
			</div>


			)
	}
}

class Main extends React.Component {
  constructor(props){
    super(props);
    this.state = {
    	view1: {model: 'test'},
    	view2: '2',
    	view3: null,
    	view4: null,
    	view5: null,
    	view6: null,
    	view7: null,
    	view8: null,
    	view9: null,
    	view10: null,
    	view11: null,
    	view12: null,
    	view13: null,
    	view14: null,
    	view16: null,
    	pulledSTBData: 'empty',
    }

  }


  componentDidMount(){
  	// set scoping for fetch function
  	var that = this;
  	

  	fetch('http://localhost:3000/stbs/JSON')
      .then(function(response){
        if(response.status==400){
          throw new Error("Bad Response for the server");
        }
        return response.json();
      })
      .then(function(data){
        console.log('response was good! stb data found')
        console.log(data.stbInfoData[0]);
        var dataArr = data.stbInfoData;

        that.setState({
        	pulledSTBData: data,
        })
      })
  }



  render(){
    return(
        <div>
        	<ViewTable />
        </div>
      )
   }
 }

const domContainer = document.querySelector('#react_main_container');
ReactDOM.render(< Main />, domContainer);