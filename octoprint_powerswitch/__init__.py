# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events

import pigpio
from time import sleep

class PowerSwitchPlugin(octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.AssetPlugin,
                        octoprint.plugin.SimpleApiPlugin,
                        octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.EventHandlerPlugin,
                        octoprint.plugin.StartupPlugin):

    def __init__(self):
        self._power_state = False
        self._pi = pigpio.pi()

    def get_assets(self):
        return dict(js=["js/powerswitch.js"])

    def on_after_startup(self):
        self._pin = int(self._settings.get(["pin"]))
        self._logger.info("PowerSwitch plugin: pin " + str(self._pin))
        self._pi.set_mode(self._pin, pigpio.OUTPUT)
        self.read_power_state()

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self._pin = int(self._settings.get(["pin"]))
        self._logger.info("PowerSwitch plugin: new pin " + str(self._pin))
        self._pi.set_mode(self._pin, pigpio.OUTPUT)
        self.read_power_state()

    def get_settings_defaults(self):
        return dict(pin=13)

    def get_template_configs(self):
        return [
            dict(type="sidebar", icon="gears", name="Power Switch", data_bind="visible: loginState.isAdmin", custom_bindings=False),
            dict(type="settings", name="PowerSwitch", custom_bindings=False)
            ]

    def get_api_commands(self):
        return dict(ON=[], OFF=[])

#    def is_api_adminonly():
#        return true

    def on_api_command(self, command, data):
        import flask
        if command == 'ON':
            self._power_state = True
        elif command == 'OFF':
            self._power_state = False
        state = pigpio.HIGH if self._power_state else pigpio.LOW
        self._logger.info("PowerSwitch plugin: writing " + str(state) + " to pin " + str(self._pin))
        self._pi.write(self._pin, state)
        self.read_power_state()

    def read_power_state(self):
        sleep(0.2)
        pin_state = self._pi.read(self._pin)
        self._logger.info("Powerswitch: pin " + str(self._pin) + " reads state " + str(pin_state))
        self._plugin_manager.send_plugin_message(self._identifier, dict(powerswitch_state = 'ON' if pin_state else 'OFF'))

    def on_event(self, event, payload):
        if event != Events.CLIENT_OPENED:
            return
        self.read_power_state()


__plugin_name__ = "PowerSwitch"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PowerSwitchPlugin()

