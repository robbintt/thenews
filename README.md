
### The News!

Keep up to date with the world. Get reddit's top 100 posts delivered to your inbox in an orderly fashion on the schedule you prefer.


#### What?

Copy the secret.cfg.example to secret.cfg and add your information. Don't share your secrets with other people.


#### Is it safe?

Short Answer: As safe as your server.

I recommend using a fresh gmail account as a relay since you have to store a password in the cron file.

You should also use a fresh reddit account intended for this purpose.


#### So, how do I do the cron part?

I put thenews/ in /home/myusername/bin, then added this line to my cron (type `crontab -e`):
`0 */12 * * * cd bin/thenews; ./thenews`
