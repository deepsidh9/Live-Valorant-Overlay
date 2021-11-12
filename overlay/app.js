document.addEventListener("DOMContentLoaded", function(event) { 
    var socket = io.connect("http://127.0.0.1:4445/");
    socket.on('after connect', function(message){
        console.log('After connect', message);
        return true;
     });
     socket.on('receive_details', function(data) {
          console.log('New Value Received',data["match_details"]);
          populateOverlay(data["match_details"]);
     });
});

function populateOverlay(matchDetails){
    // console.log('Hello')
    const sides= ["blue","red"]
    var allElements = {blue:[],red:[]}

    for (const side of sides) {
        
        var agents =  Object.keys(matchDetails[side]);
        console.log('agents',agents)
        for (const agent of agents) {
            var allInformationDiv = document.createElement('div')
            
            
            var weaponContainer = document.createElement('div')
            weaponContainer.className = "weaponContainer"
            
            var agentDiv = document.createElement('div');
            agentDiv.className = "agent"
            
            var shieldHealthContainerDiv = document.createElement('div');
            shieldHealthContainerDiv.className = "shieldHealthContainer"

            var shieldImage = document.createElement('img')
            shieldImage.src=""
            shieldImage.className="shieldImage"
            if(matchDetails[side][agent]["shield"]){
                console.log("Shield Icons/"+matchDetails[side][agent]["shield"]+".png")
                shieldImage.src =  "Shield Icons/"+matchDetails[side][agent]["shield"]+".png"
            }
            
            var ultimateContainer = document.createElement('div')
            ultimateContainer.className = "ultimateContainer"

            var ultimateImage = document.createElement('img')
            ultimateImage.className = "ultimateImage"
            ultimateImage.src="Ultimate Icons/"+matchDetails[side][agent]["agent"]+"_ult.png"
            ultimateContainer.appendChild(ultimateImage)
            console.log("Source of Ultimate Image: " + matchDetails[side][agent]["agent"]+"_ult.png")
            var ultimatePointsSpan = document.createElement('span');
            if(matchDetails[side][agent]["current_ultimate_points"]){
                if(matchDetails[side][agent]["current_ultimate_points"]=="READY"){
                    ultimatePointsSpan.innerHTML="READY"
                }else{
                    ultimatePointsSpan.innerHTML=matchDetails[side][agent]["current_ultimate_points"]+"/"+matchDetails[side][agent]["required_ultimate_points"]
                }
            }else{
                ultimatePointsSpan.innerHTML="NA"
            }
            // var healthSpan = document.createElement('span');
            // if(matchDetails[side][agent]["health"]){
            //     healthSpan.innerHTML = matchDetails[side][agent]["health"]
            //     // shieldHealthContainerDiv.style.background = "linear-gradient(to top, red "+matchDetails[side][agent]["health"]+"%, white 0%);" 
            // }
            // else{
            //     healthSpan.innerHTML = "__"
            //     // shieldHealthContainerDiv.style.background = "linear-gradient(to top, red 0%, white 0%);"
            // }

            shieldHealthContainerDiv.appendChild(shieldImage)
            // shieldHealthContainerDiv.appendChild(healthSpan)
            shieldHealthContainerDiv.appendChild(ultimateContainer)
            shieldHealthContainerDiv.appendChild(ultimatePointsSpan)

            var weaponImageElement = document.createElement('img')
            weaponImageElement.src =  ""
            if(matchDetails[side][agent]["weapon"]){
                weaponImageElement.src =  "Weapon Images/" + matchDetails[side][agent]["weapon"]+".png"
            }
            
            
            var agentNameSpan = document.createElement('span');
            if(matchDetails[side][agent]["name"].length>8){ 
                agentNameSpan.innerHTML = matchDetails[side][agent]["name"].substring(0,8)+"..."
            }else{
                agentNameSpan.innerHTML = matchDetails[side][agent]["name"]
            }
             
            var agentImageSource= "Original Agent Icons/" + matchDetails[side][agent]["agent"].charAt(0).toUpperCase() +matchDetails[side][agent]["agent"].slice(1)+ "_icon.png"
            
            if (matchDetails[side][agent]["alive"] == false){
                var brightness= 0.5}
            else{
                var brightness= 1
            }

            var imageElement = document.createElement('img');
            imageElement.src =agentImageSource
            imageElement.style.filter = "brightness(" +brightness+ ")";
            imageElement.style.height = "100px"
            imageElement.style.width = "100px"
           
            if (side=="red"){
                allInformationDiv.className = "allRightInformation"
                imageElement.className = "right-agent"
                agentNameSpan.className= "right-span"
                weaponImageElement.className = "right-weapon"
                agentDiv.appendChild(imageElement)
                agentDiv.appendChild(agentNameSpan)
                weaponContainer.appendChild(weaponImageElement)
                allInformationDiv.appendChild(agentDiv)
                allInformationDiv.appendChild(shieldHealthContainerDiv)
                allInformationDiv.appendChild(weaponContainer)

            }else{
                allInformationDiv.className = "allLeftInformation"
                imageElement.className = "left-agent"
                agentNameSpan.className= "left-span"
                weaponImageElement.className = "left-weapon"
                agentDiv.appendChild(imageElement)
                agentDiv.appendChild(agentNameSpan)
                weaponContainer.appendChild(weaponImageElement)
                allInformationDiv.appendChild(agentDiv)
                allInformationDiv.appendChild(shieldHealthContainerDiv)
                allInformationDiv.appendChild(weaponContainer)
                
            }    
            allElements[side].push(allInformationDiv)
        }
        console.log('Side with all elements:',side,allElements[side])
    }
    console.log('All  Elements:',allElements)
    updateElements(allElements);
}

function updateElements(allElements){
    const blue = document.getElementById("blue");
    blue.innerHTML = '';
    blueAgentElements = allElements["blue"]
    
    const red = document.getElementById("red");
    red.innerHTML = '';
    redAgentElements = allElements["red"]

    for (var redAgentElement of redAgentElements){
        red.appendChild(redAgentElement)
    }
    for (var blueAgentElement of blueAgentElements){
        blue.appendChild(blueAgentElement)
    }
    console.log('Updated Agents')

}

function showPostRoundToast() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
  
    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
  }