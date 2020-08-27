'use strict';

const e = React.createElement;

class Search extends React.Component {
  constructor(props){
    super(props);
  }




  render(){
    return(
      <div >
        <span> test</span>
        <input placeholder="Search" />
        <div>
          {this.props.searchData}
        </div>
        <ul id="searchSuggestions">
        </ul>
      </div>
      )
  }
}



class MultiViewButtons extends React.Component {
  constructor(props){
    super(props);
  }

    render(){
      return( 
        <div>
          <h2>Modes </h2>
          <table className="table table-config-1">
              <thead>
                 <tr><th></th></tr>
              </thead>
              <tbody>
              <tr>
                <td className={this.props.keyPressed =='='? 'letter lightblue-bg': 'letter'}>
                  <div id="`" data-txt="guide" className="cell-text-container">
                    <span className="cell-text">Toggle 4x4/2x2</span><br />
                    <span> = </span>
                  </div>  
                </td>
                <td className={this.props.keyPressed =='+'? 'letter lightblue-bg': 'letter'}>
                  <div id="`" data-txt="guide" className="cell-text-container">
                    <span className="cell-text">Toggle Solo Mode</span><br />
                    <span>mode: {this.props.soloMode}</span> 
                    <span> + </span>
                  </div>  
                </td>
              </tr>
              <tr>
                <td className={this.props.keyPressed =='['? 'letter lightblue-bg': 'letter'}>
                  <div id="`" data-txt="guide" className="cell-text-container">
                    <span className="cell-text">A03</span><br />
                    <span> [ </span>
                  </div>  
                </td>
                <td className={this.props.keyPressed ==']'? 'letter lightblue-bg': 'letter'}>
                  <div id="`" data-txt="guide" className="cell-text-container">
                    <span className="cell-text">B12</span><br />
                    <span> ] </span>
                  </div>  
                </td>
                <td className={this.props.keyPressed =='&#92;'? 'letter lightblue-bg': 'letter'}>
                  <div id="`" data-txt="guide" className="cell-text-container">
                    <span className="cell-text">B11</span><br />
                    <span> &#92; </span>
                  </div>  
                </td>
                <td className={this.props.keyPressed ==';'? 'letter lightblue-bg': 'letter'}>
                  <div id="`" data-txt="guide" className="cell-text-container">
                    <span className="cell-text">B11</span><br />
                    <span> ; </span>
                  </div>  
                </td>
                <td className={this.props.keyPressed =='&apos;'? 'letter lightblue-bg': 'letter'}>
                  <div id="`" data-txt="guide" className="cell-text-container">
                    <span className="cell-text">B11</span><br />
                    <span> &apos;</span>
                  </div>  
                </td>
              </tr>
              </tbody>
          </table>
          
        </div>
      )
      ;
    }
  }

  class BackDrop extends React.Component {
    constructor(props){
      super(props);
    }

      render(){
        return(
          <div className={this.props.windowFocused ? 'backdrop-none' : 'backdrop-display'}>
            <p className="screensave-data">{this.props.displayData[0]}</p>
            <br />
            <p className="screensave-data">{this.props.displayData[1]}</p>
            <br />
            <p className="screensave-data">{this.props.displayData[2]}</p>
            <br />
          </div>
        )
      }
  } 

  class TestComponent extends React.Component{
    constructor(props){
      super(props);
    }

      render(){
        return(
          <div>
            <span> Test Component </span>
          </div>
        )
      }
  }


