function randomIntFromInterval(min,max)
{
    return Math.floor(Math.random()*(max-min+1)+min);
}


sels = document.getElementsByClassName('movie');
for(i=0; i<sels.length; i++) {
	sels[i].addEventListener('click', function(e){
		panel=this.getElementsByClassName("sliderright");
		if ( panel != undefined && panel.length == 1) {
			panel[0].classList.toggle("closed");
		} else {
			console.log("sliderright not found or to many sliders: nothing to slide : "+panel.length);
		}
	});
}


sels = document.getElementsByClassName('trailerimg');
for(i=0; i<sels.length; i++) {
	sels[i].addEventListener('click', function(e){
		var movieid=this.parentNode.parentNode.id;
		var video = document.getElementById(movieid).getElementsByClassName('trailervideo');
		video[0].classList.toggle("visible");
		video[0].style.display=video[0].style.display=='none'?'block':'none';
	});

}

//**********************selectionbuttons************************************
watchedbuttons = document.getElementById('watchedbutton');
if (watchedbuttons != undefined ) {
	watchedbuttons.checked=false;
	watchedbuttons.addEventListener('click', function(e){

		movies = document.getElementsByClassName('watched');

		if (this.checked==true) { displaystyle='none'; }
		else 			{ displaystyle='inline-block'; }

		for(j=0; j<movies.length; j++) {
			movies[j].parentNode.parentNode.style.display=displaystyle;
		}	
	});
}

//**********************filterbuttons***************************************

gfbuttons = document.getElementsByClassName('filterbutton');

//make tag cloud, do this once, else you will get jumpy txt
var decorated=false;
if (gfbuttons.length > 1){
	var attr=gfbuttons[i].parentNode.getAttribute('decorated');	
	if ( attr != undefined && attr != 'False' && attr != '') {
		decorated=true;
		gfbuttons[0].parentNode.setAttribute('decorated','True');
	} 
} 

//loop all filterbutton and decorate it and add event listner
for(i=0; i<gfbuttons.length; i++) {

	//add the tag cloud decoration
	if ( ! decorated ) {
		gfbuttons[i].style.fontSize=randomIntFromInterval(10,50)+"px";
		gfbuttons[i].style.fontWeight=randomIntFromInterval(200, 900);	
	}

	//add the click event listner to the genrefilter button
	gfbuttons[i].addEventListener('click', function(e){
		var genre=this.id;
		//loop all movies
		movies = document.getElementsByClassName('movie');
		for(j=0; j<movies.length; j++) {
			if( genre == "All" || movies[j].getAttribute("genres").indexOf(genre) >= 0  ){				
				movies[j].style.display='inline-block';
			} else {
				movies[j].style.display='none';
			}
		}
		//add selected filter class
		this.classList.add("selected");
		//remove selected filter class from previous selection
		prevsel=this.parentNode.getAttribute('active');  
		if ( prevsel != undefined && prevsel !='' ) {
			document.getElementById(prevsel).classList.remove('selected')
		}
		//store the selection
		this.parentNode.setAttribute('active',genre);	
		//reset the other filter options
		watchedbuttons = document.getElementById('watchedbutton');
		watchedbuttons.checked=false;
	});
}
	






