import time

from openobd import *
from .stream_handler import StreamHandler, StreamState
from openobd_protocol.Session.Messages import Session_pb2 as grpcSession
import threading


class SessionContext:

    def __init__(self, openobd_session: OpenOBDSession):
        """
        Authenticates the given openOBD session and starts a thread to keep the session active by periodically updating
        its session token.

        :param openobd_session: a newly created OpenOBDSession that should remain active.
        """
        self.openobd_session = openobd_session

        '''Start session context'''
        self.openobd_session.start_context()

        '''Keep track of exactly this context that we want to monitor'''
        self.session_context = self.openobd_session.session_context

        '''
        Create stream handler for receiving session context updates
        The argument is the context that we want to monitor, after that we will just listen
        to an incoming stream for updates (until the context is finished)'''
        self.stream_handler = StreamHandler(self.openobd_session.monitor_context, request=self.openobd_session.session_context)

        self.refresh_session_context_thread = threading.Thread(target=self._monitor_session_context, daemon=True)
        self.refresh_session_context_thread.start()

    def get_session_info(self) -> SessionInfo:
        return self.openobd_session.session_info

    def _monitor_session_context(self):
        print(f" [+] openOBD session [{self.openobd_session.id()}] => " + \
              f"start monitoring context [{self.openobd_session.session_context.id}]")
        try:
            while True:
                session_context = self.stream_handler.receive()    # type: grpcSession.SessionContext
                self.openobd_session.session_context = session_context
                if session_context.finished:
                    '''Context has finished'''
                    print(f" [+] openOBD session [{self.openobd_session.id()}] => " + \
                          f"finished context [{self.openobd_session.session_context.id}]")

                    '''Allow authentication again from openOBD session'''
                    self.openobd_session.session_token = session_context.authentication_token
                    break

        except OpenOBDException as e:
            print(f" [!] openOBD session [{self.openobd_session.id()}] => " + \
                  f"stopped monitoring context [{self.openobd_session.session_context.id}] due to an exception")
            print(e)
        finally:
            self.stream_handler.stop_stream()

        print(f" [+] Stopped monitoring on context [{self.openobd_session.session_context.id}]")

    def stop_stream(self) -> None:
        """
        Closes the gRPC stream if it is not already closed. A new ContextMonitor object will have to be created to
        start another stream.
        """
        self.stream_handler.stop_stream()

    def active(self) -> bool:
        if self.stream_handler.stream_state == StreamState.ACTIVE:
            return True
        return False

    def wait(self) -> None:
        try:
            while self.active():
                time.sleep(1)
        except Exception:
            pass

