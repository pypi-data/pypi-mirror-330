from whitebox import Plugin


class WhiteboxPluginGpsDisplay(Plugin):
    """
    A plugin that displays a map using leaflet.js and updates the map with the GPS data received from the GPS plugin.

    Attributes:
        name: The name of the plugin.
        plugin_template: Path to the plugin's template.
        plugin_css: List of paths to the plugin's CSS files.
        plugin_js: List of paths to the plugin's JS files.
    """

    name = "GPS Display"

    plugin_template = "whitebox_plugin_gps_display/whitebox_plugin_gps_display.html"
    plugin_iframe_template = "whitebox_plugin_gps_display/map_only.html"
    plugin_css = [
        "/static/whitebox_plugin_gps_display/whitebox_plugin_gps_display.css",
    ]
    plugin_js = [
        "/static/whitebox_plugin_gps_display/leaflet/leaflet.js",
        "/static/whitebox_plugin_gps_display/leaflet-rotatedMarker/leaflet.rotatedMarker.js",
        "/static/whitebox_plugin_gps_display/whitebox_plugin_gps_display.mjs",
    ]

    provides_capabilities = ["map"]
    provider_templates = {
        "map": plugin_iframe_template,
    }


plugin_class = WhiteboxPluginGpsDisplay
