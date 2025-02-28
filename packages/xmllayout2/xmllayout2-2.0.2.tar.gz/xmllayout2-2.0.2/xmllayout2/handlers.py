"""logging Handlers"""
import logging.handlers
import sys

__all__ = ['RawSocketHandler']

PY3 = sys.version_info >= (3,)


class RawSocketHandler(logging.handlers.SocketHandler):
    """Logging Handler that writes log records to a streaming socket.

    Like ``logging.handlers.SocketHandler``, but writes the actual formatted
    log record (not a pickled version).
    """

    def emit(self, record):
        """Emit a record.

        Formats the record and writes it to the socket in binary format. If
        there is an error with the socket, silently drop the packet. If there
        was a problem with the socket, re-establishes the socket.
        """
        try:
            msg = self.format(record)
            if PY3:
                self.send(msg.encode())
            else:
                self.send(msg.encode('utf-8'))
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
