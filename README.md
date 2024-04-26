# deye-mithm
Man in the middle tracer of traffic between Deye inverter and AWS cloud


## Sources

This is a modified mixture of two Github repositories.

## https://github.com/Hypfer/deye-microinverter-cloud-free

Provides the idea how to interpret the binary data sent into the Amazon cloud.
However I want no keep the cloud connectivity, just tee the packets and replicate them
to my own logger, which is a Splunk HEC (http Event Collector). The original provides a dummy server.

## https://github.com/ickerwx/tcpproxy

Provides the idea how to implement a proxy, however that thing may get berserk in the communication
between Inverter and Cloud (an Amazon TCP load balancer) from time to time for unknown reasons.
Maybe this is caused by improper handling of socket close reset packets received.
I tried to reimplement it, not to nice in terms of the modules, but maybe better in terms of state handlicng.
A master listens on a port, on incoming connection a child thread is created.
The child thread forks two communication threads, one for each direction.
You are not supposed to kill a thread, so it will be in an endless timeout / try to read data loop.
If one of these sockets die the thread exits, the intermediate controller closes the two sockets, so
the other directional transport thread dies as well.
