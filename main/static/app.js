'use strict';

const e = React.createElement;

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      liked: false,
      display: true,
      keyPressed: '',
      command: '',
      viewerConfig: [],
      viewerPosition: '',
      irnetboxMac: '',
      slot: '1-16'
    };
    this.toggleDisplay = this.toggleDisplay.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
    this.sendCommands = this.sendCommands.bind(this);
  }

  componentDidMount(){
    document.addEventListener('keypress', this.handleKeyPress);
  }

  componentWillUnmount(){
    document.removeEventListener('keypress', this.handleKeyPress);
  }

  toggleDisplay(){
    this.setState({
      display: !this.state.display
      });
  }

  sendCommands(){
    var mac_list = ['00-80-A3-A9-E3-7A', "00-80-A3-A2-D9-13", "00-80-A3-A9-E3-68", 
                 "00-80-A3-A9-E3-6A", "00-80-A3-A9-E3-7A", 
                 "00-80-A3-A9-DA-67", "00-80-A3-A9-E3-79", 
                 "00-80-A3-A9-E3-78", "00-80-A3-9E-67-37", 
                 "00-80-A3-9D-86-D5", "00-80-A3-9E-67-34",
                 "00-80-A3-9E-67-27", "00-80-A3-9D-86-CF",
                 "00-80-A3-9E-67-35", "00-20-4A-BD-C5-1D",
                 "00-80-A3-9D-86-D2", "00-80-A3-9E-67-3B",
                 "00-80-A3-9E-67-36", "00-80-A3-9E-67-32",
                 "00-80-A3-9D-86-D6", "00-80-A3-9D-86-D3",
                 "00-80-A3-9D-86-D1", "00-80-A3-9D-86-D0",
                 "00-20-4A-DF-64-55", "00-80-A3-A1-7C-3C",
                 "00-80-A3-A2-48-5C", "00-20-4A-DF-65-A0",
                 "00-80-A3-9E-67-3A"];


    console.log('viewerPosition: '+this.state.viewerPosition);
    console.log('command: '+this.state.command);
    console.log('irnetboxMac:'+this.state.irnetboxMac);
    console.log('slot state:'+this.state.slot);
    if(this.state.irnetboxMac && this.state.slot && this.state.command){
      console.log('if statement executed');
      console.log('http://localhost:3000/redesign/command/'+this.state.irnetboxMac+'/'+this.state.slot+'/'+this.state.command);
      fetch('http://localhost:3000/redesign/command/'+this.state.irnetboxMac+'/'+this.state.slot+'/'+this.state.command);
    } else {
      console.log('invalid mac, slot, command');
    }
  
  }

  handleKeyPress(event){
    console.log(event.keyCode);
    var key = '';
    switch(event.keyCode){
      case 119:
        key = 'w';
        break;
      case 97:
        key = 'a';
        break;
      case 100:
        key = 'd';
        break;
      case 115:
        key = 's';
        break;
      case 32:
        key = ' ';
        break;
      case 120:
        key = 'x';
        break;
      case 101:
        key='e';
        break;
      case 114:
        key= 'r';
        break;
      // numbers
      case 48:
        key= '0';
        break;
      case 49:
        key= '1';
        break;
      case 50:
        key= '2';
        break;
      case 51:
        key= '3';
        break;
      case 52:
        key= '4';
        break;
      case 53:
        key= '5';
        break;
      case 54:
        key= '6';
        break;
      case 55:
        key= '7';
        break;
      case 56:
        key= '8';
        break;
      case 57:
        key= '9';
        break;
      case 38:
        key= '&';
        break;
      case 42:
        key='*';
        break;
      case 40:
        key='(';
        break;
      case 41:
        key=')';
        break;
      case 117:
        key='u';
        break;
      case 94:
        key='^';
        break;
      case 121:
        key='y';
        break;
      case 104:
        key='h';
        break;
      case 110:
        key='n';
        break;
      case 106:
        key='j';
        break;
      case 109:
        key='m';
        break;
      case 105:
        key='i';
        break;
      case 107:
        key='k';
        break;
      case 44:
        key=',';
        break;
      case 40:
        key='(';
        break;
      case 111:
        key='o';
        break;
      case 108:
        key='l';
        break;
      case 46:
        key='.';
        break;
      case 102:
        key='f';
        break;
      case 103:
        key='g';
        break;
      case 122:
        key='z';
        break;
      case 99:
        key='c';
        break;
      case 118:
        key='v';
        break;
      case 98:
        key='b';
        break;
      case 96:
        key='`';
        break;
      case 116:
        key='t';
        break;
      case 112:
        key='p';
        break;
      case 45:
        key='-';
        break;
      case 113:
        key='q';
        break;
      case 59:
        key=';';
        break;
      case 39:
        key="'";
        break;
      case 91:
        key="[";
        break;
      case 92:
        key='&#92;';
        break;
      case 93:
        key=']';
        break;
      default:
        key = 'unexpected keypress';
    }

    this.setState({
      keyPressed: key,
    });
    console.log('keypress state:');
    console.log(this.state.keyPressed);

    var controlCommands = {
                            'w':'upArrow',
                            'a':'leftArrow',
                            's':'downArrow',
                            'd':'rightArrow',
                            'e':'menu',
                            'r':'red',
                            'x':'exit',
                            'c':'rewind',
                            'v':'play',
                            'b':'fastforward',
                            't':'chanup',
                            'q':'guide',
                            ' ':'select',
                            'f':'info',
                            'g':'chandown',
                            'z':'dash',
                            '1': '1',
                            '2': '2',
                            '3': '3',
                            '4': '4',
                            '5': '5',
                            '6': '6',
                            '7': '7',
                            '8': '8',
                            '9': '9',
                            '0': '0',
                            '`': 'prev'
                              };
    var viewerPositionMapping = {
                            '': '0',
                            '^':'1',
                            'y':'2',
                            'h':'3',
                            'n':'4',
                            '&':'5',
                            'u':'6', 
                            'j':'7',
                            'm':'8', 
                            '*':'9',
                            'i':'10',
                            'k':'11', 
                            ',':'12', 
                            '(':'13', 
                            'o':'14',
                            'l':'15',
                            '.':'16',
                            ')':'17',
                            '-':'18',
                            'p':'19'
                            };
    console.log('viewerPositionMapping')
    console.log(viewerPositionMapping[key]);                        
    var stbs = {
      '1': {macAddr: '00-80-A3-A9-E3-7A', slot: '8'},
      '2': {macAddr: '00-80-A3-A9-E3-6A', slot: '15'},
      '3': {macAddr: '00-80-A3-A9-E3-7A', slot: '5'},
      '4': {macAddr: '00-80-A3-A9-E3-6A', slot: '10'},
      '5': {macAddr: '00-80-A3-A9-E3-6A', slot: '14'},
      '6': {macAddr: '00-80-A3-A9-E3-6A', slot: '16'},
      '7': {macAddr: '00-80-A3-A9-E3-6A', slot: '9'},
      '8': {macAddr: '00-80-A3-A9-E3-6A', slot: '11'},
      '9': {macAddr: '00-80-A3-A9-E3-7A', slot: '1'},
      '10':{macAddr: '00-80-A3-A9-E3-6A', slot: '2'},
      '11':{macAddr: '00-80-A3-A9-E3-7A', slot: '2'},
      '12':{macAddr: '00-80-A3-A9-E3-6A', slot: '5'},
      '13':{macAddr: '00-80-A3-A9-E3-6A', slot: '1'},
      '14':{macAddr: '00-80-A3-A9-E3-6A', slot: '3'},
      '15':{macAddr: '00-80-A3-A9-E3-6A', slot: '4'},
      '16':{macAddr: '00-80-A3-A9-E3-6A', slot: '6'},
      '17':{macAddr: '00-80-A3-9D-86-D0', slot: '1-16'},
      '18':{macAddr: '00-80-A3-9D-86-D1', slot: '1-16'},
      '19':{macAddr: '00-80-A3-9D-86-D3', slot: '1-16'},

    };

    var multiviewConfig = {
                          '[':'1',
                          ']':'2',
                          '&#92;':'3',
                          ';':'4',
                          "'":'5'
                          };



    var macMapping = {
                          '1' :'00-80-A3-A9-E3-7A',
                          '2' :'00-80-A3-A9-E3-6A',
                          '3' :'00-80-A3-A9-E3-7A',
                          '17':'00-80-A3-9D-86-D0',
                          '18':'00-80-A3-9D-86-D1',
                          '19':'00-80-A3-9D-86-D3'
                            };

    if(stbs[viewerPositionMapping[key]]){
      this.setState({
        irnetboxMac: stbs[viewerPositionMapping[key]].macAddr,
        slot: stbs[viewerPositionMapping[key]].slot
      });
    }
    console.log('irnetboxMac state:');
    console.log(this.state.irnetboxMac);

    if(multiviewConfig[key]){
      //4 quadConf
      console.log('multiview config executed');
      console.log(multiviewConfig[key]);
      //fetch('http://localhost:3000/setVideo/redesign/4/');
      fetch('http://localhost:3000/setVideo/redesign/'+multiviewConfig[key]+'/');
    }

    if(controlCommands[key]){
      this.setState({
        command: controlCommands[key]
      });
      this.sendCommands();
    }
  }


    
    //fetch('https://jsonplaceholder.typicode.com/todos/1')
    //  .then(response => response.json())
    //  .then(json => console.log(json))

  

  render() {
    if(this.state.display){
      return(
        <div className="row">
          <div className="col-md-5">
            <h1>Controls </h1>
            <table className="table-style">
              <tr>
                <td className={this.state.keyPressed =='`'? 'letter lightblue-bg': 'letter'}>
                  <h1>prev</h1>
                  <span> ` (backtick)</span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='1'? 'letter lightblue-bg': 'letter'}> 1</span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='2'? 'letter lightblue-bg': 'letter'}> 2 </span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='3'? 'letter lightblue-bg': 'letter'}> 3 </span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='4'? 'letter lightblue-bg': 'letter'}> 4 </span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='5'? 'letter lightblue-bg': 'letter'}> 5 </span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='6'? 'letter lightblue-bg': 'letter'}> 6 </span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='7'? 'letter lightblue-bg': 'letter'}> 7 </span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='8'? 'letter lightblue-bg': 'letter'}> 8 </span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='9'? 'letter lightblue-bg': 'letter'}> 9 </span>
                </td>
                <td>
                  <span className={this.state.keyPressed =='0'? 'letter lightblue-bg': 'letter'}> 0 </span>
                </td>
              </tr>
            </table>
            <table className="table-style">
              <tr>
                <td className={this.state.keyPressed =='q'? 'letter lightblue-bg': 'letter'}>
                  <h1>GUIDE</h1>
                  <span> Q</span>
                </td>
                <td className={this.state.keyPressed =='w'? 'letter lightblue-bg': 'letter'}>
                  <h1>&uarr;</h1>
                  <span > W </span> <br />
                </td>
                <td className={this.state.keyPressed =='e'? 'letter lightblue-bg': 'letter'}>
                  <h1>MENU</h1>
                  <span> E </span>
                </td>
                <td className={this.state.keyPressed =='r'? 'letter lightblue-bg': 'letter'}>
                  <h1>RED</h1>
                  <span > R </span>
                </td>
                 <td className={this.state.keyPressed =='t'? 'letter lightblue-bg': 'letter'}>
                  <h1>&#9650;</h1>
                  <span > T </span>
                </td>
              </tr>
            </table>
            <table className="table-style" >
              <tr>
                <td colSpan='1' width= "10%"  className='hidden-top-border hidden-left-border hidden-bottom-border'>
                </td>
                <td className={this.state.keyPressed =='a'? 'letter lightblue-bg': 'letter'}>
                  <h1>&larr;</h1>
                  <span >A</span>
                </td>
                <td className={this.state.keyPressed =='s'? 'letter lightblue-bg': 'letter'}>
                  <h1>&darr;</h1>
                  <span >S</span>
                </td>
                <td className={this.state.keyPressed =='d'? 'letter lightblue-bg': 'letter'}>
                  <h1>&rarr;</h1>
                  <span >D</span>
                </td>
                <td className={this.state.keyPressed =='f'? 'letter lightblue-bg': 'letter'}>
                  <h1>INFO</h1>
                  <span>F</span>
                </td>
                <td className={this.state.keyPressed =='g'? 'letter lightblue-bg': 'letter'}>
                  <h1>&#9660;</h1>
                  <span>G</span>
                </td>
              </tr>
            </table>
              <table className="table-style" >
              <tr>
                <td colSpan='1' width= "10%"  className='hidden-top-border hidden-left-border hidden-bottom-border'>
                </td>
                <td colSpan='1' width= "10%"  className='hidden-top-border hidden-left-border hidden-bottom-border'>
                </td>
                <td className={this.state.keyPressed =='z'? 'letter lightblue-bg': 'letter'}>
                  <h1>DASH</h1>
                  <span>Z</span>
                </td>
                <td className={this.state.keyPressed =='x'? 'letter lightblue-bg': 'letter'}>
                  <h1>EXIT</h1>
                  <span>X</span>
                </td>
                <td className={this.state.keyPressed =='c'? 'letter lightblue-bg': 'letter'}>
                  <h1>REW</h1>
                  <span>C</span>
                </td>
                <td className={this.state.keyPressed =='v'? 'letter lightblue-bg': 'letter'}>
                  <h1>PLAY</h1>
                  <span>V</span>
                </td>
                 <td className={this.state.keyPressed =='b'? 'letter lightblue-bg': 'letter'}>
                  <h1>FFWD</h1>
                  <span>B</span>
                </td>
              </tr>
            </table>
            <p>key pressed: </p>
            <h1>{this.state.keyPressed}</h1>
            <p>command:</p>
            <h1>{this.state.command}</h1>
            <h1>true</h1>
            <form method='post'>
              <input type='text' name='name' />
              <input type='submit' key='submit' />
            </form>
          </div>
          <div className="col-md-5">
             <h1>Device Selector</h1>
             <table className="table-style">
              <tr>
                <td className={this.state.keyPressed =='^'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 1</h5>
                  <span> &#x5e;</span>
                </td>
                <td className={this.state.keyPressed =='&'? 'letter lightblue-bg': 'letter'}>
                <h5>STB 5</h5>
                  <span > &amp;</span>

                </td>
                <td className={this.state.keyPressed =='*'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 9</h5>
                  <span>*</span>
                </td>
                <td className={this.state.keyPressed =='('? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 13</h5>
                  <span> (</span>
                </td>
                <td className={this.state.keyPressed ==')'? 'letter lightblue-bg': 'letter'}>
                  <h5>hx2x rack B12</h5>
                  <span> )</span>
                </td>
                <td className={this.state.keyPressed =='-'? 'letter lightblue-bg': 'letter'}>
                  <h5>hx2x rack B11</h5>
                  <span className="letter">_</span>
                </td>
                <td className={this.state.keyPressed =='-'? 'letter lightblue-bg': 'letter'}>
                  <h5>unassigned</h5>
                  <span className="letter">=</span>
                </td>
              </tr>
            </table>
             <table className="table-style">
              <tr>
                <td colSpan='1' width= "10%" className='hidden-left-border hidden-bottom-border'>
                </td>
                <td className={this.state.keyPressed =='y'? 'letter lightblue-bg': 'letter'}>
                  <h5> STB 2 </h5>
                  <span> Y</span>
                </td>
                <td className={this.state.keyPressed =='u'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 6</h5>
                  <span>U</span>
                </td>
                <td className={this.state.keyPressed == 'i'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 10</h5>
                  <span>I</span>
                </td>
                <td className={this.state.keyPressed  =='o'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 14</h5>
                  <span> O</span>
                </td>
                <td className={this.state.keyPressed =='p'? 'letter lightblue-bg': 'letter'}>
                  <h5>hx2x rack B10</h5>
                  <span> P</span>
                </td>
                <td className={this.state.keyPressed =='['? 'letter lightblue-bg': 'letter'}>
                  <h5>Multiviewer Config 1</h5>
                  <span>[</span>
                </td>
                <td className={this.state.keyPressed ==']'? 'letter lightblue-bg': 'letter'}>
                  <h5>Multiviewer Config 2</h5>
                  <span>]</span>
                </td>
                <td className={this.state.keyPressed =="&#92;"? 'letter lightblue-bg': 'letter'}>
                  <h5>Multiviewer Config 3 (Rack A02/A03)</h5>
                  <span>&#92;</span>
                </td>
              </tr>
            </table>
            <table className="table-style">
              <tr>
                <td colSpan='1' width= "10%" className='hidden-top-border hidden-left-border hidden-bottom-border'>
                </td>
                <td colSpan='1' width= "10%"  className='hidden-top-border hidden-left-border hidden-bottom-border'>
                </td>
                <td className={this.state.keyPressed == 'h'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 3</h5>
                  <span>H</span>
                </td>
                <td className={this.state.keyPressed == 'j'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 7</h5>
                  <span>J</span>
                </td>
                <td className={this.state.keyPressed =='k'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 11</h5>
                  <span>K</span>
                </td>
                <td className={this.state.keyPressed =='l'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 15</h5>
                  <span>L</span>
                </td>
                <td className={this.state.keyPressed ==';'? 'letter lightblue-bg': 'letter'}>
                  <h5>MultiViewer Config 4 (Rack B12/B14)</h5>
                  <span className="letter">&#59;</span>
                </td>
                <td className={this.state.keyPressed =="'"? 'letter lightblue-bg': 'letter'}>
                  <h5>Multiviwer Config 5 (Rack B15/B16) </h5>
                  <span className="letter">&apos;</span>
                </td>
              </tr>
            </table>
            <table className="table-style">
              <tr>
                <td colSpan='1' width= "10%"  className='hidden-top-border hidden-left-border hidden-bottom-border'>
                </td>
                <td colSpan='1' width= "10%"  className='hidden-top-border hidden-left-border hidden-bottom-border'>
                </td>
                <td colSpan='1' width= "10%"  className='hidden-top-border hidden-left-border hidden-bottom-border'>
                </td>
                <td className={this.state.keyPressed =='n'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 4</h5>
                  <span> N</span>
                </td>
                <td className={this.state.keyPressed == 'm'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 8</h5>
                  <span>M</span>
                </td>
                <td className={this.state.keyPressed ==','? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 12</h5>
                  <span>&#44;</span>
                </td>
                <td className={this.state.keyPressed =='.'? 'letter lightblue-bg': 'letter'}>
                  <h5>STB 16</h5>
                  <span >&#46;</span>
                </td>
                <td className={this.state.keyPressed =='.'? 'letter lightblue-bg': 'letter'}>
                  <h5>unnassigned</h5>
                  <span>/</span>
                </td>
              </tr>
            </table>
            <p>viewer position:</p>
            <h1>{this.state.viewerPosition}</h1>
          </div>
      </div>
        )
    } else {
      return(
      <div>
        <h1>{this.state.keyPressed}</h1>
        <h1>rendered</h1>
        <form method='post'>
          <input type='text' name='name' />
          <input type='submit' key='submit' />
        </form>
      </div>
    )

    }

    
  }
}

const domContainer = document.querySelector('#react_main_container');
ReactDOM.render(< Main />, domContainer);