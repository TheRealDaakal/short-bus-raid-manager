# Deploying to a VPS

Tested against a $4-6/mo Ubuntu box (DigitalOcean, Hetzner, Vultr - any of them work the same way).

## 1. Create the server

Spin up the cheapest Ubuntu 22.04 (or 24.04) droplet/instance from your provider of choice.
SSH in as root, then create a non-root user to run the bot as:

```bash
adduser jawa
usermod -aG sudo jawa
su - jawa
```

## 2. Install prerequisites

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git fonts-dejavu-core
```

(`fonts-dejavu-core` gives the wheel-spin GIF a proper bold font on Linux -
same visual result as on Windows, just a different font file.)

## 3. Get the code

```bash
cd ~
git clone https://github.com/TheRealDaakal/short-bus-jawa.git
cd short-bus-jawa
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Configure

```bash
cp .env.example .env
nano .env
```

Fill in `DISCORD_TOKEN`. Leave `DEV_GUILD_ID` blank (that's dev-only).

## 5. Bring over your existing database

If you've already been running the bot locally (officer roles, welcome message,
automod config, tickets, raid templates, etc. are all already set), copy that
database up rather than starting fresh - otherwise the VPS starts completely
blank and you'd have to redo every `/settings` command.

From your **local machine** (not the server), with the local bot stopped first
so the file isn't being written to mid-copy:

```powershell
scp "C:\Users\davew\Documents\WhirlwindFX\SWTOR-Raid-Manager\database\short_bus_jawa.db" jawa@YOUR_SERVER_IP:~/short-bus-jawa/database/
```

(Run this from PowerShell. Replace `YOUR_SERVER_IP` with the droplet's IP address.)

## 6. Run it as a service (so it survives reboots/crashes)

```bash
sudo cp deploy/short-bus-jawa.service /etc/systemd/system/
sudo nano /etc/systemd/system/short-bus-jawa.service
```

Update the `User`, `WorkingDirectory`, and `ExecStart` paths in that file to match
your actual username and clone location if they differ from `jawa` /
`/home/jawa/short-bus-jawa`.

```bash
sudo systemctl daemon-reload
sudo systemctl enable short-bus-jawa
sudo systemctl start short-bus-jawa
```

## 7. Check it's running

```bash
sudo systemctl status short-bus-jawa
journalctl -u short-bus-jawa -f
```

## Auto-restart behavior

`Restart=on-failure` restarts the bot if it crashes or exits. On top of that,
the service also uses a **systemd watchdog** (`WatchdogSec=60`): the bot pings
systemd every 20 seconds while its event loop is healthy, and if those pings
stop arriving (a genuine hang, not just a crash), systemd force-kills and
restarts it too. No action needed - this is already wired up in `bot.py` and
the service file, and does nothing on non-systemd systems (like local dev).

`journalctl -u short-bus-jawa -f` tails live logs - watch for "Logged in as
Short Bus Raid Manager" to confirm it connected.

## Updating later

```bash
cd ~/short-bus-jawa
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart short-bus-jawa
```

## Notes

- **Stop the local copy before starting the VPS one.** The same bot token can't
  usefully run in two places at once - both processes will try to respond to every
  command, sync commands against each other, and generally fight. Once the VPS is
  confirmed running, don't start `bot.py` locally again unless the VPS one is stopped.
- The SQLite database (`database/short_bus_jawa.db`) lives on the server's disk under
  the repo folder. Back it up periodically (`scp` it down, or `cron` a copy) - if the
  server is ever destroyed without a backup, raid history, settings, tickets, and
  templates go with it.
- Enable **Server Members Intent** and **Message Content Intent** for this bot in the
  Discord Developer Portal (Bot page) before starting it, or login will fail outright.
  (Already enabled currently, since the local bot has been running fine with both -
  this only matters if you ever recreate the bot application from scratch.)

## Optional hardening (not required, but worth doing eventually)

- `sudo ufw allow OpenSSH && sudo ufw enable` - a basic firewall that only allows
  SSH in. This bot doesn't need to accept any other inbound connections.
- Once you've confirmed the SSH key works, consider disabling password login
  entirely (`PasswordAuthentication no` in `/etc/ssh/sshd_config`, then
  `sudo systemctl restart sshd`) - closes off brute-force login attempts, which
  every internet-facing server gets constantly.