class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      availableRacks: [],
      deviceData: null,
      dataLoaded: false,
      searchActivated: false,
      searchResults: [],
      rackSelected: '',
      testSearchItems: ['config 1','config 2', 'config 3', 'config 4', 'config 5', 'config 6', 'config 7', 'sar', '4x4','3x3','2x2', 
                    'solo on', 'solo off', 'solo 1', 'solo 2', 'solo 3', 'solo 4', 'solo 5',
                    'solo 6', 'solo 7', 'solo 8', 'solo 9', 'solo 10', 'solo 11', 'solo 12',
                    'solo 13', 'solo 14', 'solo 15', 'solo 16', 'labels on', 'labels off',
                     'audio meters on', 'audio meters off'],
      testEnv: false, 
      liked: false,
      display: true,
      displaySearchBar: false,
      textBoxFocused: true,
      keyPressed: '',
      command: '',
      windowFocused: true,
      viewerConfig: [],
      keys: ['q','w', 'e', 'r', 't', 'y'],
      keyObjects: { 
                        q :'guide',
                        w :'upArrow',
                        e : 'menu',
                        r :'red',
                        t :'chanUp',
                      },
      viewerPosition: '',
      irnetboxMac: '',
      soloMode: false,
      slot: '1-16',
      stbLabels: ['HR34-700', 'HR25-100', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12','13', '14', '15', '16'],
      view1: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view2: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view3: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view4: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view5: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view6: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view7: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view8: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view9: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view10: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view11: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view12: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view13: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view14: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view15: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      view16: {macAddr:'', slot: '', model: '', vidRouteMoniker: ''},
      toggleTempView3: 'null',
      toggleTempView4: 'null',
      toggleTempView5: 'null',
      toggleTempView6: 'null',
      screenSaverData: 'null',
      rackSlotData:    'null',
      chosenConfig: 'multiviewerConfig1',
      multipleMacs: false,
      viewMode16: true,
      rssItems: 'null',
      jsonDataReceived: 'null',
      macsInConfig: [],
      configs: {
      'multiviewerConfig1': {
                           '1': {macAddr: '00-80-A3-A9-E3-7A', slot: '1', model: 'H44-100', vidRouteMoniker:'r3s1'}, 
                           '2': {macAddr: '00-80-A3-A9-E3-7A', slot: '2', model: 'HR54-700', vidRouteMoniker:'r3s2'},
                           '3': {macAddr: '00-80-A3-A9-E3-7A', slot: '3', model: 'HR54-500', vidRouteMoniker: 'r3s3'},
                           '4': {macAddr: '00-80-A3-A9-E3-7A', slot: '4', model: 'HR54-200', vidRouteMoniker: 'r3s4'},
                           '5': {macAddr: '00-80-A3-A9-E3-7A', slot: '5', model: 'HR44-700', vidRouteMoniker: 'r3s5'},
                           '6': {macAddr: '00-80-A3-A9-E3-7A', slot: '6', model: 'HR44-500', vidRouteMoniker: 'r3s6'},
                           '7': {macAddr: '00-80-A3-A9-E3-7A', slot: '7', model: 'HR44-200', vidRouteMoniker: 'r3s7'},
                           '8': {macAddr: '00-80-A3-A9-E3-7A', slot: '8', model: 'HR34-700', vidRouteMoniker: 'r3s8'},
                           '9': {macAddr: '00-80-A3-A9-E3-6A', slot: '1', model: 'C51-100(H44-500)', vidRouteMoniker: 'r2s1'},
                           '10': {macAddr: '00-80-A3-A9-E3-6A', slot: '2', model: 'C41-700(H44-500)', vidRouteMoniker: 'r2s2'},
                           '11': {macAddr: '00-80-A3-A9-E3-6A', slot: '3', model: 'C41-700(H44-500)', vidRouteMoniker: 'r2s3'},
                           '12': {macAddr: '00-80-A3-A9-E3-6A', slot: '4', model: 'C51-500(HR54R1-700)', vidRouteMoniker: 'r2s4'},
                           '13': {macAddr: '00-80-A3-A9-E3-6A', slot: '5', model: 'C61-700(HR54R1-700)', vidRouteMoniker: 'r2s5'},
                           '14': {macAddr: '00-80-A3-A9-E3-6A', slot: '6', model: 'C61w-700(HR54R1-700)', vidRouteMoniker: 'r2s6'},
                           '15': {macAddr: '00-80-A3-A9-E3-6A', slot: '7', model: 'C51-500(HR54-500)', vidRouteMoniker: 'r2s7'},
                           '16': {macAddr: '00-80-A3-A9-E3-6A', slot: '8', model: 'C41-700(HR54-200)', vidRouteMoniker: 'r2s8'},
                         },
      'multiviewerConfig2': {
                           '1': {macAddr: '00-80-A3-9D-86-D0', slot: '1', model: 'H24-100', vidRouteMoniker:'r13s1'}, 
                           '2': {macAddr: '00-80-A3-9D-86-D0', slot: '2', model: 'H24-200', vidRouteMoniker:'r13s2'},
                           '3': {macAddr: '00-80-A3-9D-86-D0', slot: '3', model: 'H24-700', vidRouteMoniker: 'r13s3'},
                           '4': {macAddr: '00-80-A3-9D-86-D0', slot: '4', model: 'H25-100', vidRouteMoniker: 'r13s4'},
                           '5': {macAddr: '00-80-A3-9D-86-D0', slot: '5', model: 'HR24-100', vidRouteMoniker: 'r13s5'},
                           '6': {macAddr: '00-80-A3-9D-86-D0', slot: '6', model: 'H25-700', vidRouteMoniker: 'r13s6'},
                           '7': {macAddr: '00-80-A3-9D-86-D0', slot: '7', model: 'H25-500', vidRouteMoniker: 'r13s7'},
                           '8': {macAddr: '00-80-A3-9D-86-D0', slot: '8', model: 'HR24-200', vidRouteMoniker: 'r13s8'},
                           '9': {macAddr: '00-80-A3-9D-86-D1', slot: '1', model: 'H21-100', vidRouteMoniker: 'r14s1'},
                           '10': {macAddr: '00-80-A3-9D-86-D1', slot: '2', model: 'H21-200', vidRouteMoniker: 'r14s2'},
                           '11': {macAddr: '00-80-A3-9D-86-D1', slot: '3', model: 'H23-600', vidRouteMoniker: 'r14s3'},
                           '12': {macAddr: '00-80-A3-9D-86-D1', slot: '4', model: 'HR20-100', vidRouteMoniker: 'r14s4'},
                           '13': {macAddr: '00-80-A3-9D-86-D1', slot: '5', model: 'HR20-700', vidRouteMoniker: 'r14s5'},
                           '14': {macAddr: '00-80-A3-9D-86-D1', slot: '6', model: 'HR21-100', vidRouteMoniker: 'r14s6'},
                           '15': {macAddr: '00-80-A3-9D-86-D1', slot: '7', model: 'HR22-100', vidRouteMoniker: 'r14s7'},
                           '16': {macAddr: '00-80-A3-9D-86-D1', slot: '8', model: 'HR24-500', vidRouteMoniker: 'r14s8'},
                         },
      'multiviewerConfig3': {
                           '1': {macAddr: '00-80-A3-9D-86-D1', slot: '1', model: 'H21-100', vidRouteMoniker: 'r14s1'},
                           '2': {macAddr: '00-80-A3-9D-86-D1', slot: '2', model: 'H21-200', vidRouteMoniker: 'r14s2'},
                           '3': {macAddr: '00-80-A3-9D-86-D1', slot: '3', model: 'H23-600', vidRouteMoniker: 'r14s3'},
                           '4': {macAddr: '00-80-A3-9D-86-D1', slot: '4', model: 'HR20-100', vidRouteMoniker: 'r14s4'},
                           '5': {macAddr: '00-80-A3-9D-86-D1', slot: '5', model: 'HR20-700', vidRouteMoniker: 'r14s5'},
                           '6': {macAddr: '00-80-A3-9D-86-D1', slot: '6', model: 'HR21-100', vidRouteMoniker: 'r14s6'},
                           '7': {macAddr: '00-80-A3-9D-86-D1', slot: '7', model: 'HR22-100', vidRouteMoniker: 'r14s7'},
                           '8': {macAddr: '00-80-A3-9D-86-D1', slot: '8', model: 'HR24-500', vidRouteMoniker: 'r14s8'},
                           '9': {macAddr: '00-80-A3-9D-86-D3', slot: '1', model: 'THR22-100', vidRouteMoniker: 'r15s1'},
                           '10': {macAddr: '00-80-A3-9D-86-D3', slot: '2', model: 'HR21-200', vidRouteMoniker: 'r15s2'},
                           '11': {macAddr: '00-80-A3-9D-86-D3', slot: '3', model: 'HR21P-200', vidRouteMoniker: 'r15s3'},
                           '12': {macAddr: '00-80-A3-9D-86-D3', slot: '4', model: 'R22-100', vidRouteMoniker: 'r15s4'},
                           '13': {macAddr: '00-80-A3-9D-86-D3', slot: '5', model: 'HR24-200', vidRouteMoniker: 'r15s5'},
                           '14': {macAddr: '00-80-A3-9D-86-D3', slot: '6', model: 'HR21-700', vidRouteMoniker: 'r15s6'},
                           '15': {macAddr: '00-80-A3-9D-86-D3', slot: '7', model: 'HR23-700', vidRouteMoniker: 'r15s7'},
                           '16': {macAddr: '00-80-A3-9D-86-D3', slot: '8', model: 'HR24-500', vidRouteMoniker: 'r15s8'},
                         },
      'multiviewerConfig4': {
                           '1': {macAddr: '00-80-A3-9E-67-3A', slot: '1', model: 'HS171', vidRouteMoniker:'r13s1'}, 
                           '2': {macAddr: '00-80-A3-9E-67-3A', slot: '2', model: 'HS172', vidRouteMoniker:'r13s2'},
                           '3': {macAddr: '00-80-A3-9E-67-3A', slot: '3', model: 'HS173', vidRouteMoniker: 'r13s3'},
                           '4': {macAddr: '00-80-A3-9E-67-3A', slot: '4', model: 'HS174', vidRouteMoniker: 'r13s4'},
                           '5': {macAddr: '00-80-A3-9E-67-3A', slot: '5', model: 'HS175', vidRouteMoniker: 'r13s5'},
                           '6': {macAddr: '00-80-A3-9E-67-3A', slot: '6', model: 'HS176', vidRouteMoniker: 'r13s6'},
                           '7': {macAddr: '00-80-A3-9E-67-3A', slot: '7', model: 'HS177', vidRouteMoniker: 'r13s7'},
                           '8': {macAddr: '00-80-A3-9E-67-3A', slot: '8', model: 'HS178', vidRouteMoniker: 'r13s8'},
                           '9': {macAddr: '00-80-A3-A9-E3-6A', slot: '1', model: '#', vidRouteMoniker: 'r14s1'},
                           '10': {macAddr: '00-80-A3-A9-E3-6A', slot: '2', model: '#', vidRouteMoniker: 'r14s2'},
                           '11': {macAddr: '00-80-A3-A9-E3-6A', slot: '3', model: '#', vidRouteMoniker: 'r14s3'},
                           '12': {macAddr: '00-80-A3-A9-E3-6A', slot: '4', model: '#', vidRouteMoniker: 'r14s4'},
                           '13': {macAddr: '00-80-A3-A9-E3-6A', slot: '5', model: '#', vidRouteMoniker: 'r14s5'},
                           '14': {macAddr: '00-80-A3-A9-E3-6A', slot: '6', model: '#', vidRouteMoniker: 'r14s6'},
                           '15': {macAddr: '00-80-A3-A9-E3-6A', slot: '7', model: '#', vidRouteMoniker: 'r14s7'},
                           '16': {macAddr: '00-80-A3-A9-E3-6A', slot: '8', model: '#', vidRouteMoniker: 'r14s8'},
                         },
      'multiviewerConfig5': {
                           '1': {'macAddr': '00-80-A3-9E-67-34', 'slot': '1', 'model': 'HR44-200', 'vidRouteMoniker':'r9s1'}, 
                           '2': {'macAddr': '00-80-A3-9E-67-34', 'slot': '2', 'model': 'Client', 'vidRouteMoniker':'r9s2'},
                           '3': {'macAddr': '00-80-A3-9E-67-34', 'slot': '3', 'model': 'client', 'vidRouteMoniker': 'r9s3'},
                           '4': {'macAddr': '00-80-A3-9E-67-34', 'slot': '4', 'model': 'client', 'vidRouteMoniker': 'r9s4'},
                           '5': {'macAddr': '00-80-A3-9E-67-34', 'slot': '5', 'model': 'HR44-500', 'vidRouteMoniker': 'r9s5'},
                           '6': {'macAddr': '00-80-A3-9E-67-34', 'slot': '6', 'model': 'client', 'vidRouteMoniker': 'r9s6'},
                           '7': {'macAddr': '00-80-A3-9E-67-34', 'slot': '7', 'model': 'client', 'vidRouteMoniker': 'r9s7'},
                           '8': {'macAddr': '00-80-A3-9E-67-34', 'slot': '8', 'model': 'client', 'vidRouteMoniker': 'r9s8'},
                           '9': {'macAddr': '00-80-A3-9E-67-34', 'slot': '9', 'model': 'HR44-700', 'vidRouteMoniker': 'r9s9'},
                           '10': {'macAddr': '00-80-A3-9E-67-34', 'slot': '10', 'model': 'client', 'vidRouteMoniker': 'r9s10'},
                           '11': {'macAddr': '00-80-A3-9E-67-34', 'slot': '11', 'model': 'client', 'vidRouteMoniker': 'r9s11'},
                           '12': {'macAddr': '00-80-A3-9E-67-34', 'slot': '12', 'model': 'client', 'vidRouteMoniker': 'r9s12'},
                           '13': {'macAddr': '00-80-A3-9E-67-34', 'slot': '13', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
                           '14': {'macAddr': '00-80-A3-9E-67-34', 'slot': '14', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
                           '15': {'macAddr': '00-80-A3-9E-67-34', 'slot': '15', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
                           '16': {'macAddr': '00-80-A3-9E-67-34', 'slot': '16', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
                         }
        },
    };
    this.toggleDisplay = this.toggleDisplay.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
    this.sendCommands = this.sendCommands.bind(this);
    this.focusTest = this.focusTest.bind(this);
    this.focused = this.focused.bind(this);
    this.focusFunction = this.focusFunction.bind(this);
    this.blurFunction = this.blurFunction.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.searchBarDisplay = this.searchBarDisplay.bind(this);
    this.setFocus = this.setFocus.bind(this);
    this.handleOffClick = this.handleOffClick.bind(this);
    this.setFocusState = this.setFocusState.bind(this);
    this.pushDataToView = this.pushDataToView.bind(this);
    this.setVideoRoutes = this.setVideoRoutes.bind(this);
    this.checkNull = this.checkNull.bind(this);
    this.clickToSearch = this.clickToSearch.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.init();
  }

  init(){
    console.log('init called');
    console.log('second comment');

  }

  componentDidMount(){
    console.log('00000000');
    var that = this;
    var rackNums;

    /**
     * load device info into app
     */
    fetch('http://localhost:3000/deviceInfo/')
      .then(function(response){
        if(response.status>=400){
          throw new Error('Bad Response for the server');
        }
        return response.json();
      })
      .then(function(deviceData){
        console.log("deviceData response was good, stb device info loading..")
        console.log(deviceData);

        // store the rack numbers (the keys) in an array and make sure they are upper case
        var racks = Object.keys(deviceData).map(v=>v.toUpperCase());                                                                                                                                                                                                                    
        var updatedSearchItems = that.state.testSearchItems.concat(racks);
        that.setState({
          deviceData: deviceData,
          dataLoaded: true,
          availableRacks: racks,
          testSearchItems: updatedSearchItems,
        })

      });


    // initialize temp view values so that they get be set to reset the views in the toggle function
    this.setState({
          toggleTempView3: this.state.view3,
          toggleTempView4: this.state.view4,
          toggleTempView5: this.state.view5,
          toggleTempView6: this.state.view6,
        });
    //console.log(navigator);
    //console.log(this.state.keyObjects.length);
    //console.log(this.state.keyObjects[0][0]);
    //for (var key in this.state.keyObjects[0][0]){
    //  console.log(key);
    //  console.log(this.state.keyObjects[0][0][key]);
    //}
    console.log('document focus var');
    console.log(document.hasFocus());

    //commented the lines below so the screensaver wouldn't interrupt debugging
    //window.addEventListener("blur", this.focusTest);
    //window.addEventListener("focus", this.focused);

    //document.addEventListener('click', this.handleClick);
    document.addEventListener('click', this.handleOffClick);

    document.addEventListener('keypress', this.handleKeyPress);
    
   /*
    fetch('http://localhost:3000/stbs/JSON')
      .then(function(response){
        if(response.status==400){
          throw new Error("Bad Response for the server");
        }
        return response.json();
      })
      .then(function(data1){
        console.log('response was good! stb data found')
        console.log(data1);
        var rackSlotsArr = data1.stbInfoData;
        this.setState({
          rackSlotData: rackSlotsArr,
        })

      })
    */

    // initial load of data
    fetch('http://localhost:3000/rssTest')
      .then(function(response){
        console.log('fetch function triggered!');
        if (response.status>= 400) {
          throw new Error("Bad response from the server");
        }
        return response.json();
      })
      .then(function(data){
        console.log('response was good!');
        console.log(data.title[0]);
        console.log(data.title.length);
        var screenSaverDataArr = [];
        for(var i=0; i<data.title.length; i++){
          screenSaverDataArr.push(data.title[i])
        }
        console.log(screenSaverDataArr);
        
        // generate a random integer and use that integer to select random item in an array of news articles.
        var j = 0;
        var ranThreeArticles = [];
        while(j < 3){
          var ranNum = Math.floor(Math.random() * screenSaverDataArr.length)
          console.log('ranNum:');
          console.log(ranNum);
          console.log(screenSaverDataArr[ranNum]);
          ranThreeArticles.push(screenSaverDataArr[ranNum])
          j++;
        }
        
        that.setState({
          screenSaverData: ranThreeArticles,
        });
      });


    // load new data into screenSaverData state every 5 mins
    setInterval(function(){
      fetch('http://localhost:3000/rssTest')
      .then(function(response){
        console.log('fetch function triggered!');
        if (response.status>= 400) {
          throw new Error("Bad response from the server");
        }
        return response.json();
      })
      .then(function(data){
        console.log('response was good!');
        console.log(data.title[0]);
        console.log(data.title.length);
        var screenSaverDataArr = [];
        for(var i=0; i<data.title.length; i++){
          screenSaverDataArr.push(data.title[i])
        }
        console.log(screenSaverDataArr);
        // generate a random integer and use that integer to select random item in an array of news articles.
        var j = 0;
        var ranThreeArticles = [];
        while(j < 3){
          var ranNum = Math.floor(Math.random() * screenSaverDataArr.length)
          console.log('ranNum:');
          console.log(ranNum);
          console.log(screenSaverDataArr[ranNum]);
          ranThreeArticles.push(screenSaverDataArr[ranNum])
          j++;
        }

        that.setState({
          screenSaverData: ranThreeArticles,
        });
      })
    }, 300000)
    /* will depecrate auto loading and moving to search logic
    this.getJsonTest(1);
    */

    this.logOutput();
  }

  componentWillUnmount(){
    document.removeEventListener('keypress', this.handleKeyPress);
    window.addEventListener("blur", this.focusTest);
    window.addEventListener('focus', this.focused);
  }

  logOutput(){
    console.log('&&&');
    console.log(this.state.jsonDataReceived);
  }



  getJsonTest(configVal){
    var that = this;
    fetch('http://localhost:3000/jsonTest/'+configVal+'/')
      .then(function(response){
        console.log('fetch function triggered!');
        if (response.status>= 400) {
          throw new Error("Bad response from the server");
        }
        return response.json();
      })
      .then(function(data){
        console.log('####response was good!####');
        console.log(data['fakeData']);
        //need santizaiton of data here?

        //set data to state.

        that.setState({
          jsonDataReceived: data['fakeData'],
          view1: data['fakeData']['1'],
          view2: data['fakeData']['2'],
          view3: data['fakeData']['3'],
          view4: data['fakeData']['4'],
          view5: data['fakeData']['5'],
          view6: data['fakeData']['6'],
          view7: data['fakeData']['7'],
          view8: data['fakeData']['8'],
          view9: data['fakeData']['9'],
          view10: data['fakeData']['10'],
          view11: data['fakeData']['11'],
          view12: data['fakeData']['12'],
          view13: data['fakeData']['13'],
          view14: data['fakeData']['14'],
          view15: data['fakeData']['15'],
          view16: data['fakeData']['16'],
          irnetboxMac: data['fakeData']['1']['macAddr']
          });

        });
  }

  getItems(){
    $.ajax({ 
    type: 'GET', 
    url: 'http://localhost:3000/rssTest', 
    data: { get_param: 'value' }, 
    dataType: 'json',
    success: function (data) { 
        console.log('test$$$');
        console.log(data.title[0]);
        this.setState({
          screenSaverData: data.title[0],
        })
      }
    });
  }

  handleClick(){
    console.log('Click registered!');
    console.log(document.activeElement.tagName);
  }

  toggleDisplay(){
    this.setState({
      display: !this.state.display
      });
  }

  setViewerPosition(viewerPos){
    this.setState({
      viewerPosition: viewerPos,
    })
    console.log('setViewerPosition')
  }

  searchBarDisplay(){
    console.log('changing search bar display');

    this.setState({
      displaySearchBar: true,
    });

    this.focusFunction();

 

  }

  focused(){
    console.log('screen is focused!');
    this.setState({
      windowFocused: true,
    })
  }

  focusTest(){
    console.log('window not focused!');
    this.setState({
      windowFocused: false,
    })
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


 

    // logic to send command to all unique macs in a config, it checks if multiple macs are in the config
    // and then for each mac calls a command api.
    if(this.state.multipleMacs){
      var newArr = this.state.macsInConfig.forEach(function(currVal){
        console.log('------');
        fetch('http://localhost:3000/redesign/command/'+currVal+'/'+this.state.slot+'/'+this.state.command); 
      }, this);
    }

    if(this.state.irnetboxMac && this.state.slot && this.state.command){
      console.log('if statement executed');
      console.log('http://localhost:3000/redesign/command/'+this.state.irnetboxMac+'/'+this.state.slot+'/'+this.state.command);
      fetch('http://localhost:3000/redesign/command/'+this.state.irnetboxMac+'/'+this.state.slot+'/'+this.state.command);
    } else {
      console.log('invalid mac, slot, command');
    }
  
  }

  sendVideoConfigs(){
    // fetch('http://localhost:3000/setVideo/')
  }

  sendLabelNames(){
    var stbLabelsArr = [
                        this.state.view1.model, this.state.view2.model, this.state.view3.model, this.state.view4.model,
                        this.state.view5.model, this.state.view6.model, this.state.view7.model, this.state.view8.model,
                        this.state.view9.model, this.state.view10.model, this.state.view11.model, this.state.view12.model,
                        this.state.view13.model, this.state.view14.model, this.state.view15.model, this.state.view16.model];
    console.log('sendlabelnames--> '+stbLabelsArr);
    
    var stbObjsArr = [this.state.view1, this.state.view2, this.state.view3, this.state.view4,
                      this.state.view5, this.state.view6, this.state.view7, this.state.view8,
                      this.state.view9, this.state.view10, this.state.view11, this.state.view12,
                      this.state.view13, this.state.view14, this.state.view15, this.state.view16];
    var labelsArr = [];
    // convert empty model to rack/slot position
    for(let i=0; i<stbObjsArr.length; i++){
      var tempModelVar;
      // if model is empty, convert it to vidroutemoniker instead
      if(stbObjsArr[i].model==''){ 
        tempModelVar = stbObjsArr[i].vidRouteMoniker;
        } else {
          tempModelVar = stbObjsArr[i].model;
        }

        labelsArr.push(tempModelVar);
    }

    console.log('labelsArr:'+labelsArr);
        
    if(stbLabelsArr.length == 16){
      //var commandStr = 'http://localhost:3000/setLabels/'+stbLabelsArr.join('/');
      var commandStr = 'http://localhost:3000/setLabels/'+labelsArr.join('/');
      console.log(commandStr);
      fetch(commandStr);
    } else{
      console.log('Number of stb labels does not equal 16');
    }
  }

  checkNull(item){
    console.log('[checkNull]')
    console.log(item)
    return item !='';
  }

  setVideoRoutes(){
    // check if routes were configured
    var vidRoutesArr = [this.state.view1.vidRouteMoniker,
                        this.state.view2.vidRouteMoniker,
                        this.state.view3.vidRouteMoniker,
                        this.state.view4.vidRouteMoniker,
                        this.state.view5.vidRouteMoniker,
                        this.state.view6.vidRouteMoniker,
                        this.state.view7.vidRouteMoniker,
                        this.state.view8.vidRouteMoniker,
                        this.state.view9.vidRouteMoniker,
                        this.state.view10.vidRouteMoniker,
                        this.state.view11.vidRouteMoniker,
                        this.state.view12.vidRouteMoniker,
                        this.state.view13.vidRouteMoniker,
                        this.state.view14.vidRouteMoniker,
                        this.state.view15.vidRouteMoniker,
                        this.state.view16.vidRouteMoniker]


    var setVideoCall = 'http://localhost:3000/setVideo/'+this.state.view1.vidRouteMoniker+'/'
                                                           +this.state.view2.vidRouteMoniker+'/'
                                                           +this.state.view3.vidRouteMoniker+'/'
                                                           +this.state.view4.vidRouteMoniker+'/'
                                                           +this.state.view5.vidRouteMoniker+'/'
                                                           +this.state.view6.vidRouteMoniker+'/'
                                                           +this.state.view7.vidRouteMoniker+'/'
                                                           +this.state.view8.vidRouteMoniker+'/'
                                                           +this.state.view9.vidRouteMoniker+'/'
                                                           +this.state.view10.vidRouteMoniker+'/'
                                                           +this.state.view11.vidRouteMoniker+'/'
                                                           +this.state.view12.vidRouteMoniker+'/'
                                                           +this.state.view13.vidRouteMoniker+'/'
                                                           +this.state.view14.vidRouteMoniker+'/'
                                                           +this.state.view15.vidRouteMoniker+'/'
                                                           +this.state.view16.vidRouteMoniker+'/'
  
    if(vidRoutesArr.indexOf('') < 0){

      console.log('setVideoCall--->'+setVideoCall);
            
      fetch(setVideoCall);
    } else {
      console.log('Error: Invalid set video call: ' + setVideoCall)
    }

    

  }

  pushDataToView(){
    var rackSelection = this.state.searchResults[0];
    var keysArr = Object.keys(this.state.deviceData[rackSelection]);
    var addedMacSlotArr = [];
    for(let i=1; i<=keysArr.length-1; i++){
      var tempObj = this.state.deviceData[rackSelection][i.toString()]

      tempObj['macAddr'] = this.state.deviceData[rackSelection]['macAddr'];
      tempObj['slot'] = i;
      
      
      // convert empty vidRouteMoniker to null to be compatible with setVideo api
      if(tempObj['vidRouteMoniker'] == ''){
        tempObj['vidRouteMoniker'] = 'null';
      }


      addedMacSlotArr.push(tempObj);
    }
    
    // load rack info into 'Device Selector View'
    this.setState({
      view1: addedMacSlotArr[0],
      view2: addedMacSlotArr[1],
      view3: addedMacSlotArr[2],
      view4: addedMacSlotArr[3],
      view5: addedMacSlotArr[4],
      view6: addedMacSlotArr[5],
      view7: addedMacSlotArr[6],
      view8: addedMacSlotArr[7],
      view9: addedMacSlotArr[8],
      view10: addedMacSlotArr[9],
      view11: addedMacSlotArr[10],
      view12: addedMacSlotArr[11],
      view13: addedMacSlotArr[12],
      view14: addedMacSlotArr[13],
      view15: addedMacSlotArr[14],
      view16: addedMacSlotArr[15],
      irnetboxMac: this.state.deviceData[rackSelection]['macAddr'],
    });
  }

  handleKeys_textbox(key){
    console.log('handleKeys_textbox triggered '+key);
    if(key == 13){
      console.log('enter key detected');
      console.log(this.state.searchResults);

      // check if entry is a rack number
      if(this.state.availableRacks.indexOf(this.state.searchResults[0]) > 0){
        console.log('should be a qualified rack');
        this.setState({
          rackSelected: this.state.searchResults[0],
        })
        this.pushDataToView();
        this.setVideoRoutes();

        // setLabels
        this.sendLabelNames();

      } else {
        console.log('configs-->')

        switch(this.state.searchResults[0]){
        case 'config 1': 
          console.log('A03 was entered')
          this.setVideoRouteConfig(1);
          break;
        case 'config 2':
          console.log('config 2 was entered');
          this.setVideoRouteConfig(2);
          break;
        case 'config 3':
          console.log('config 3 was entered');
          this.setVideoRouteConfig(3);
          break;
        case 'config 4':
          console.log('config 4 was entered');
          this.setVideoRouteConfig(4);
          break;
        case 'config 5':
          console.log('config 5 was entered');
          this.setVideoRouteConfig(5);
          break;
        case 'config 6':
          console.log('config 6 - rack A06 was entered');
          this.setVideoRouteConfig(6);
        case 'config 7':
          console.log('config 7 - b12;b11')
          this.setVideoRouteConfig(7);
        case '4x4':
          console.log('4x4 config was entered')
          this.setGridCall('4x4');
          break;
        case '2x2':
          console.log('2x2 config was entered')
          this.setGridCall('2x2');
          break;
        case '3x3':
          console.log('3x3 config was entered')
          this.setGridCall('3x3');
          break;
        case 'SOLO ON':
          console.log('solo on was entered')
          this.setSoloMode('true');
          break;
        case 'SOLO OFF':
          console.log('solo off was entered')
          this.setSoloMode('false');
          break;
        case 'SOLO 1':
          console.log('solo 1 was entered')
          this.setSoloPosition('1');
          this.setViewerPosition('1');
          break;
        case 'SOLO 2':
          console.log('solo 2 was entered')
          this.setSoloPosition('2');
          this.setViewerPosition('2');
          break;
        case 'SOLO 3':
          console.log('solo 3 was entered')
          this.setSoloPosition('3');
          this.setViewerPosition('3');
          break;
        case 'SOLO 4':
          console.log('solo 4 was entered')
          this.setSoloPosition('4');
          this.setViewerPosition('4');
          break;
        case 'SOLO 5':
          console.log('solo 5 was entered')
          this.setSoloPosition('5');
          this.setViewerPositin('5');
          break;
        case 'SOLO 6':
          console.log('solo 6 was entered')
          this.setSoloPosition('6');
          this.setViewerPosition('6');
          break;
        case 'SOLO 7':
          console.log('solo 7 was entered')
          this.setSoloPosition('7');
          this.setViewerPosition('7');
          break;
        case 'SOLO 8':
          console.log('solo 8 was entered')
          this.setSoloPosition('8');
          this.setViewerPosition('8');
          break;
        case 'SOLO 9':
          console.log('solo 9 was entered')
          this.setSoloPosition('9')
          this.setViewerPosition('9');
          break;
        case 'SOLO 10':
          console.log('solo 10 was entered');
          this.setSoloPosition('10');
          this.setViewerPosition('10');
          break;
        case 'SOLO 11':
          console.log('solo 11 was entered');
          this.setSoloPosition('11');
          this.setViewerPosition('11');
          break;
        case 'SOLO 12':
          console.log('solo 12 was entered');
          this.setSoloPosition('12');
          this.setViewerPosition('12');
          break;
        case 'SOLO 13':
          console.log('solo 13 was entered');
          this.setSoloPosition('13');
          this.setViewerPosition('13');
          break;
        case 'SOLO 14':
          console.log('solo 14 was entered');
          this.setSoloPosition('14');
          this.setViewerPosition('14');
          break;
        case 'SOLO 15':
          console.log('solo 15 was entered');
          this.setSoloPosition('15');
          this.setViewerPosition('15');
          break;
        case 'SOLO 16':
          console.log('solo 16 was entered');
          this.setSoloPosition('16');
          this.setViewerPosition('16');
          break;
        case 'LABELS ON':
          console.log('labels on was entered')
          this.setLabelsMode('true');
          break;
        case 'LABELS OFF':
          console.log('labels off was entered');
          this.setLabelsMode('false');
          break;
        case 'AUDIO METERS ON':
          console.log('audio meters on was entered')
          this.setAudioMeters('true');
          break;
        case 'AUDIO METERS OFF':
          console.log('audio meters off was entered')
          this.setAudioMeters('false');
          break;
        default:
          console.log('error with search results')
          console.log(this.state.searchResults[0]);
        }
      }

      
      console.log('triggering blurfunction after enter key');
      this.blurFunction();
    }
  }

  handleKeys_default(inputKey){
    console.log('handleKeys_default triggered! '+ inputKey)
     var key = '';
    switch(inputKey){
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
        key="&apos;";
        break;
      case 90:
        key='Z';
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
      case 86:
        key='V';
        break;
      case 47:
        key='/';
        break;
      case 61:
        key='=';
        break;
      case 43:
        key='+'
        break;
      case 13:
        key='enter'
        break;
      case 63:
        key='?'
        break;
      case 71:
        key='G'
        break;
      default:
        key = 'unexpected keypress';
      }

      console.log('key translated to'+key)
      this.setState({
        keyPressed: key,
      });
      console.log('keypress state:');
      console.log(this.state.keyPressed);

      if(key=='?'){
        console.log('question mark detected');
        this.setFocusState();
        this.setFocus();
        this.clearSearchBox();
        this.setFocus();
      }

    var controlCommands = {
                              'Z':'back',
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
                              'V':'record',
                              'G': 'pause',
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
                          'test':'0',
                          '^': '1',
                          'y': '2',
                          'h': '3',
                          'n': '4',
                          '&': '5',
                          'u': '6',
                          'j': '7',
                          'm': '8',
                          '*': '9',
                          'i': '10',
                          'k': '11',
                          ',': '12',
                          '(': '13',
                          'o': '14',
                          'l': '15',
                          '.': '16',
    };

    var viewerPositionConversion = {
      '1': this.state.view1,
      '2': this.state.view2,
      '3': this.state.view3,
      '4': this.state.view4,
      '5': this.state.view5,
      '6': this.state.view6,
      '7': this.state.view7,
      '8': this.state.view8,
      '9': this.state.view9,
      '10': this.state.view10,
      '11': this.state.view11,
      '12': this.state.view12,
      '13': this.state.view13,
      '14': this.state.view14,
      '15': this.state.view15,
      '16': this.state.view16,
    }
    /* will depecrate below and moving to search feature logic instead of key shortcuts
    var multiviewAPI = {
                        '=':'toggleLayout',
                        '+':'toggleSolo',
                        };

    var multiviewConfig = {
                            '[': 1,
                            ']': 2,
                            '&#92;':3,
                            ';':4,
                            "&apos;":5,
                            };
    */
    if(viewerPositionMapping[key]){
      console.log('viewerPositionMapping');
      console.log(viewerPositionMapping[key]);
      console.log('[handleKeys - viewerpositionmapping]')
      this.setState({
        irnetboxMac: viewerPositionConversion[viewerPositionMapping[key]].macAddr,
        slot: viewerPositionConversion[viewerPositionMapping[key]].slot,
        viewerPosition: viewerPositionMapping[key],
      })
    } else if(key == '/'){
      this.setState({
        slot: '1-16',
      })
    }else{
      console.log('viewerPositionMapping key not found');
      //this.setState({
      //  slot: '1-16',
      //})
    }

    if(controlCommands[key]){
      console.log('command key detected');
      console.log(controlCommands[key]);
      this.setState({
          command: controlCommands[key]
        });
      this.sendCommands();
    }

    /* will deprecate and move toward search logid instead of key shortcuts
    if(multiviewConfig[key]){
      console.log('multiviewConfig[key] detected')
      this.getJsonTest(multiviewConfig[key]);
      var setVideoCall = 'http://localhost:3000/setVideo/'+this.state.view1.vidRouteMoniker+'/'
                                                           +this.state.view2.vidRouteMoniker+'/'
                                                           +this.state.view3.vidRouteMoniker+'/'
                                                           +this.state.view4.vidRouteMoniker+'/'
                                                           +this.state.view5.vidRouteMoniker+'/'
                                                           +this.state.view6.vidRouteMoniker+'/'
                                                           +this.state.view7.vidRouteMoniker+'/'
                                                           +this.state.view8.vidRouteMoniker+'/'
                                                           +this.state.view9.vidRouteMoniker+'/'
                                                           +this.state.view10.vidRouteMoniker+'/'
                                                           +this.state.view11.vidRouteMoniker+'/'
                                                           +this.state.view12.vidRouteMoniker+'/'
                                                           +this.state.view13.vidRouteMoniker+'/'
                                                           +this.state.view14.vidRouteMoniker+'/'
                                                           +this.state.view15.vidRouteMoniker+'/'
                                                           +this.state.view16.vidRouteMoniker+'/'


          console.log('setVideoCall--->'+setVideoCall);
          
          fetch(setVideoCall);

          this.sendLabelNames();
    }*/
    
  }

  clearSearchBox(){
    console.log('clearSearchBox triggered!');
    console.log('[clearSearchBox] active element:'+document.activeElement.tagName);
    document.getElementById('testInput').value='';
  }

  setVideoRouteConfig(configKey){
    this.getJsonTest(configKey);
    var setVideoCall = 'http://localhost:3000/setVideo/'+this.state.view1.vidRouteMoniker+'/'
                                                         +this.state.view2.vidRouteMoniker+'/'
                                                         +this.state.view3.vidRouteMoniker+'/'
                                                         +this.state.view4.vidRouteMoniker+'/'
                                                         +this.state.view5.vidRouteMoniker+'/'
                                                         +this.state.view6.vidRouteMoniker+'/'
                                                         +this.state.view7.vidRouteMoniker+'/'
                                                         +this.state.view8.vidRouteMoniker+'/'
                                                         +this.state.view9.vidRouteMoniker+'/'
                                                         +this.state.view10.vidRouteMoniker+'/'
                                                         +this.state.view11.vidRouteMoniker+'/'
                                                         +this.state.view12.vidRouteMoniker+'/'
                                                         +this.state.view13.vidRouteMoniker+'/'
                                                         +this.state.view14.vidRouteMoniker+'/'
                                                         +this.state.view15.vidRouteMoniker+'/'
                                                         +this.state.view16.vidRouteMoniker+'/'


    console.log('setVideoCall--->'+setVideoCall);
          
    fetch(setVideoCall);

    this.sendLabelNames();

  }

  activateVideoRouteConfig(){

  }

  handleKeyPress(event){
    console.log('handleKeyPress triggered');
    console.log('textboxfocus state-->'+this.state.textBoxFocused);

    // textbox focused redo
    if(!this.state.searchActivated){
      this.handleKeys_default(event.keyCode);
    } else {
      this.handleKeys_textbox(event.keyCode);
    }

    /*
    // if textbox is focused handle keys differently
    if(this.state.textBoxFocused){
      this.handleKeys_default(event.keyCode);
    } else {
      this.handleKeys_textbox(event.keyCode);
    }*/
}


   focusFunction(){
    console.log('focusFunction triggered!');
    var elem2focus = document.getElementById('searchBox1');
    console.log('elem2focus:'+elem2focus.tagName);
    //this.setState({
    //  textBoxFocused: false,
    //})
    elem2focus.focus();

    console.log('activeElem: '+ document.activeElement.tagName);
    console.log('reached end of focusFunction');
  }

  blurFunction(){
    console.log('blurFunction triggered!');

    // remove focus from input element 
    var inputElem2Blur = document.getElementById('search-new');
    inputElem2Blur.blur();


    // clear the text box so that so that it is clear next time it is triggered
    document.getElementById('searchInputBox').value='';
    document.getElementById('search-new').value='';
    
    this.setState({
      textBoxFocused: true,
      searchActivated: false,
      displaySearchBar: false,
    })

    var searchInputBar = document.getElementById('testInput')
    var searchSuggestions = document.getElementById('searchSuggesions')
    searchInputBar.style.display ='none';
    //searchSuggestions.style.display = 'none';

    console.log('activeElem: '+document.activeElement.tagName);
  }

  updateSearchSuggestions(){

  }


  setGridCall(gridConfig){
    var validConfigs = ['2x2', '3x3', '4x4']
    if(validConfigs.indexOf(gridConfig) > -1){
      var setGridCall = 'http://localhost:3000/redesign/multiview/setGrid/'+ gridConfig +'/'
      console.log(setGridCall);
      fetch(setGridCall);
    }
  }

  setSoloMode(mode){
    // mode should only be true or false
    var validVars = ['true', 'false']
    console.log('toggleSolo triggered!');
    console.log(this.state.soloMode)

    //var setSoloCall = 'http://localhost:3000/redesign/setSolo/'+this.state.soloMode;
    var setSoloCall = 'http://localhost:3000/redesign/setSolo/'+mode;
    console.log('setSolo call:'+setSoloCall)
    console.log(validVars.indexOf(mode))
    if(validVars.indexOf(mode)>-1){
      fetch(setSoloCall);
    }
    this.setState({
      soloMode: !this.state.soloMode,
    })
    //break;
  }



  setSoloPosition(position){
    var validPositions = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
                          '11', '12', '13', '14', '15', '16'];

    var setSoloPositionCall = 'http://localhost:3000/redesign/setSoloPosition/'+position
    console.log('setSoloPosition call:'+setSoloPositionCall)
    if(validPositions.indexOf(position)>-1){
      fetch(setSoloPositionCall);
    }

  }

  setLabelsMode(labelsMode){
    var setLabelsModeCall = 'http://localhost:3000/redesign/labelsMode/'+labelsMode
    fetch(setLabelsModeCall);
  }

  setAudioMeters(mode){
    console.log('setAudioMeters function executed')
    var setAudioMetersCall = 'http://localhost:3000/redesign/audioMeters/'+mode
    console.log(setAudioMetersCall);
    fetch(setAudioMetersCall);
  }

  setFocusState(){
    console.log('setFocusState Triggered!');
     this.setState({
      textBoxFocused: false,
    })
  }

  setFocus(){
    console.log('setFocus function triggered');
    //var elemTestContainer = document.getElementById('searchInputBox-container')
    var elemTest = document.getElementById('searchInputBox');
    console.log('setFocus elements declared');
    elemTest.style.display ='block';
    //elemTestContainer.focus();
    //document.getElementById('searchInputBox').focus();
    elemTest.focus();
    console.log('value:'+elemTest.value);
    console.log('focus functions executed');

    //seting state to ____
   
    console.log('active element>'+document.activeElement.tagName);
  }


  clickToSearch(){
    console.log('clicktosearch called!');
    this.setState({
      searchActivated: true,
      searchResults: [],
    });


   
  }

  handleOffClick(){
    console.log('handleOffClick Triggered');
    console.log(document.activeElement.tagName);
    if(document.activeElement.tagName == 'BODY'){
      this.blurFunction();
    }
    //this.blurFunction();
  }


  handleChange(event){
    /*var valueArr = ['config 1','config 2', 'config 3', 'config 4', 'config 5', 'config 6', 'config 7', 'sar', '4x4','3x3','2x2', 
                    'solo on', 'solo off', 'solo 1', 'solo 2', 'solo 3', 'solo 4', 'solo 5',
                    'solo 6', 'solo 7', 'solo 8', 'solo 9', 'solo 10', 'solo 11', 'solo 12',
                    'solo 13', 'solo 14', 'solo 15', 'solo 16', 'labels on', 'labels off',
                     'audio meters on', 'audio meters off']
    */
    // convert all search items strings to upper case
    var valueArr = this.state.testSearchItems.map(item=>item.toUpperCase());
    console.log(this.state.testSearchItems);
    console.log('handleChange triggered');
    console.log('event.target.value:'+event.target.value);
    // convert value to upper case
    var upperCaseVar = event.target.value.toUpperCase();
    console.log('upperCase'+upperCaseVar);

    // this makes sure the search box is cleared of any text when it launches by the ? key
    if (event.target.value == '?' ){
      document.getElementById('searchInputBox').value='';
    }
    
    var filteredArr = [];
    for(var i=0; i<valueArr.length; i++){
      console.log('inside for loop')
      console.log(valueArr[i]);

      console.log('checking index:');
      console.log(valueArr[i].indexOf(event.target.value));
      if(valueArr[i].indexOf(upperCaseVar) > -1){
        filteredArr.push(valueArr[i]);
      } 
      console.log('filtered arr:');
      console.log(filteredArr);

      var searchSugg = document.getElementById('searchSuggestions');
      var newElemA = document.createElement("UL");
      newElemA.id='default1';
      newElemA.classList.add('list-group', 'searchItemCenter')

      filteredArr.forEach(function(searchItemA){
        var listElemA = document.createElement("LI")
        listElemA.classList.add('searchListItems');
        var textNodeA = document.createTextNode(searchItemA);
        listElemA.appendChild(textNodeA);
        newElemA.appendChild(listElemA);
      })
      var searchSugg = document.getElementById('searchSuggestions');
      searchSugg.replaceChild(newElemA, document.getElementById('default1'));

      this.setState({
        searchResults: filteredArr,
      })
    }


    var output = valueArr.filter(item=>event.target.value==item)
    console.log(valueArr);
    console.log(output);
    /*
    var searchSugg = document.getElementById('searchSuggestions')
    var newElem = document.createElement("UL");
    newElem.id='default1';
    var testVar = this.state.searchResults.forEach(function(searchItem){
      var listElem = document.createElement("LI")
      var textNode = document.createTextNode(searchItem);
      listElem.appendChild(textNode);
      newElem.appendChild(listElem);
    })
    console.log(testVar)
    searchSugg.replaceChild(newElem, document.getElementById('default1'));
    */
    

    
  }


    
    //fetch('https://jsonplaceholder.typicode.com/todos/1')
    //  .then(response => response.json())
    //  .then(json => console.log(json))

  

  render() {
    if(this.state.display){
      return(
        <div className="containerMain">
          <div className="header-spacer"></div>
          <div> 
            Device Data loaded:{this.state.dataLoaded ? "Yes":"No"}

          </div>
          <div className="search-new-container">
            <span>
              <i className="fas fa-search padding-sm icon-inline"></i>
              <input id='search-new' type="text" className="form-control search-button" onChange={this.handleChange} 
                    onFocus={this.clickToSearch} placeholder="Type to Search Features and press 'Enter' ">
              </input>
            </span>

            <div id="searchSuggestions" className={this.state.searchActivated ? "searchContainer" : "searchContainer-none"}  >
                <ul id='default1' >
                </ul>
                
            </div>
          </div>
          <div className={this.state.searchActivated ? "backdrop-display-new": ""}></div>
          <BackDrop windowFocused={this.state.windowFocused} displayData={this.state.screenSaverData} />
            <div className={this.state.textBoxFocused ? 'search-backdrop-invisible':'search-backdrop'} onClick={this.handleOffClick}></div>
            <div className="testInput_container">
              <i className="fas fa-search search-icon"></i>
            </div>

            <div id='searchInputBox-container' className={this.state.textBoxFocused ? "hide input-group mb-3" : 'input-group mb-3 input-customize' }>
              <div className="input-group-prepend">
                <span className="input-group-text" id="basic-addon1"><i className="fas fa-search search-icon"></i></span>
              </div>
              <input id='searchInputBox' type="text" className="form-control" placeholder="Start typing..." onChange={this.handleChange} pattern="[A-Za-z]" aria-label="Username" aria-describedby="basic-addon1" />
            </div>
            <input id='testInput' placeholder='start typing...' className={this.state.textBoxFocused ? 'testInput-close' : 'alert alert-info' } onChange={this.handleChange} pattern="[A-Za-z]"></input>
            
            

            
          
             

        <div className="row">
          
          <div className="col-md-6">
            <div className="section-header">
              <span className="title-font">Controls: </span> <span>{this.state.command}</span>
            </div>
            <table className="table table-config-1">
                <tbody>
                  <tr>
                    <td className={this.state.keyPressed =='`'? 'letter lightblue-bg': 'letter'}>
                      <div id="`" data-txt="guide" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">PREV</span><br />
                        <span> `</span>
                      </div>
                    </td>
                    <td className={this.state.keyPressed =='1'? 'letter lightblue-bg': 'letter'}>
                      <div id="1" data-txt="upArrow" onClick={this.handleControlClick} className="cell-text-container">  
                        <span className="cell-text">1</span><br />
                      <span > 1 </span>
                      </div>
                    </td>
                    <td className={this.state.keyPressed =='2'? 'letter lightblue-bg': 'letter'}>
                      <div id="2" data-txt="menu" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">2</span><br />
                        <span> 2 </span>
                      </div>
                    </td>
                    <td className={this.state.keyPressed =='3'? 'letter lightblue-bg': 'letter'}>
                      <div id="3" data-txt="red" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">3</span><br />
                        <span > 3 </span>
                      </div>
                    </td>
                     <td className={this.state.keyPressed =='4'? 'letter lightblue-bg': 'letter'}>
                        <div id="4" data-txt="chanup" onClick={this.handleControlClick} className="cell-text-container">
                          <span className="cell-text">4</span><br />
                          <span > 4 </span>
                        </div>
                    </td>
                    <td className={this.state.keyPressed =='5'? 'letter lightblue-bg': 'letter'}>
                        <div id="4" data-txt="chanup" onClick={this.handleControlClick} className="cell-text-container">
                          <span className="cell-text">5</span><br />
                          <span > 5 </span>
                        </div>
                    </td>
                     <td className={this.state.keyPressed =='6'? 'letter lightblue-bg': 'letter'}>
                        <div id="4" data-txt="chanup" onClick={this.handleControlClick} className="cell-text-container">
                          <span className="cell-text">6</span><br />
                          <span > 6 </span>
                        </div>
                    </td>
                    <td className={this.state.keyPressed =='7'? 'letter lightblue-bg': 'letter'}>
                        <div id="4" data-txt="chanup" onClick={this.handleControlClick} className="cell-text-container">
                          <span className="cell-text">7</span><br />
                          <span > 7 </span>
                        </div>
                    </td>
                    <td className={this.state.keyPressed =='8'? 'letter lightblue-bg': 'letter'}>
                        <div id="4" data-txt="chanup" onClick={this.handleControlClick} className="cell-text-container">
                          <span className="cell-text">8</span><br />
                          <span > 8 </span>
                        </div>
                    </td>
                    <td className={this.state.keyPressed =='9'? 'letter lightblue-bg': 'letter'}>
                        <div id="4" data-txt="chanup" onClick={this.handleControlClick} className="cell-text-container">
                          <span className="cell-text">9</span><br />
                          <span > 9 </span>
                        </div>
                    </td>
                  </tr>
                  <tr>
                    <td colSpan='2' className={this.state.keyPressed =='q'? 'letter lightblue-bg': 'letter'}>
                      <div id="q" data-txt="guide" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">GUIDE</span><br />
                        <span className="controls-key-text"> q</span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='w'? 'letter lightblue-bg': 'letter'}>
                      <div id="w" data-txt="upArrow" onClick={this.handleControlClick} className="cell-text-container">  
                        <span className="cell-text">&uarr;</span><br />
                      <span className="controls-key-text"> w </span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='e'? 'letter lightblue-bg': 'letter'}>
                      <div id="e" data-txt="menu" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">MENU</span><br />
                        <span className="controls-key-text"> e </span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='r'? 'letter lightblue-bg': 'letter'}>
                      <div id="r" data-txt="red" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">RED</span><br />
                        <span className="controls-key-text"> r </span>
                      </div>
                    </td>
                     <td colSpan='2' className={this.state.keyPressed =='t'? 'letter lightblue-bg': 'letter'}>
                        <div id="t" data-txt="chanup" onClick={this.handleControlClick} className="cell-text-container">
                          <span className="cell-text">&#9650;</span><br />
                          <span className="controls-key-text"> t </span>
                        </div>
                    </td>
                  </tr>
                  <tr>
                    <td colSpan='2' className={this.state.keyPressed =='a'? 'letter lightblue-bg': 'letter'}>
                      <div id="a" data-txt="leftArrow" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">&larr;</span><br />
                        <span className="controls-key-text"> a</span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='s'? 'letter lightblue-bg': 'letter'}>
                      <div id="s" data-txt="downArrow" onClick={this.handleControlClick} className="cell-text-container">  
                        <span className="cell-text">&darr;</span><br />
                      <span className="controls-key-text"> s </span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='d'? 'letter lightblue-bg': 'letter'}>
                      <div id="d" data-txt="rightArrow" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">&rarr;</span><br />
                        <span className="controls-key-text"> d </span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='f'? 'letter lightblue-bg': 'letter'}>
                      <div id="f" data-txt="info" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">INFO</span><br />
                        <span className="controls-key-text"> f </span>
                      </div>
                    </td>
                     <td colSpan='2' className={this.state.keyPressed =='g'? 'letter lightblue-bg': 'letter'}>
                        <div id="g" data-txt="chandown" onClick={this.handleControlClick} className="cell-text-container">
                          <span className="cell-text">&#9660;</span><br />
                          <span className="controls-key-text"> g </span>
                        </div>
                    </td>
                  </tr>
                  <tr>
                    <td colSpan='2' className={this.state.keyPressed =='Z'? 'letter lightblue-bg': 'letter'}>
                      <div id="Z" data-txt="leftArrow" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">BACK</span><br />
                        <span className="controls-key-text"> Z </span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='X'? 'letter lightblue-bg': 'letter'}>
                      <div id="X" data-txt="downArrow" onClick={this.handleControlClick} className="cell-text-container">  
                        <span className="cell-text">null</span><br />
                      <span className="controls-key-text"> X </span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='C'? 'letter lightblue-bg': 'letter'}>
                      <div id="C" data-txt="rightArrow" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">null</span><br />
                        <span className="controls-key-text"> C </span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='V'? 'letter lightblue-bg': 'letter'}>
                      <div id="V" data-txt="info" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">RECORD</span><br />
                        <span className="controls-key-text"> V </span>
                      </div>
                    </td>
                     <td colSpan='2' className={this.state.keyPressed =='B'? 'letter lightblue-bg': 'letter'}>
                        <div id="B" data-txt="chandown" onClick={this.handleControlClick} className="cell-text-container">
                          <span className="cell-text">null</span><br />
                          <span className="controls-key-text"> B </span>
                        </div>
                    </td>
                  </tr>
                  <tr>
                    <td colSpan='2' className={this.state.keyPressed =='z'? 'letter lightblue-bg': 'letter'}>
                      <div id="z" data-txt="dash" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">DASH</span><br />
                        <span className="controls-key-text">z</span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='x'? 'letter lightblue-bg': 'letter'}>
                      <div id="x" data-txt="exit" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">EXIT</span><br />
                        <span className="controls-key-text">x</span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='c'? 'letter lightblue-bg': 'letter'}>
                      <div id="c" data-txt="rewind" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">REW</span><br />
                        <span className="controls-key-text">c</span>
                      </div>
                    </td>
                    <td colSpan='2' className={this.state.keyPressed =='v'? 'letter lightblue-bg': 'letter'}>
                      <div id="v" data-txt="play" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">PLAY</span><br />
                        <span className="controls-key-text">v</span>
                      </div>
                    </td>
                     <td colSpan='2' className={this.state.keyPressed =='b'? 'letter lightblue-bg': 'letter'}>
                      <div id="b" data-txt="fastForward" onClick={this.handleControlClick} className="cell-text-container">
                        <span className="cell-text">FFWD</span><br />
                        <span className="controls-key-text">b</span>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td colSpan="10" className={this.state.keyPressed ==' '? 'letter lightblue-bg': 'letter'}>
                      <h1>Select</h1>
                      <span>Spacebar</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            
            
              <table className="table-style" >
                <tbody>
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
                  <tr>
                    <td className={this.state.keyPressed =='space'? 'letter lightblue-bg': 'letter'}>
                      <h1>Select</h1>
                      <span>Spacebar</span>
                    </td>
                  </tr>
                </tbody>
            </table>
          </div>
          <div className="col-md-6">
            <div className="section-header">
              <span className="title-font">Device:</span>{!this.state.rackSelected && <span> First select rack # with search function </span>}{ this.state.rackSelected && <span className="rack-text">Rack-{this.state.rackSelected} Slot-{this.state.slot}</span>}
            </div>
              {!this.state.viewMode16 &&
            <table className="table table-config-1">
              <tbody>
                  <tr>
                    <td className={this.state.viewerPosition == '1' ? 'letter lightblue-bg': 'letter'}>
                      
                      <span className="cell-text-container">Device 1 -{this.state.viewerPosition}</span><br />
                      <span className="cell-text-container"> ^</span>
                      
                    </td>
                    <td className={this.state.viewerPosition == '5' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 5</span><br />
                      <span> &</span>
                    </td>
                  </tr>
                  <tr>
                    <td className={this.state.viewerPosition == '2' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 9</span><br />
                      <span className="key-text">y</span>
                    </td>
                    <td className={this.state.viewerPosition == '6' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 13</span><br />
                      <span> u</span>
                    </td>
                  </tr>
                </tbody> 
            </table>
          }
          {this.state.viewMode16 && <table className="table table-config-1">
                <tbody>
                  <tr>
                    <td className={this.state.viewerPosition == '1' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 1</span><br />
                      <span className="cell-text-container">{this.state.view1.model}</span><br />
                      <span className="key-text"> ^</span>
                    </td>
                    <td className={this.state.viewerPosition == '5' ? 'letter lightblue-bg': 'letter'}>
                    <span className="cell-text-container">Device 5</span><br />
                    <span className="cell-text-container-info">{this.state.view5.model}</span><br />
                      <span className="key-text"> &</span>

                    </td>
                    <td className={this.state.viewerPosition == '9' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 9</span><br />
                      <span className="cell-text-container-info">{this.state.view9.model}</span><br />
                      <span className="key-text">*</span>
                    </td>
                    <td className={this.state.viewerPosition == '13' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 13</span><br />
                      <span className="cell-text-container">{this.state.view13.model}</span><br />
                      <span className="key-text"> (</span>
                    </td>
                  </tr>                  
                  <tr>
                    <td className={this.state.viewerPosition == '2' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 2</span><br />
                      <span className="cell-text-container">{this.state.view2.model}</span><br />
                      <span className="key-text"> y</span>
                    </td>
                    <td className={this.state.viewerPosition == '6' ? 'letter lightblue-bg': 'letter'}>
                    <span className="cell-text-container">Device 6</span><br />
                     
                      <span className="cell-text-container">{this.state.view6.model}</span><br />
                       <span className="key-text"> u</span>
                    </td>
                    <td className={this.state.viewerPosition == '10' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 10</span><br />
                      <span className="cell-text-container">{this.state.view10.model}</span><br />
                      <span className="key-text">i</span>
                    </td>
                    <td className={this.state.viewerPosition == '14' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 14</span><br />
                      <span className="cell-text-container">{this.state.view14.model}</span><br />
                      <span className="key-text"> o</span>
                    </td>
                  </tr>
                  <tr>
                    <td className={this.state.viewerPosition == '3' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container"> Device 3 </span> <br />
                      <span className="cell-text-container">{this.state.view3.model}</span><br />
                      <span className="key-text"> h</span>
                    </td>
                    <td className={this.state.viewerPosition == '7' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 7</span><br />
                      <span className="cell-text-container">{this.state.view7.model}</span><br />
                      <span className="key-text">j</span>
                    </td>
                    <td className={this.state.viewerPosition == '11' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 11</span><br />
                      <span className="cell-text-container">{this.state.view11.model}</span><br />
                      <span className="key-text">k</span>
                    </td>
                    <td className={this.state.viewerPosition == '15' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 15</span><br />
                      <span className="cell-text-container">{this.state.view15.model}</span><br />
                      <span className="key-text"> l</span>
                    </td>
                  </tr>
                  <tr>
                    <td className={this.state.viewerPosition == '4' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">STB 4</span><br />
                      <span className="cell-text-container">{this.state.view4.model}</span><br />
                      <span className="key-text">n</span>
                    </td>
                    <td className={this.state.viewerPosition == '8' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 8</span><br />
                      <span className="cell-text-container">{this.state.view8.model}</span><br />
                      <span className="key-text">m</span>
                    </td>
                    <td className={this.state.viewerPosition == '12' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 12</span> <br />
                      <span className="cell-text-container">{this.state.view12.model}</span><br />
                      <span className="key-text">,</span>
                    </td>
                    <td className={this.state.viewerPosition == '16' ? 'letter lightblue-bg': 'letter'}>
                      <span className="cell-text-container">Device 16</span><br />
                      <span className="cell-text-container">{this.state.view16.model}</span><br />
                      <span className="key-text">.</span>
                    </td>
                  </tr>
                  <tr>
                    <td colSpan="4" className={this.state.slot == '1-16' ? 'letter lightblue-bg': 'letter'}>
                      <h1>All 16 Slots</h1>
                      <span className="key-text">/</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            }


          </div>
          
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