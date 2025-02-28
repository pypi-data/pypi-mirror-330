import os
import errno
import queue
import select
import socket
import logging
import threading
import time as tm

from .cosmetics import colorize, colored_variables
from .cosmetics import check

keepReading = True
logger = logging.getLogger("i3")
incoming = queue.SimpleQueue()
threads = []


def socket_listen(host="localhost", port: int = 9000):
    myname = colorize("socket_listen()", "green")
    logger.info(f"{myname} Started   {colored_variables(host, port)}")

    while keepReading:
        # Open a socket to connect FIFOShare
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
        except:
            logger.info("fifoshare server not available")
            k = 5
            while k > 0:
                # logger.debug('Try again in {} second{} ... '.format(k, 's' if k > 1 else ''), end='\r')
                s = "s" if k > 1 else ""
                print(f"Try again in {k} second{s} ... ", end="\r")
                tm.sleep(1.0)
                k -= 1
            continue
        sock.setblocking(0)
        logger.info(f"{myname} fifoshare connection {host} established")

        localMemory = b""

        while keepReading:
            # Check if the socket is ready to read
            readyToRead, _, selectError = select.select([sock], [], [sock], 0.1)
            if selectError:
                logger.error(f"{myname} Error in select() {selectError}")
                break
            elif readyToRead:
                try:
                    r = sock.recv(1024)
                    logger.debug(f"{myname} recv() -> {r}")
                    if r[:4] == b'\xff\x00\x00\x00':
                        continue
                except:
                    logger.warning(f"{myname} fifoshare connection interrupted.")
                    break
                if not r:
                    logger.debug(f"{myname} fifoshare connection closed.")
                    break
            else:
                continue

            # Concatenate the received string into local memory and consume it
            localMemory += r
            files = localMemory.decode("ascii").split("\n")
            localMemory = files[-1].encode("utf")
            logger.debug(f"{myname}   {colored_variables(files)}")

            for file in files[:-1]:
                logger.debug(f"{myname} listen() -> '{file}' ({len(file)})")
                if len(file) == 0:
                    continue
                # At this point, the filename is considered good
                file = os.path.expanduser(file)
                incoming.put(file)

        # Out of the second keepReading loop. Maybe there was an error in select(), close and retry
        sock.close()
        logger.info(f"{myname} fifoshare connection terminated")
        if keepReading:
            k = 50
            while k > 0 and keepReading:
                tm.sleep(0.1)
                k -= 1


def fifo_listen(pipe="/tmp/pipe.fifo"):
    myname = colorize("fifo_listen()", "green")
    logger.info(f"{myname}   {colored_variables(pipe)}")

    while keepReading:
        try:
            fd = os.open(pipe, os.O_RDONLY | os.O_NONBLOCK)
            while keepReading:
                try:
                    line = os.read(fd, 1024)
                except OSError as e:
                    if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                        tm.sleep(0.1)
                        continue
                    else:
                        k = 5
                        while k > 0:
                            s = "s" if k > 1 else ""
                            print(f"Try again in {k} second{s} ... ", end="\r")
                            tm.sleep(1.0)
                            k -= 1
                        break
                if not line:
                    tm.sleep(0.1)
                    continue
                line = line.decode("utf-8").strip()
                if len(line) == 0:
                    logger.debug("Empty line")
                    continue
                # At this point, the filename is considered good
                file = os.path.expanduser(line)
                incoming.put(file)
        except Exception as e:
            logger.error(f"Error in fifo_listen() {e}")
        if keepReading:
            k = 50
            while k > 0 and keepReading:
                tm.sleep(0.1)
                k -= 1


def deliver(callback=None):
    while keepReading:
        try:
            file = incoming.get(timeout=0.1)
            logger.debug(f"{colorize(file, 'mint')}  {check}")
            if callback:
                callback(file)
        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"Error in start() {e}")
            break


def start(sources: list = ["/tmp/s3.fifo"], callback=None):
    """
    Start the traffic listener
    """
    global keepReading
    keepReading = True

    for source in sources:
        if "/" in source or "fifo" in source:
            thread = threading.Thread(target=fifo_listen, args=(source,))
            thread.start()
            threads.append(thread)
        else:
            if ":" in source:
                host, port = source.split(":")
                port = int(port)
                thread = threading.Thread(target=socket_listen, args=(host, port))
                thread.start()
                threads.append(thread)
            else:
                thread = threading.Thread(target=socket_listen, args=(source,))
                thread.start()
                threads.append(thread)

    thread = threading.Thread(target=deliver, args=(callback,))
    thread.start()
    threads.append(thread)


def stop():
    global keepReading
    keepReading = False
    for thread in threads:
        thread.join()


def set_logger(newLogger):
    global logger
    logger = newLogger
