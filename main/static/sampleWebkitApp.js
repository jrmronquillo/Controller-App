


//Application specific code
//window.onload = setPig;
window.onload = main;
//window.onload = initFunction;



//window.onkeydown = Controller;
function View(controller){ 
    this.controller = controller;
    //this.controller.setPig();

    // pull in data
    this.controller.dataProcess();

    // set default highlight
    this.controller.defaultHighlight();

   
    //this.leaderboardContainer - render player data;
    document.getElementById('canvas-data').appendChild(this.controller.getPlayerData());




    // item views
    this.allMenuItems = document.getElementById('list-container-1').children;

   	this.err = document.getElementById('error-message');

   	//this.err.innerHTML = controller.getErrorMessage();

    window.addEventListener('keydown', this.controller);
    window.onerror = function(errorMsg, url, lineNumber){
		   // If Webkit throws an error on the STB - the app crashes.
		   // To prevent the propagation and therefore the crash
		   // return true

		   // Look for this console.log message in the logs
		   // To access the logs use http://{STB_IP}/itv/getLogs
		   //console.log(errorMsg);
		   return true;
		 };
}

function Model(){
  this.sampleText = "Leaderboard1";
  this.className = "testClass";
  this.listContainer = document.getElementById('list-container-1');
  this.elem2Focus = '';
  this.leftMenuPosition = 0;
  this.dataListPosition = 0;
  this.errorMessage = "";
  this.focusedListPosition = 0;
}

this.PlayerModel = function (data){
	this.id = data.id;
	this.name = data.name;
};

const emptyDataSet = [];

const testData = [
					{
					'id': 1,
					'name': 'andrew agassi'},
					 {
					 'id': 2,
					 'name': 'pete sampras'},
					 {
					 'id': 3,
					 'name': 'jrock'},
					 {
					 'id': 4,
					 'name': 'jrock111'},
					 {
					 'id': 5,
					 'name': 'jrock222'},
					 {
					 'id': 6,
					 'name': 'jrock123123123'},
				];

