# TwiKit_extended
[![Telegram channel](https://img.shields.io/endpoint?url=https://runkit.io/damiankrawczyk/telegram-badge/branches/master?url=https://t.me/bots_forge)](https://t.me/bots_forge)

Надстройка над [twikit](https://github.com/d60/twikit) от [d60](https://github.com/d60).
Теперь Client связан с Profile.

## Installation
```bash
pip install twikit_ext
```

## Examples
```python
try:
    async with Client({'auth_token': 'sdf123...'}) as client:
        client.connect()
        ...
finally:
    client.profile.save('profile.json')
```

## Added methods
```python
Client.change_username()
Client.change_name()
Client.change_bio()
Client.change_location()
Client.change_password()
Client.get_enabled_two_factor_methods()
Client.is_totp_enabled()
Client.disable_totp()
Client.enable_totp()
Client.is_backup_code_enabled()
Client.get_backup_code()
Client.change_backup_code()
Client.oauth2()
```

## Support
Developed by `MrSmith06`: [telegram](https://t.me/Mr_Smith06) |  [gtihub](https://github.com/MrSmith06)
If you find this project helpful, feel free to leave a tip!
- EVM address (metamask): `0x6201d7364F01772F8FbDce67A9900d505950aB99`