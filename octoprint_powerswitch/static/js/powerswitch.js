$(function() {
    function PowerSwitchViewModel() {
	var self = this;

	self.powerswitch_state = ko.observable(undefined);
	self.powerswitch_state("Unknown");

        self.powerswitch_on = function(action) {
            showConfirmationDialog('Printer will be turned ON.', function (e) {
                action.powerswitch_action('ON');
            });
        };

        self.powerswitch_off = function(action) {
            showConfirmationDialog('Printer will be turned OFF.', function (e) {
                action.powerswitch_action('OFF');
            });
        };

        self.powerswitch_action = function(new_state) {
            $.ajax({
                url: API_BASEURL + "plugin/powerswitch",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: new_state
                }),
                contentType: "application/json; charset=UTF-8"
            });
        }

	self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "powerswitch") {
                return;
            }
	    self.powerswitch_state(data.powerswitch_state);
	}

    }

    OCTOPRINT_VIEWMODELS.push([
        PowerSwitchViewModel,
	["loginStateViewModel", "settingsViewModel"],
        document.getElementById('sidebar_plugin_powerswitch')
    ]);
});
