xmllayout2 provides a Python logging Formatter that formats log messages as XML,
according to `log4j's [XMLLayout specification](https://logging.apache.org/log4j/1.2/apidocs/org/apache/log4j/xml/XMLLayout.html)

xmllayout2 formatted log messages can be viewed and filtered within the
[Chainsaw](https://logging.apache.org/chainsaw/2.x) application
(see the example section below), part of the Java based log4j project.

This is a fork of Philip Jenveys fork of [xmllayout](https://github.com/perillaseed/xmllayout) maintained for usage in commercial projects, with supporting a variety of Python versions.

# Installation
via pip: `pip install xmllayout2`

for local development: `pip install .`

# Usage
This package includes a `RawSocketHandler` -- like
`logging.handler.SocketHandler`, but sends the raw log message over the socket
instead of a pickled version. `RawSocketHandler` can be configured to send log
messages to Chainsaw directly over a socket.

For example to forward log messages to Chainsaw, if it were listening on
localhost port 4448:

    import logging
    import xmllayout2

    handler = xmllayout2.RawSocketHandler('localhost', 4448)
    handler.setFormatter(xmllayout2.XMLLayout())
    logging.root.addHandler(handler)


