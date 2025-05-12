(()=>{frappe.provide("vulero_dialer");vulero_dialer=class{static addCallButton(t,a,o){frappe.ui.form.on(t,{refresh(e){e.add_custom_button('<i class="fa fa-phone"></i> Call',()=>{if(e.doc[a]&&e.doc[o]){let l=[{label:__("Phone: ")+e.doc[a],value:e.doc[a]},{label:__("Mobile: ")+e.doc[o],value:e.doc[o]}];frappe.prompt([{fieldname:"number_to_call",fieldtype:"Select",label:"Which number to call?",options:l,reqd:1}],r=>{s(r.number_to_call)},__("Call "+t),__('<i class="fa fa-phone"></i> Call'))}else if(e.doc[a]||e.doc[o]){let l=e.doc[a]||e.doc[o];s(l)}else frappe.msgprint(__("No contact number found for this "+t.toLowerCase()+"."))})}})}};function s(n){window.dispatchEvent(new CustomEvent("callEvent",{detail:{number:n}}))}vulero_dialer.addCallButton("Lead","phone","mobile_no");vulero_dialer.addCallButton("Opportunity","phone","mobile_no");vulero_dialer.addCallButton("Contact","phone","mobile_no");vulero_dialer.addCallButton("Customer","phone","mobile_no");$(document).ready(function(){let n="/assets/vulero_dialer/images/joining-queue.png",t="/assets/vulero_dialer/images/leaving-queue.png";window.addEventListener("queueEvent",function(o){o.detail=="join_queue"?($("#queueIcon").attr("src",t),frappe.msgprint("Joined the queue")):o.detail=="leave_queue"&&($("#queueIcon").attr("src",n),frappe.msgprint("Left the queue"))}),frappe.call({method:"vulero_dialer.config.queue.get_queue_status",args:{},callback:function(o){if(o.message&&o.message.status==="success"){let e=$("#queueIcon");o.message.is_member?e.attr("src",t):e.attr("src",n)}else console.log("Error:",o.message?o.message:"Unknown error")},error:function(o){console.log("Error calling the method:",o)}});function a(){let o=$(`
            <li class="nav-item">
                <button class="btn" id="queueButton" style="border: none; background-color: transparent;">
                    <img src="${n}" id="queueIcon" width="24" height="24" alt="joining-queue"/>
                </button>
            </li>
        `),e=$("ul.navbar-nav > li.nav-item.dropdown-notifications");if(e.length===0){console.error("Bell icon not found"),setTimeout(a,500);return}e.after(o),$("#queueButton").on("click",function(){let l=$(this),r=$("#queueIcon");r.attr("src")===n?(frappe.call({method:"vulero_dialer.config.queue.add_to_queue",callback:function(c){c.message.message==="added"?(console.log("Successfully joined the queue."),r.attr("src",t)):console.error("Failed to join the queue:",c.message.message)}}),frappe.call({method:"vulero_dialer.config.call_log.fetch_and_process_missed_call_logs",callback:function(c){console.log("Fetched Missed Calls")}})):frappe.call({method:"vulero_dialer.config.queue.remove_from_queue",callback:function(c){c.message.message==="removed"?($("#queueIcon").attr("src",n),console.log("Successfully left the queue."),r.attr("src",n)):console.error("Failed to leave the queue:",c.message)}})}),$("head").append(`
            <style>
                #queueButton {
                    display: inline-block;
                    margin-left: 10px;
                    background-color: transparent;
                    border: none;
                    padding: 0;
                }
                #queueButton:hover {
                    background-color: rgba(0, 0, 0, 0.1);
                }
            </style>
        `)}a()});$(document).ready(function(){window.addEventListener("statusEvent",function(t){switch(t.detail){case"connected":$("#connectionStatusDot").css("background-color","green");break;case"disconnected":$("#connectionStatusDot").css("background-color","red");break;case"reconnecting":$("#connectionStatusDot").css("background-color","orange");break;default:console.log("Unknown status:",t.detail),$("#connectionStatusDot").css("background-color","grey");break}});function n(){let t=$("ul.navbar-nav > li.nav-item.dropdown-notifications");if(t.length===0){console.error("Bell icon not found"),setTimeout(n,500);return}let a=$('<li class="nav-item"><span id="connectionStatusDot"></span></li>');t.after(a),$("head").append(`
            <style>
                #connectionStatusDot {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background-color: red;
                    display: inline-block;
                    margin-left: 10px;
                    vertical-align: middle;
                }
            </style>
        `)}n()});(function(){function n(o){let e=document.createElement("div");e.id=o,o==="app"&&(e.classList.add("sticky-top"),e.style.zIndex="2000");var l=document.querySelector(".main-section");l?l.prepend(e):document.body.prepend(e)}n("app"),n("modals"),n("popovers");var t=document.createElement("script"),a=document.createElement("link");a.rel="stylesheet",a.href="/assets/vulero_dialer/frontend/assets/index-DaPgrmOC.css",t.src="/assets/vulero_dialer/frontend/assets/index-Dyl3I0Od.js",t.type="module",document.head.appendChild(t),document.head.appendChild(a)})();})();
//# sourceMappingURL=vulero_dialer.bundle.VLUWM6UG.js.map
