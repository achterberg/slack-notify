## Summary
This plugin extends [Indigo](http://www.indigodomo.com) allowing it to send messages and attachments to [Slack](https://slack.com).
## Installation
* Download the zip file
* Unzip the file
* On the computer with Indigo running, double-click the file "Slack.indigoPlugin" inside the folder created above
* Follow the Indigo dialog and enable the plugin
* The plugin should be visible in the Plugins drop-down menu as "Slack Notify"

## Configuration
###Configure Plugin
In the menu: Indigo 6/Plugins/Slack Notify/Configure...
  * A Slack Team is required. Register for an account at [Slack](https://slack.com) and set up a team
  * Optional: Create a channel to be used for Slack Notify (recommended), or use one of the defaults
  
####WebHook Token
  * Set up an incoming webhook integration by reading and following the link on: https://api.slack.com/incoming-webhooks
  * An URL should be generated and after services/ the series of numbers/letters is the token
  * Enter this in the WebHook Token field
  
####Slack Token
  * Go [here](https://api.slack.com/web)
  * Under Authentication there should be a team Token
  * Enter this in the Slack Token field
  
####User ID
  * Go to the following link, replacing the part after = with the slack token above
  * https://slack.com/api/users.list?token=replacewithSlackToken
  * Look for the line begining with: "id":
  * Enter this in the User ID field
  
###Configure Notifications
  * The plugin will show under Type: Notification Actions under Actions as Slack Notify.
  * Once added to a TRIGGER, SCHEDULE or ACTION GROUPS, click on Edit Action Settings...
  * The Channel drop down menu should be auto populated with channels in your team; select one.
  * Alternately send a [Direct Message](https://slack.zendesk.com/hc/en-us/articles/202009646-Using-channel-group-everyone) by entering text in the Direct Message field.
  * Enter text in the Text field, following the formatting hints listed below the field.
  * Optional: Enter a username to be posted as. If blank, the plugin will use your username and post as a bot.
  * Optional: Enter an icon name to be posted with the message. This can be the built-in Slack icons or you can use [custom icon names](https://my.slack.com/customize/emoji).
  * Optional: Enter the URL to a publically sharable URL for an image file that will be displayed inside a message attachment. Slack currently supports the following formats: GIF, JPEG, PNG, and BMP.
  * Optional: Enter the file path to a local file to upload to Slack.
