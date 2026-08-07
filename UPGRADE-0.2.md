
# Upgrade PhotoVault 0.1 -> 0.2

## Mac
Copy this package over your existing local PhotoVault repository, then:

```bash
cd ~/Documents/PhotoVault
git add -A
git commit -m "Add PhotoVault 0.2 scanner"
git push
```

## Unraid

```bash
cd /mnt/user/photovault/source
git pull
```

Then rebuild/recreate the PhotoVault stack in Compose Manager Plus.

Verify:

```text
http://YOUR-UNRAID-IP:5000/health
```

It should report version `0.2.0`.

Start the first scan from:

```text
http://YOUR-UNRAID-IP:5000/docs
```

Open `POST /scan`, click **Try it out**, leave the body as `{}`, then click **Execute**.
Use `GET /scan/status` and `GET /stats` to follow progress.