function Controller(model){
  console.log('Controller Triggered! ');

  var self = this;
  this.model = model;


  fetch('http://localhost:3000/rssTest', {mode: 'no-cors'})
      .then(function(response){
        console.log('fetch function triggered!');
        console.log(response);
        if (response.status>= 400) {
          throw new Error("Bad response from the server");
        }
        return response.json();
      })
      .then(function(data){
       			console.log('response was good!');
       			console.log(data);
       		});

 

 this.playersArr = [];
 // data intake
 this.dataProcess = function(){

 	testData.forEach(function(dataItem){
 		// add PlayersModel Objects the the playersArr for each player item.
 		self.playersArr.push(new PlayerModel(dataItem));
 	});
 	
 };

 this.defaultHighlight = function(){
 	console.log('default highlight function called!');
 	console.log(self.model.listContainer);
 	// set position to first item
 	self.model.position = 0;
 	self.model.listContainer.children[0].classList.add('underline');
 };

 this.setHighlight = function(){
 	console.log('setHighlight function called!');
 	console.log('getFocusListPosition'+this.getFocusedListPosition());
 	self.model.listContainer.children[this.getFocusedListPosition()].classList.add('underline');
 };

 this.getFocusedListPosition = function(){
 	console.log('getFocusedListPosition called!');
 	return self.model.focusedListPosition;
 };

 this.highlightPrevChild = function(){
 	console.log('highlight prev child called');
 	var leftMenuObj = document.querySelector("#list-container-1");
 	var dataObj = document.querySelector("#data-list-container");
 	if(leftMenuObj == self.model.listContainer){
		self.model.listContainer.children[this.getLeftMenuPosition()-1].classList.add('underline');
		self.model.leftMenuPosition = this.getLeftMenuPosition() - 1;
		
 	} else {
 		self.model.listContainer.children[this.getDataListPosition()-1].classList.add('underline');
		self.model.dataListPosition = this.getDataListPosition() - 1;
	}
 
 };


 this.highlightPrevChild2 = function(){
 	console.log('highlightPrevChild2 called!');
 	var leftMenuObj = document.querySelector("#list-container-1");
 	var dataObj = document.querySelector("#data-list-container");
 
 	if(leftMenuObj == self.model.listContainer){
 		self.model.leftMenuPosition = this.getLeftMenuPosition()-1;
		self.model.focusedListPosition = this.getLeftMenuPosition(); 
 	} else {
 		self.model.dataListPosition = this.getDataListPosition()-1;
 		self.model.focusedListPosition = this.getDataListPosition();
 	}

 	console.log(self.model);
 };

 this.highlightNextMenuItem = function(){
 	return self.model.listContainer;
 };

 this.highlightNextChild = function(){
 	console.log('highlight next Child called!');
 	//check  model is set to which list
 	var leftMenuObj = document.querySelector("#list-container-1");
 	var dataObj = document.querySelector("#data-list-container");
 
 	
 	if(leftMenuObj == self.model.listContainer){
		self.model.listContainer.children[this.getLeftMenuPosition()+1].classList.add('underline');
		self.model.leftMenuPosition = this.getLeftMenuPosition() + 1;
 	} else {
 		self.model.listContainer.children[this.getDataListPosition()+1].classList.add('underline');
		self.model.dataListPosition = this.getDataListPosition() + 1;
	}
	console.log('leftMenuPosition'+self.model.leftMenuPosition);
	console.log('dataListPosition'+self.model.dataListPosition);
 };


 this.highlightNextChild2 = function(){
 	console.log('highlightNextChild2 called!');
 	var leftMenuObj = document.querySelector("#list-container-1");
 	var dataObj = document.querySelector("#data-list-container");
 
 	if(leftMenuObj == self.model.listContainer){
 		self.model.leftMenuPosition = this.getLeftMenuPosition()+1;
		self.model.focusedListPosition = this.getLeftMenuPosition(); 
 	} else {
 		self.model.dataListPosition = this.getDataListPosition()+1;
 		self.model.focusedListPosition = this.getDataListPosition();
 	}

 	console.log(self.model);
 };

this.setScrollPosition = function(){
	console.log('setScrollPosition function called!');
	var highlightedItem = document.querySelector('#data-list-container').children[this.getFocusedListPosition()];
	console.log(highlightedItem);
	highlightedItem.scrollIntoView(true);
	//console.log(container.scrollTop);
	//console.log(container.scrollLeft);
};




//EVENTLISTENER INTERFACE
  this.handleEvent = function(e){
    e.stopPropagation();
    console.log('------');
    console.log(e.keyCode);
    
    switch(e.keyCode){
      case 37:
      	console.log('leftArrow detected!');
      	self.clearUnderlines();
      	self.switchLists();
      	//self.defaultHighlight();
      	self.setHighlight();
      	break;
      case 38:
      	//upArrow
      	console.log('upArrow detected!');

      	// 
      	if(self.model.focusedListPosition > 0){
        	self.clearUnderlines();
        	self.highlightPrevChild2();
        	self.setHighlight();
        }

        if(self.model.listContainer == document.getElementById('data-list-container')){
        	self.setScrollPosition();
        }	
        
      	break;
      case 39:
      	console.log('right arrow triggered');
		self.clearUnderlines();
		self.switchLists();
		//self.defaultHighlight();
		self.setHighlight();
		break;
      case 40:
      	//downArrow
      	console.log('down arrow detected!');
      	if(self.model.focusedListPosition < self.model.listContainer.children.length-1){
	      	self.clearUnderlines();
	        self.highlightNextChild2();

	        // sethighlight uses focusedListHighlight value;
	        self.setHighlight();
	    }

	    if(self.model.listContainer == document.getElementById('data-list-container')){
        	self.setScrollPosition();
        }	
        
        break;
      default:
        console.log(e.target);
        console.log(e.keyCode);
    }
    return false; 
  };

 this.getPlayerData = function(){
 	
 	var list = document.createElement('ul');
 	list.id = "data-list-container";
 	// validate player data here ----->
 	if(this.playersArr && this.playersArr.length){
	 	console.log('data detected');
	 	for(var i = 0; i < this.playersArr.length; i++) {
	       // Create the list item:
	       var item = document.createElement('li');
	       
	       //set tabIndex to -1 to attempt to allow focus on a li element;
	       //item.tabIndex = -1;
	       

	       // Set its contents:
	      item.appendChild(document.createTextNode(this.playersArr[i].name));
		  item.classList.add('canvas-data-item-container');
	      // Add it to the list:
	      list.appendChild(item);
	    }
	    return list;

	 } else {
	 	var errorObj = document.createElement('h1');
	 	errorObj.innerHTML = 'No data available.';
	 	errorObj.classList.add('error-message');
	 	console.log('no data available');
	 	console.log(errorObj);
	 	return errorObj;
	 }


	 

 };

 this.getSelectedList = function(){
 	return self.model.listContainer;
 };

 this.switchLists = function(){
 	console.log('switchLists function called!');
 	if(this.getSelectedList() == document.getElementById('list-container-1')){
 		self.model.listContainer = document.getElementById('data-list-container');
 		self.model.focusedListPosition = this.getDataListPosition();
 	} else {
 		self.model.listContainer = document.getElementById('list-container-1');
 		self.model.focusedListPosition = this.getLeftMenuPosition();
 	}
 };

 this.setPig = function(){

	console.log('setPig triggered');
	// navigator test
	//console.log('attempting to blind');
	navigator.blind(false);

	// set pig
	var in_x = 100;
	var in_y = 100;
	var in_width = 1820;
	var in_height = 870;
	var out_x = 40;
	var out_y = 120;
	var out_width = 450;
	var out_height = 250;
	//var testeee = navigator.clearBackground(in_x, in_y, in_width, in_height);
	//console.log(testeee);
	var setVid = VideoSource.setInputOutputWindow(in_x, in_y, in_width, in_height, out_x, out_y, out_width, out_height);
	
	return false;
};

this.toggleListContainer = function(){
	// inteneded to be called from a left/right arrow keypress
	
	// change list container in model 
	self.model.listContainer = document.getElementById('')
};


//GET ELEMENT TO HIGHLIGHT
this.getElementToHighlight = function() {
	return self.model.elem2Focus;
};

//GET LEFT MENU POSITION
this.getLeftMenuPosition = function(){
 	return self.model.leftMenuPosition;
 };

 //GET DATA LIST POSITION
 this.getDataListPosition = function(){
 	return self.model.dataListPosition;
 };



//GET MODEL HEADING
  this.getModelHeading = function(){
    return self.model.sampleText;
  };


//GET ERR MESSAGE
this.getErrorMessage = function(){
	return self.model.errorMessage;
};
//GET MODEL CLASSNAME
  this.getClassName = function(){
  	return self.model.className;
  };

// Clear all underlines
this.clearUnderlines =function(){
	console.log('clearUnderlines called');
	// clear underline and cells from all lists
  	// declare object for all children of list items
    var listItemsArr = document.getElementById('list-container-1').children;
    var leaderboardItemsArr = document.getElementById('data-list-container').children;

    // initialize by checking if there highlights on any list elements 
	// and if found, clear them.

	// loop for left menu items
    var counter = listItemsArr.length-1;
    while(counter >= 0){
    	if(listItemsArr[counter].classList.contains('underline')){
    		listItemsArr[counter].classList.toggle('underline');
    	}
    	counter--;
    }
	
	    
    // loop for data items
    var counter2 = leaderboardItemsArr.length-1;
    while(counter2 >= 0){
    	if(leaderboardItemsArr[counter2].classList.contains('underline')){
    		leaderboardItemsArr[counter2].classList.toggle('underline');
    	}
    	counter2--;
    }

	console.log('clearUnderlines completed!');

};

//CHANGE THE MODEL
  this.keyHandler = function(target){
  	console.log('keyHandler called, attempting to clear underlines!');
  	self.clearUnderlines();

  	if(target >1){
		console.log('keyhandler called right, should move higlight to leaderboard-->'); 
		self.model.elem2Focus = document.getElementById('data-list-container').children[0];
		this.getElementToHighlight().classList.add('underline');		
  	}

    var maxElemItems = allListItems.length-1;

    if(target<2){
	    // if highlight is not the last element, increment position
	    // if it is last element, move highlight to the first element
	    	
		// change the model by setting the model.position
		var newPos = self.getHighlightPosition() + target;
		if (newPos < 0 ){
			self.model.position = 0;
		} else if ( newPos > maxElemItems){
			self.model.position = maxElemItems;
		} else {
			self.model.position = newPos;
		}
	}

    // add underline to element with matching position from the model
    allListItems[self.getHighlightPosition()].classList.add('underline');

   
  };
}

