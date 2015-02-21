## Summary
This plugin extends [Indigo](http://www.indigodomo.com) allowing it to send messages to [Slack](https://slack.com), optionally with attachments and file upload.
## Requirements
* [Indigo 6](http://www.indigodomo.com/index.html) or later (pro version only)
* A Slack Team is required. Register for an account at [Slack](https://slack.com) and set up a team
* Optional: Create a Slack channel to be used for Slack Notify (recommended), or use one of the defaults

## Installation
* Download the ZIP file (look over there --->)
* Unzip the file if it doesn't automatically unzip
* On the computer running Indigo, double-click the file "Slack.indigoPlugin"
* Follow the Indigo dialog and enable the plugin
* The plugin should be visible in the Plugins drop-down menu as "Slack Notify"
* Trouble?: Indigo help for the [installation process](http://wiki.indigodomo.com/doku.php?id=indigo_6_documentation:getting_started)

## Configuration
###Configure Plugin
In the menu: Indigo 6/Plugins/Slack Notify/Configure...
  
####WebHook Token
  * Set up an incoming webhook integration by reading and following the link on: https://api.slack.com/incoming-webhooks
  * An URL should be generated and after services/ the series of numbers/letters is the token
  * Enter the above in the WebHook Token field
  
####Slack Token
  * Go [here](https://api.slack.com/web)
  * Under Authentication there should be a team Token
  * Enter the above in the Slack Token field
  
####User ID
  * Go to the following link, replacing the part after = with the slack token above
  * https://slack.com/api/users.list?token=replacewithSlackToken
  * Look for the series of letter/numbers after the line beginning with: "id":
  * Enter the above in the User ID field
  
###Configure Notifications
  * The plugin will show under Type: Notification Actions under Actions as Slack Notify.
  * Once added to a TRIGGER, SCHEDULE or ACTION GROUPS, click on Edit Action Settings...
  * ... wait a second or two ... or three
  * The Channel drop down menu should be auto populated with channels in your team; select one.
  * Alternately send a [Direct Message](https://slack.zendesk.com/hc/en-us/articles/202009646-Using-channel-group-everyone) by entering text in the Direct Message field.
  * Enter the message text in the Text field, following the formatting hints listed below the field. Formatting for Indigo and Slack is outlined.
  * Optional: Enter a username to be posted as. If blank, the plugin will use your username and post as a bot.
  * Optional: Enter a name of an [emoji](http://www.emoji-cheat-sheet.com) to be posted with the message. Or use [Custom Emoji](https://my.slack.com/customize/emoji). If nothing is entered the default is a Slack emoji.
  * Optional: Enter the URL to a publically sharable URL for an image file that will be displayed inside a message attachment. Slack currently supports the following formats: GIF, JPEG, PNG, and BMP.
  * Optional: Enter the file path to a local file to upload to Slack.

## Back-end info
* The plugin uses the Slack incoming webhook integration [API](https://api.slack.com/incoming-webhooks).
* The plugin uses an URL shortener to shorten the image URL. The script runs through several shortener websites to do this, but bit.ly requires an access token to work. The file plugin.py needs to edited to include your token if you want to use that service.
* The plugin will attempt to get your user information from Slack to fill in the channels available in your team and to retrieve your username. Turning on debugging mode will expose your Slack user credentials (including ID, username, user icon, user color, real name, status and email address) in the Indigo log.
* The plugin will attempt to get your [gravatar](http://gravatar.com) using your Slack email address if a Slack icon does not exist.

## Dependencies
Indigo plugins (the IOM and SDK) use Python 2.5

## Plugin ID
To programmatically restart the plugin, the Plugin ID is: com.bot.indigoplugin.slack

## Uninstall
Remove “/Library/Application Support/Perceptive Automation/Indigo 6/Plugins/Slack.indigoPlugin” (or check in the Disabled Plugins folder if disabled) and restart the Indigo Server

## GitHub Gist
For a simple python script version: [indigotoslack](https://gist.github.com/achterberg/cbd46bc3b9cdb391eed7)
