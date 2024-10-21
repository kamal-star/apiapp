console.log("Hello Desk");

console.log("Hello Desk");

window.onload = function() {
    // Ensure the DOM is fully loaded and the navbar is available
    let navbar = document.querySelector(".navbar-collapse");

    if (navbar) {
        // Create the anchor element for the gtranslate wrapper
        let anc = document.createElement("a");
        anc.className = "gtranslate_wrapper";
        navbar.prepend(anc); // Insert at the beginning of the navbar

        // Inject the gtranslateSettings script
        let settingsScript = document.createElement('script');
        settingsScript.type = 'text/javascript';
        settingsScript.innerHTML = `
            window.gtranslateSettings = {
                "default_language": "en",
                "languages": ["en", "fr", "de", "it", "es", "ar"],
                "wrapper_selector": ".gtranslate_wrapper"
            };
        `;
        document.head.appendChild(settingsScript);

        // Inject the dropdown.js script
        let gtranslateScript = document.createElement('script');
        gtranslateScript.src = "https://cdn.gtranslate.net/widgets/latest/dropdown.js";
        gtranslateScript.defer = true; // Ensure the script runs after the DOM is loaded
        document.head.appendChild(gtranslateScript);

    } else {
        console.error("Navbar element not found");
    }
    $(document).on('click', '.navbar .dropdown-help .logout-btn', function() {
        frappe.confirm(
            'Are you sure you want to log out?',
            function() {
                // If confirmed
                frappe.call({
                    method: 'logout',
                    callback: function() {
                        window.location.href = '/login';
                    }
                });
            },
            function() {
                // If canceled, do nothing
            }
        );
    });

    
};