function main(){
  var model = new Model();
  var controller = new Controller(model);
  var view = new View(controller);
}

//-------------------------




function keyHandler1(e){
	console.log('keyHandler1 called!');
	var code = e.keyCode
		, container = document.getElementById('key-down');

		//Don't for get to put a BREAK after every case OR it will
		//Fall through like it does below.
		switch(code){
			case 13: // Select / Enter
				console.log('attempting to unblind');
				navigator.blind(false);
				break;
			case 48 : // 0
			case 49 : // 1
			case 50 : // 2
			case 51 : // 3
			case 52 : // 4
			case 53 : // 5
			case 54 : // 6
			case 55 : // 7
			case 56 : // 8
			case 57 : // 9
			case 79 : // Info
			case 87 : // Rewind Trick play
			case 9 : // FF Trick play
			case 65 : //Active
			case 67 : // Next Trick play
			case 72 : // red
			case 74 : // green
			case 75 : // yellow
			case 76 : // blue
			case 80: // Play Trick play
			case 82 : // Record Trick play
			case 83 : // Stop Trick play
			case 85 : // Pause Trick play
			case 46 : // Back Trick play
			case 37: //left
				console.log('left arrow triggered');
				//var vidVar = VideoSource.setFullScreen();
				//console.log(vidVar);
				break;
			case 33: //pageup channelUp
			case 34: //pagedown channelDown
			case 38: //up
				console.log('up arrow triggered');
				break;
			case 39: //right
				console.log('right arrow triggered');
				this.switchLists();
				this.setUnderline();
				break;
			case 40: //down
			case 47: //back
			case 189 : //dash
			default :
				container.innerHTML = code;
				break;
			}

			// return false prevents keys from bubbling to UI
			return false;
			}


		

		window.onerror = function(errorMsg, url, lineNumber){
		   // If Webkit throws an error on the STB - the app crashes.
		   // To prevent the propagation and therefore the crash
		   // return true

		   // Look for this console.log message in the logs
		   // To access the logs use http://{STB_IP}/itv/getLogs
		   //console.log(errorMsg);
		   return true;
		 };