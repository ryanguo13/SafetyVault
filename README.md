## Mechachronics Final Project

### Versions Clarification
```
v1 => Initial setup, only about transfering the messages.
v2 => Using USB port to send and receieve data, with sha256 method. With the function of judging.
```

### Progress
```
MPY: soft reboot
Pico hardware wallet is ready.
```

In the PC, execute the Python file and start verify.
```
Connecting to hardware wallet...
Challenge sent: 4b98bcc187e2e0e4d88012ac528638e07bf9c9c74878779fc312a946b3c6597b
Raw signature received: 2afadfa5e284878cb1ea79c03fe857900a8bbab33d0e00e7f2209a7286f06e43
Verification successful: Access granted
```

In the case tha that the private key is not correct:
```
Connecting to hardware wallet...
Challenge sent: eb27ca5d847125481d5e99c9882c0ff76980900ae9889b553f1c54339d1c444b
Raw signature received: 
Verification failed: Access denied
```