(() => {
  // ../vulero_dialer/vulero_dialer/public/js/call_button.js
  frappe.provide("vulero_dialer");
  vulero_dialer = class vulero_dialer2 {
    static addCallButton(doctype, phoneField, mobileField) {
      frappe.ui.form.on(doctype, {
        refresh(frm) {
          frm.add_custom_button('<i class="fa fa-phone"></i> Call', () => {
            if (frm.doc[phoneField] && frm.doc[mobileField]) {
              let options = [
                { label: __("Phone: ") + frm.doc[phoneField], value: frm.doc[phoneField] },
                { label: __("Mobile: ") + frm.doc[mobileField], value: frm.doc[mobileField] }
              ];
              frappe.prompt([
                { "fieldname": "number_to_call", "fieldtype": "Select", "label": "Which number to call?", "options": options, "reqd": 1 }
              ], (values) => {
                triggerCallEvent(values.number_to_call);
              }, __("Call " + doctype), __('<i class="fa fa-phone"></i> Call'));
            } else if (frm.doc[phoneField] || frm.doc[mobileField]) {
              let number_to_call = frm.doc[phoneField] || frm.doc[mobileField];
              triggerCallEvent(number_to_call);
            } else {
              frappe.msgprint(__("No contact number found for this " + doctype.toLowerCase() + "."));
            }
          });
        }
      });
    }
  };
  function triggerCallEvent(number) {
    window.dispatchEvent(new CustomEvent("callEvent", {
      detail: { number }
    }));
  }
  vulero_dialer.addCallButton("Lead", "phone", "mobile_no");
  vulero_dialer.addCallButton("Opportunity", "phone", "mobile_no");
  vulero_dialer.addCallButton("Contact", "phone", "mobile_no");
  vulero_dialer.addCallButton("Customer", "phone", "mobile_no");

  // ../vulero_dialer/vulero_dialer/public/js/queue_button.js
  $(document).ready(function() {
    const joinIconUrl = "/assets/vulero_dialer/images/joining-queue.png";
    const leaveIconUrl = "/assets/vulero_dialer/images/leaving-queue.png";
    window.addEventListener("queueEvent", function(e) {
      if (e.detail == "join_queue") {
        $("#queueIcon").attr("src", leaveIconUrl);
        frappe.msgprint("Joined the queue");
      } else if (e.detail == "leave_queue") {
        $("#queueIcon").attr("src", joinIconUrl);
        frappe.msgprint("Left the queue");
      }
    });
    frappe.call({
      method: "vulero_dialer.config.queue.get_queue_status",
      args: {},
      callback: function(response) {
        if (response.message && response.message.status === "success") {
          let icon = $("#queueIcon");
          if (response.message.is_member) {
            icon.attr("src", leaveIconUrl);
          } else {
            icon.attr("src", joinIconUrl);
          }
        } else {
          console.log("Error:", response.message ? response.message : "Unknown error");
        }
      },
      error: function(err) {
        console.log("Error calling the method:", err);
      }
    });
    function appendQueueButton() {
      let queueButton = $(`
            <li class="nav-item">
                <button class="btn" id="queueButton" style="border: none; background-color: transparent;">
                    <img src="${joinIconUrl}" id="queueIcon" width="24" height="24" alt="joining-queue"/>
                </button>
            </li>
        `);
      let bellIcon = $("ul.navbar-nav > li.nav-item.dropdown-notifications");
      if (bellIcon.length === 0) {
        console.error("Bell icon not found");
        setTimeout(appendQueueButton, 500);
        return;
      }
      bellIcon.after(queueButton);
      $("#queueButton").on("click", function() {
        let button = $(this);
        let icon = $("#queueIcon");
        if (icon.attr("src") === joinIconUrl) {
          frappe.call({
            method: "vulero_dialer.config.queue.add_to_queue",
            callback: function(response) {
              if (response.message.message === "added") {
                console.log("Successfully joined the queue.");
                icon.attr("src", leaveIconUrl);
              } else {
                console.error("Failed to join the queue:", response.message.message);
              }
            }
          });
          frappe.call({
            method: "vulero_dialer.config.call_log.fetch_and_process_missed_call_logs",
            callback: function(response) {
              console.log("Fetched Missed Calls");
            }
          });
        } else {
          frappe.call({
            method: "vulero_dialer.config.queue.remove_from_queue",
            callback: function(response) {
              if (response.message.message === "removed") {
                $("#queueIcon").attr("src", joinIconUrl);
                console.log("Successfully left the queue.");
                icon.attr("src", joinIconUrl);
              } else {
                console.error("Failed to leave the queue:", response.message);
              }
            }
          });
        }
      });
      $("head").append(`
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
        `);
    }
    appendQueueButton();
  });

  // ../vulero_dialer/vulero_dialer/public/js/connect_status.js
  $(document).ready(function() {
    window.addEventListener("statusEvent", function(e) {
      switch (e.detail) {
        case "connected":
          $("#connectionStatusDot").css("background-color", "green");
          break;
        case "disconnected":
          $("#connectionStatusDot").css("background-color", "red");
          break;
        case "reconnecting":
          $("#connectionStatusDot").css("background-color", "orange");
          break;
        default:
          console.log("Unknown status:", e.detail);
          $("#connectionStatusDot").css("background-color", "grey");
          break;
      }
    });
    function appendConnectionStatusDot() {
      let bellIcon = $("ul.navbar-nav > li.nav-item.dropdown-notifications");
      if (bellIcon.length === 0) {
        console.error("Bell icon not found");
        setTimeout(appendConnectionStatusDot, 500);
        return;
      }
      let connectionStatusDot = $(`<li class="nav-item"><span id="connectionStatusDot"></span></li>`);
      bellIcon.after(connectionStatusDot);
      $("head").append(`
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
        `);
    }
    appendConnectionStatusDot();
  });

  // ../vulero_dialer/frontend/call_loader.js
  (function() {
    function createAndAppendDiv(id) {
      const div = document.createElement("div");
      div.id = id;
      if (id === "app") {
        div.classList.add("sticky-top");
        div.style.zIndex = "2000";
      }
      var mainSection = document.querySelector(".main-section");
      if (mainSection) {
        mainSection.prepend(div);
      } else {
        document.body.prepend(div);
      }
    }
    createAndAppendDiv("app");
    createAndAppendDiv("modals");
    createAndAppendDiv("popovers");
    var script = document.createElement("script");
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/assets/vulero_dialer/frontend/assets/index-DaPgrmOC.css";
    script.src = "/assets/vulero_dialer/frontend/assets/index-Dyl3I0Od.js";
    script.type = "module";
    document.head.appendChild(script);
    document.head.appendChild(link);
  })();
})();
//# sourceMappingURL=vulero_dialer.bundle.UMA4TLRX.js.map
