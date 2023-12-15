const URL = 'ws://localhost:8763/interface'
var ws = new WebSocket(URL);

ws.onmessage = function(evt){

   var received_msg = evt.data;
   console.log(received_msg);
   
   if(received_msg.includes("details")){
     implementDetail(received_msg)
   }

   if(received_msg.includes("command_feedback")){
      implementCommand(received_msg)
   }
};

ws.onclose = () => {
   alert("Connection is closed...")
}

ws.onopen = function() {
   ws.send("interfaceDetail")
}

const tab = document.querySelectorAll('.tab_container section').forEach((tab) => {
   tab.addEventListener('click', (event) => {
      
      document.querySelector('#tab_active').removeAttribute('id');
      event.target.id='tab_active';
      currentView = event.target.className;
      changeView(currentView);
   
    });
  });

function changeView(currentView){

   

   if(currentView == "tab1"){

      let tab1 = `<div class="tab1_container">               
   <div class="identifier">Identifier</div>
   <div class="timestamp">Timestamp</div>
   <div class="state">State</div>
   </div>`

      document.querySelector('.main_view').innerHTML = tab1;
      ws.send("interfaceDetail")
      
      
   }else{

      let tab2 = `<div class="button_container">
      <div class="button_on" id="button_active">On</div>
      <div class="button_off">Off</div>
      </div>`

      document.querySelector(".main_view").innerHTML = tab2;

      document.querySelectorAll(".button_container div").forEach((button) => {
         button.addEventListener("click", (e)=>{
            document.querySelector("#button_active").removeAttribute("id");
            e.target.id="button_active"
            sendCommand(e);
         });
      })
   }
}

function implementDetail(msg){
   msg = msg.replace(/'/g, '"')
   msg = JSON.parse(msg)
   let tab1 = `<div class="tab1_container">
                  
   <div class="identifier">${msg.name}</div>
   <div class="timestamp">${msg.timestamp}</div>
   <div class="state">${msg.state}</div>
   </div>`
   document.querySelector('.main_view').innerHTML+= tab1;
}

function implementCommand(msg){
   msg = msg.replace(/'/g, '"')
   msg = JSON.parse(msg)
}


function sendCommand(e){
   
   msg = ["command", e.target.innerHTML]
   ws.send(msg);
   
}
