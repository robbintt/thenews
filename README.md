
### The News!

Keep up to date with the world. Get reddit's top 100 posts delivered to your inbox in an orderly fashion on the schedule you prefer. Scheduler not provided. Use cron.

Caveat Emptor - This is a quick script. It is extremely sensitive and will break if anything changes. If it proves useful, it will improve.

**Disclaimer - reddit has porn and violence. This does not filter these things. Ask me if you want to filter these things, I believe it is possible.**


#### So, how do I do it?

First of all, you need to have a server running that has: `python 2.7`, `cron`, `internet access` and `more stuff`

Make a new reddit account, add an app, choose developer. Get the app ID (string of random looking characters) and the app SECRET (also a string of random looking characters) and put them in the secret.cfg. file.

Make a new gmail account, allow 'less secure apps': https://support.google.com/accounts/answer/6010255?hl=en

Copy the secret.cfg.example to secret.cfg and add your information. Don't share your secrets with other people.

Put the gmail account and password in the config file.

Put your email in the config file under `recepient`.


I put `thenews/` in `/home/myusername/bin`, then added this line to cron:

`0 9,21 * * * cd bin/thenews; ./thenews`


#### Other Stuff

You can ignore or prioritize by adding them to the respective section in secret.cfg

You can add more than one recepient.


#### Is it safe?

Short Answer: As safe as your server.

It is best to use a fresh gmail account because you have to store a password in the secret.cfg file.

You should also use a fresh reddit account intended for this purpose.


#### License

Copyright (c) 2015 Trent Robbins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
