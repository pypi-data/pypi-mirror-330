import paramiko
import os
from scp import SCPClient
import stat
import time
from PIL import Image
import re
from tqdm import tqdm
from pyappleinternal.bootargs import BootArgs
from pyappleinternal.copyUnrestricted import copyUnrestricted
from pyappleinternal.authorized_key import authorized
from pyappleinternal.tcp_forwarder import UsbmuxTcpForwarder
import socket
import threading
import sys


class SSHTransports():
    def __init__(self, udid, internal=True):
        super().__init__()
        self.udid = udid
        self.host = "localhost"
        self.username = "root"
        self.client_on = None
        self.invoke_shell_on = None
        self.internal = internal
        self.usb_port_forward=None
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.port = self.find_unused_ports(10000, 19999, 10)[0]
        self.copyUnrestricted = copyUnrestricted(self.udid, self.internal)
        self.BootArgs = BootArgs()

    def thread_it(self,fun,args=()):
        command = threading.Thread(target=fun,args=(*args,))
        if sys.version_info >= (3, 10):
            command.daemon = True
        else:
            command.setDaemon(True)
        command.start()
        return  command

    def is_connect(self):
        return self.client.get_transport() is not None and self.client.get_transport().is_active()

    def connect(self):
        if not self.is_connect():
            authorized(self.udid, self.internal)
            # sock = paramiko.ProxyCommand(f"/usr/libexec/remotectl netcat {self.udid} com.apple.internal.ssh")
            if self.usb_port_forward == None:
                self.usb_port_forward = UsbmuxTcpForwarder(self.udid, 22, self.port)
                self.thread_it(self.usb_port_forward.start)
            self.client.connect(hostname=self.host, username=self.username,port=self.port,
                                key_filename=f'{os.path.expanduser("~")}/.ssh/id_ed25519', timeout=5)

    def is_port_open(self, port, host='localhost'):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0

    def find_unused_ports(self, start_port, end_port, step, host='localhost'):
        unused_ports = []
        for port in range(start_port, end_port + 1, step):
            if not self.is_port_open(port, host):
                unused_ports.append(port)
        return unused_ports

    def command(self, command, timeout=5):
        try:
            self.connect()
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            output = stdout.read().decode('utf-8').strip()
            outerr = stderr.read().decode('utf-8').strip()
            return output + outerr
        except Exception as e:
            print(e)
            return False

    def invoke_shell(self, command):
        try:
            self.connect()
            if self.invoke_shell_on is None:
                self.invoke_shell_on = self.client.invoke_shell()
            self.invoke_shell_on.send(command + "\n")
        except Exception as e:
            print(f"Error in invoke_shell: {e}")

    def invoke_close(self):
        try:
            if self.invoke_shell_on is not None:
                self.invoke_shell_on.close()
                self.invoke_shell_on = None
        except Exception as e:
            print(f"Error in close invoke_shell: {e}")

    def cam_shell(self, command):
        try:
            self.connect()
            self.client_on = self.client.invoke_shell()
            self.client_on.send("mkdir /tmp/take_photo &>/dev/null \n")
            self.client_on.send("cd /tmp/take_photo\n")
            self.client_on.send("OSDToolbox display -s 1 &\n")
            self.client_on.send("killall h16isp\n")
            self.client_on.send("h16isp -j\n")
            self.client_on.send("forget\n")
            self.client_on.send("on\n")
            self.client_on.send("v\n")
            self.client_on.send(command)
        except Exception as e:
            print(e)

    def tele_on(self):
        self.cam_mode = 1
        self.cam_shell("start 1 139 0 \n")

    def swide_on(self):
        self.cam_mode = 4
        self.cam_shell("start 4 139 0 \n")

    def default_on(self):
        self.cam_mode = 0
        self.cam_shell("start 0 255 0 \n")

    def focus(self):
        if self.client_on != None:
            self.client_on.send(f"f {self.cam_mode}\n")

    def exit_cam(self):
        if self.client_on != None:
            self.client_on.close()
            self.client_on = None

    def save_image(self):
        try:
            if self.client_on != None:
                self.client_on.send(f"\n")
                self.client_on.recv(2048)
                self.client_on.send(f"p 1\n")
                time.sleep(1)
                output = self.client_on.recv(2048).decode('utf-8')
                match = re.search(r'(?i)\./\S+\.(jpg|png|jpeg|tiff|bmp|heif|heic|raw)', output)
                if match:
                    filename = os.path.basename(match.group(0))
                    timestamp = int(time.time())
                    self.download(f'/tmp/take_photo/{filename}', os.path.expanduser(f"~/Desktop/photo_{timestamp}.jpg"))
                else:
                    self.screenshot(True)
        except Exception as e:
            print(e)

    def upload(self, local_path, remote_path, callback=None):
        try:
            self.connect()
            scp = SCPClient(self.client.get_transport(),
                            progress=lambda filename, size, sent: self.progress(filename, size, sent, local_path,
                                                                                callback))  # 添加进度回调
            scp.put(local_path, remote_path, recursive=True)
            scp.close()
        except Exception as e:
            print(e)

    def download(self, remote_path, local_path, callback=None):
        try:
            self.connect()
            scp = SCPClient(self.client.get_transport(),
                            progress=lambda filename, size, sent: self.progress(filename, size, sent, remote_path,
                                                                                callback))  # 添加进度回调
            scp.get(remote_path, local_path, recursive=True)
            scp.close()
        except Exception as e:
            print(e)

    def delete(self, remote_path):
        status = True
        try:
            self.command(f"rm -rf '{remote_path}'")
        except Exception as e:
            status = False
        finally:
            return status

    def movefile(self, original_path, target_path):
        status = True
        try:
            self.connect()
            sftp = self.client.open_sftp()
            sftp.rename(original_path, target_path)
        except Exception as e:
            status = False
        finally:
            sftp.close()
            return status

    def mkdir(self, remote_path):
        status = True
        try:
            self.connect()
            sftp = self.client.open_sftp()
            sftp.mkdir(remote_path)
        except Exception as e:
            status = False
        finally:
            return status

    def list_files_with_stat(self, remote_path):
        file_reslut = {}
        file_reslut[remote_path] = {}
        try:
            self.connect()
            sftp = self.client.open_sftp()
            files = sftp.listdir_attr(remote_path)
            for file in files:
                real_filetype=None
                filename = file.filename
                if stat.S_ISDIR(file.st_mode):
                    filetype = "Directory"
                elif stat.S_ISLNK(file.st_mode):
                    filetype = "Symlink"
                else:
                    filetype = "File"
                filepath = os.path.join(remote_path, filename)
                if filetype == "Symlink":
                    real_path = self.get_real_link(filepath)
                    filepath = "/" + "/".join(part for part in real_path.split("/") if part and not part.startswith(".."))
                    if self.is_directory(sftp,filepath):
                        real_filetype="Directory"
                    else:real_filetype="File"
                size = self.convert_size(file.st_size)
                file_extension = filename.split(".")[-1].lower() if "." in filename else ""
                file_reslut[remote_path][filename] = {
                    "file_path": filepath,
                    "file_type": filetype,
                    "file_size": size,
                    "file_extension": file_extension,
                    "file_real_type":real_filetype
                }
        except Exception as e:
            print(e)
            file_reslut = None
        finally:
            sftp.close()
            return file_reslut

    def is_directory(self, sftp, remote_path):
        try:
            return stat.S_ISDIR(sftp.stat(remote_path).st_mode)
        except IOError:
            return False

    def convert_size(self, size):
        if size < 1000:
            return f"{size} B"
        elif size < 1000 * 1000:
            return f"{size / 1000:.2f} KB"
        elif size < 1000 * 1000 * 1000:
            return f"{size / (1000 * 1000):.2f} MB"
        else:
            return f"{size / (1000 * 1000 * 1000):.2f} GB"

    def get_real_link(self, link_path):
        target_path = None
        try:
            self.connect()
            sftp = self.client.open_sftp()
            target_path = sftp.readlink(link_path)
        except Exception as e:
            pass
        finally:
            sftp.close()
            return target_path

    def compress(self, enter_path, save_name, remote_name):
        try:
            file_path = os.path.join(enter_path, save_name + ".tar.gz")
            remote_list = " ".join([f"'{i}'" for i in remote_name])
            self.command(f"cd {enter_path};tar -czvf '{save_name}'.tar.gz {remote_list}")
            sftp = self.client.open_sftp()
            try:
                sftp.stat(file_path)
                return file_path
            except:
                return False
        except Exception as e:
            return False

    def decompress(self, remote_path):
        try:
            result = self.command(f"cd '{os.path.dirname(remote_path)}';tar -xvf '{remote_path}'")
            return True
        except Exception as e:
            return str(e)

    def get_bootargs(self):
        try:
            result = self.command("diagstool bootargs --print", timeout=3).replace("boot-args=", '')
            return result
        except:
            return False

    def set_bootargs(self, text):
        try:
            self.command(f'OSDToolbox display -s 1 &>/dev/null & nvram boot-args="{text}";OSDToolbox appswitch -b')
            return self.get_bootargs()
        except:
            return False

    def screenshot(self, cut=False):
        try:
            timestamp = int(time.time())
            png_path = f"/tmp/screenshot_{timestamp}.png"
            self.command(f"/usr/local/bin/CADebug -c '{png_path}'")
            local_path = os.path.expanduser(f"~/Desktop/screenshot_{timestamp}.png")
            self.download(png_path, local_path)
            if cut == True:
                image = Image.open(local_path)
                width, height = image.size
                new_height = height * 0.642
                crop_box = (0, (height - new_height) // 2, width, (height + new_height) // 2)  # 上下裁剪
                cropped_image = image.crop(crop_box)
                cropped_image.save(local_path)
        except Exception as e:
            print(e)

    def showimage(self, path):
        try:
            name = os.path.basename(path)
            self.mkdir("/tmp/player/")
            self.upload(path, "/tmp/player/")
            command = self.BootArgs.generate_bootargs("newLcdMura=MagicalStarsign", "", [], "os")
            self.command(command)
            self.command("OSDToolbox appswitch -b")
            self.command("diagstool lcdmura --start-test StarsignTest")
            self.command(f"diagstool lcdmura --imagepath '/tmp/player/{name}'")
        except Exception as e:
            print(e)

    def play(self, path):
        try:
            name = os.path.basename(path)
            self.mkdir("/tmp/player/")
            self.upload(path, "/tmp/player/")
            self.command(f"figplayAV -volume 1.0 '/tmp/player/{name}' &")
        except Exception as e:
            print(e)

    def progress(self, filename, size, sent, remote_path, callback=None):
        if isinstance(filename, (bytes, bytearray)):
            filename = filename.decode("utf-8")
        percent = (sent / size) * 100
        if callable(callback):
            callback(self.udid, remote_path, filename, percent)
        else:
            bar = tqdm(
                total=size,
                ncols=100,
                bar_format=f"{filename} " + "{bar}| {percentage:3.0f}%"
            )
            bar.update(sent - bar.n) 