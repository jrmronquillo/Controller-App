'use strict';

const e = React.createElement;

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      liked: false,
      display: true,
      command: ''
    };
    this.toggleDisplay = this.toggleDisplay.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  componentDidMount(){
    document.addEventListener('keydown', this.handleKeyPress);
  }

  componentWillUnmount(){
    document.removeEventListener('keydown', this.handleKeyPress);
  }

  toggleDisplay(){
    this.setState({
      display: !this.state.display
      });
  }

  handleKeyPress(event){
    console.log(event.keyCode);
    var value = '';
    switch(event.keyCode){
      case 87:
        value = 'upArrow';
        break;
      case 65:
        value = 'leftArrow';
        break;
      case 68:
        value = 'rightArrow';
        break;
      case 83:
        value = 'downArrow';
        break;
      case 32:
        value = 'select';
        break;
      case 88:
        value = 'exit';
        break;
      case 69:
        value='guide';
        break;
      case 82:
        value= 'menu';
        break;
      // numbers
      case 48:
        value= '0';
        break;
      case 49:
        value= '1';
        break;
      case 50:
        value= '2';
        break;
      case 51:
        value= '3';
        break;
      case 52:
        value= '4';
        break;
      case 53:
        value= '5';
        break;
      case 54:
        value= '6';
        break;
      case 55:
        value= '7';
        break;
      case 56:
        value= '8';
        break;
      case 57:
        value= '9';
        break;
      default:
        value = 'unexpected keypress';
    }

    this.setState({
      command: value
    })

    if(value != 'unexpected keypress'){
      fetch('http://localhost:5000/redesign/command/'+value);
    }
    //fetch('https://jsonplaceholder.typicode.com/todos/1')
    //  .then(response => response.json())
    //  .then(json => console.log(json))

  }

  render() {
    if(this.state.display){
      return(
        <div className="row">
          <div className="col-md-5">
            <h1>{this.state.command}</h1>
            <h1>true</h1>
            <table className="table-style">
              <tr>
                <td>
                  <span className="letter-unused"> Q</span>

                </td>
                <td>
                  <span className={this.state.command =='upArrow'? 'letter lightblue-bg': 'letter'}> W </span> <br />
                </td>
                <td>
                  <span className={this.state.command =='guide'? 'letter lightblue-bg': 'letter'}> E </span>
                </td>
                <td>
                  <span className={this.state.command =='menu'? 'letter lightblue-bg': 'letter'}> R </span>
                </td>
              </tr>
            </table>
            <table className="table-style" >
              <tr>
                <td colSpan='1' width= "10%">
                </td>
                <td>
                  <span className={this.state.command =='leftArrow'? 'letter lightblue-bg': 'letter'}>A</span>
                </td>
                <td>
                  <span className={this.state.command =='downArrow'? 'letter lightblue-bg': 'letter'}>S</span>
                </td>
                <td>
                  <span className={this.state.command =='rightArrow'? 'letter lightblue-bg': 'letter'}>D</span>
                </td>
                <td>
                  <span className="letter-unused">F</span>
                </td>
                <td>
                  <span className="letter-unused">G</span>
                </td>
              </tr>
            </table>
              <table className="table-style" >
              <tr>
                <td colSpan='1' width= "10%">
                </td>
                <td>
                  <span className="letter-unused">Z</span>
                </td>
                <td>
                  <span className={this.state.command =='exit'? 'letter lightblue-bg': 'letter'}>X</span>
                </td>
                <td>
                  <span className="letter-unused">C</span>
                </td>
                <td>
                  <span className="letter-unused">V</span>
                </td>
              </tr>
            </table>
            <form method='post'>
              <input type='text' name='name' />
              <input type='submit' value='submit' />
            </form>
          </div>
          <div className="col-md-5">
             <h1>Test</h1>
             <table className="table-style">
              <tr>
                <td>
                  <span className="letter-unused"> Y</span>

                </td>
                <td>
                  <span className="letter">U</span> <br />
                </td>
                <td>
                  <span className="letter"> I</span>
                </td>
                <td>
                  <span className="letter"> O</span>
                </td>
                <td>
                  <span className="letter">P</span>
                </td>
              </tr>
            </table>
            <table className="table-style">
              <tr>
                <td colSpan='1' width= "10%">
                </td>
                <td>
                  <span className="letter-unused"> H</span>

                </td>
                <td>
                  <span className="letter">J</span> <br />
                  
                </td>
                <td>
                  <span className="letter"> K</span>
                </td>
                <td>
                  <span className="letter">L</span>
                </td>
                <td>
                  <span className="letter">&#59;</span>
                </td>
              </tr>
            </table>
            <table className="table-style">
              <tr>
                <td>
                  <span className="letter-unused"> B</span>

                </td>
                <td>
                  <span className="letter">N</span> <br />
                </td>
                <td>
                  <span className="letter"> M</span>
                </td>
                <td>
                  <span className="letter">&#44;</span>
                </td>
                <td>
                  <span className="letter">&#46;</span>
                </td>
              </tr>
            </table>
          </div>
      </div>
        )
    } else {
      return(
      <div>
        <h1>{this.state.command}</h1>
        <h1>rendered</h1>
        <form method='post'>
          <input type='text' name='name' />
          <input type='submit' value='submit' />
        </form>
      </div>
    )

    }

    
  }
}

const domContainer = document.querySelector('#react_main_container');
ReactDOM.render(< Main />, domContainer);