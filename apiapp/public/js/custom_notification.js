// my_custom_app/public/js/custom_notifications.js
frappe.provide("frappe.search");
frappe.provide("frappe.ui");

(function() {
	
    // Ensure the original class is loaded
    frappe.ui.Notifications = class CustomNotifications extends frappe.ui.Notifications {
        constructor() {
            super();
            this.setup_custom_events();
        }

        setup_custom_events() {
            frappe.realtime.on("notification", () => {
                this.on_new_notification();
            });

            this.dropdown.on("show.bs.dropdown", () => {
                this.on_dropdown_show();
            });

            this.dropdown.on("hide.bs.dropdown", () => {
                this.on_dropdown_hide();
            });
        }

        on_new_notification() {
            console.log("New notification received!");
			frappe.show_alert("received?")
            // Custom logic for new notifications
            // For example, you can call update_dropdown() method or show a message
            this.update_dropdown();
        }

        on_dropdown_show() {
            console.log("Dropdown is shownssssssssssssssss");
			frappe.show_alert("down?")
            // Custom logic when dropdown is shown
        }

        on_dropdown_hide() {
            console.log("Dropdown is hidden");
            // Custom logic when dropdown is hidden
        }
    }
})();