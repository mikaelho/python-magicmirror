    function getDom() {
  
  		var wrapper = document.createElement("div");
  
  		/************************************
  		 * Create wrappers for DIGITAL clock
  		 */
  
  		var dateWrapper = document.createElement("div");
  		var timeWrapper = document.createElement("div");
  		var secondsWrapper = document.createElement("sup");
  		var periodWrapper = document.createElement("span");
  		var weekWrapper = document.createElement("div")
  		// Style Wrappers
  		dateWrapper.className = "date normal medium";
  		timeWrapper.className = "time bright large light";
  		secondsWrapper.className = "dimmed";
  		weekWrapper.className = "week dimmed medium";
  
  		// Set content of wrappers.
  		var timeString = "";
  		var now = new Date();
  		var hrs = padWithZero(now.getHours());
  		var mins = padWithZero(now.getMinutes());
  		timeString = timeString + hrs + 
  		":<span class=\"bold\">" + mins + "</span>";
  		dateWrapper.innerHTML = now.toLocaleDateString();
  		timeWrapper.innerHTML = timeString;
  		
  		wrapper.appendChild(dateWrapper);
  		wrapper.appendChild(timeWrapper);
  		//wrapper.appendChild(weekWrapper);
  
  		return wrapper;
    }
	
