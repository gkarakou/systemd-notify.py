#!/usr/bin/python2
<<<<<<< HEAD
import os
import shutil
from systemd import journal
import subprocess as sub
import argparse

class Installer():
    """
    Installer
    :desc : Class that installs either systemd-denotify.py v2 or v3
    """

    def __init__(self):
        """
        __init__
        :desc : Function constructor
        Instantiates the installer

        """

    def get_euid(self):
        """
        get_euid_
        :desc : Function that returns effective user id as int
        return int
        """
        uid=os.geteuid()
 #       print "getting uid: "+ str(uid)
        return uid

   # def set_euid(self, *args):
   #     """set_euid
   #     return int
   #     :param *args:
   #     """
   #     euid = int(sys.argv[1])
   #     setuid = os.seteuid(euid)
   #     if setuid == None:
   #         pass
           # print("setting uid: "+ str(self.get_euid()))
   #     return setuid

    def is_archlinux(self):
        """
        is_archlinux
        return void
        :desc: function that checks if the underlying os is archlinux
        checks for the existense of /etc/pacman.conf
        if it is there (os is definitely arch) , we open the file systemd-denotify.py rw to have as interpreter python2
        """
        if  os.path.isfile("/etc/pacman.conf"):
            path = os.path.dirname(os.path.abspath(__file__))
            data = ""
            with open(path+"/systemd-denotify.py", "r+") as fin:
                data += fin.read()
                fin.seek(0)
                data_replace = data.replace("python", "python2")
                fin.write(data_replace)
                fin.truncate()
                journal.send("systemd-denotify: "+ "Os was arch.")

        else:
            #print("os wasnt arch")
            pass

    def addXuser_to_group(self):
        """addXuser_to_group
        return void
        :desc : Function that adds the logedin user to systemd-journal group
        CREDITS->http://pymotw.com/2/subprocess/
        """
        login = os.getlogin()
        try:
            who = sub.Popen(['/usr/bin/w'], stdout=sub.PIPE, stderr=sub.PIPE)
            grep = sub.Popen(['/usr/bin/grep', ':0'], stdin=who.stdout, stdout=sub.PIPE)
            cut = sub.Popen(['/usr/bin/cut', '-d ', '-f1'], stdin=grep.stdout, stdout=sub.PIPE)
            sort = sub.Popen(['/usr/bin/sort'], stdin=cut.stdout, stdout=sub.PIPE)
            uniq = sub.Popen(['/usr/bin/uniq'], stdin=sort.stdout, stdout=sub.PIPE)
            who.stdout.close()
            grep.stdout.close()
            cut.stdout.close()
            sort.stdout.close()
            end_of_pipe = uniq.stdout
            for line in end_of_pipe:
                data = line.strip()
                stringify = str(data.decode("utf-8"))
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-denotify: "+message)
        #this will autoraise  if exit status non zero
        if login == stringify:
            command = '/usr/sbin/usermod -a -G systemd-journal '+ stringify
            usermod = sub.check_call(command.split(), shell=False)
            if usermod:
                journal.send("systemd-denotify:" +  "Your user was added to the systemd-journal group.You must relogin for the changes to take effect.")
                return True
            else:
                journal.send("systemd-denotify: "+"Your user was not added to the systemd-journal group,but there is a possibility he is already a member of the group.")
                return False
        elif stringify != login:
            command = '/usr/sbin/usermod -a -G systemd-journal '+ stringify
            usermod = sub.check_call(command.split(), shell=False)
            if usermod:
                journal.send("systemd-denotify: "+ "While your login user doesnt match the Xorg loggedin user,he was added to the systemd-journal group.You must relogin for the changes to take effect.")
                return True
            else:
                journal.send("systemd-denotify: "+"Your Xorg loggedin user was not added to the systemd-journal group,but there is a possibility he is already a member of the group.")
                return False
        else:
            command = '/usr/sbin/usermod -a -G systemd-journal '+ login
            usermod = sub.check_call(command.split(), shell=False)
            if usermod:
                journal.send("systemd-denotify: "+ "While we couldnt find the Xorg loggedin user,your loggedin user was added to the systemd-journal group.You must relogin for the changes to take effect.")
                return True
            else:
                journal.send("systemd-denotify: "+ "Your loggedin user was not added to the systemd-journal group, but there is a possibility he is already a member of the group.")
                return False


    def install_v2(self):
        """install_v2
        :return void
        :desc: function that does the heavy job. Copies the v2 files to appropriate places.
         This func also chmod's the files so that the user that starts X is ab        le to execute the program.
        """
        path = os.path.dirname(os.path.abspath(__file__))
        src_c = path+"/systemd-denotify.py"
        src_d = path+"/systemd-denotify.desktop"
        src_e = path+"/systemd-denotify.conf"
        dst_c = "/usr/local/bin/systemd-denotify.py"
        dst_d = "/etc/xdg/autostart/systemd-denotify.desktop"
        dst_e = "/etc/systemd-denotify.conf"
        try:
            shutil.copy2(src_c, dst_c)
            shutil.copy2(src_d, dst_d)
            shutil.copy2(src_e, dst_e)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-denotify: "+message)
        try:
            os.chmod(dst_c, 0o755)
            os.chmod(dst_d, 0o644)
            os.chmod(dst_e, 0o644)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-denotify: "+message)

        journal.send("systemd-denotify: "+ "successfully installed v2.")

    def install_v3(self):
        """install_v3
        :return void
        :param start:str(actually bool casted to str) specifying whether the DbusNotify Class should be instantiated
        :param minutes:str(actually int casted to str) for the time interval between notifications
        :param *services: str of services separated by a space
        :desc: function that does the heavy job. Copies the v3 files to appropriate places and writes the command line args that
        will be used to start or not the DbusNotify Class. This func also chmod's the files so that the user that starts X is ab        le to execute the program.
        """
        path = os.path.dirname(os.path.abspath(__file__))
        data = ""
        with open(path+"/systemd-denotify.desktop", "r+") as fin:
            data += fin.read()
            fin.seek(0)
            data_replace = data.replace("Exec=/usr/local/bin/systemd-denotify.py", "Exec=/usr/local/bin/systemd-denotify3.py")
            fin.write(data_replace)
        src_c = path+"/systemd-denotify3.py"
        src_d = path+"/systemd-denotify.desktop"
        src_e = path+"/systemd-denotify.conf"
        dst_c = "/usr/local/bin/systemd-denotify3.py"
        dst_d = "/etc/xdg/autostart/systemd-denotify.desktop"
        dst_e = "/etc/systemd-denotify.conf"
        try:
            shutil.copy2(src_c, dst_c)
            shutil.copy2(src_d, dst_d)
            shutil.copy2(src_e, dst_e)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-denotify: "+message)
        try:
            os.chmod(dst_c, 0o755)
            os.chmod(dst_d, 0o644)
            os.chmod(dst_e, 0o644)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-denotify: "+message)
        journal.send("systemd-denotify: "+ "successfully installed v3.")

    #def __del__(self):

     #   del self.install_v2
     #   del self.install_v3


    def reset_desktop_file(self):
        path = os.path.dirname(os.path.abspath(__file__))
        data_replace = "[Desktop Entry]\nVersion=1.0\nName=system-denotify\nType=Application\nExec=/usr/local/bin/systemd-denotify.py"
        data = ""
        with open(path+"/systemd-denotify.desktop", "r+") as fin:
            data += fin.read()
            fin.seek(0)
            fin.write(data_replace)
            fin.truncate()

    def remove_old_version(self):
        files = ["/etc/systemd-desktop-notifications.conf", "/etc/xdg/autostart/systemd-notify.desktop", "/usr/local/bin/systemd-notify.py", "/usr/local/bin/systemd-notify3.py"]
        for f in files:
            if os.path.isfile(f):
                try:
                    os.remove(f)
                except OSError as e:  ## if failed, report it back to the user ##
                    journal.send("systemd-denotify: " + "Error: %s - %s." % (e.filename,e.strerror))

    def uninstall(self):
        files = ["/etc/systemd-denotify.conf", "/etc/xdg/autostart/systemd-denotify.desktop", "/usr/local/bin/systemd-denotify.py", "/usr/local/bin/systemd-denotify3.py"]
        for f in files:
            if os.path.isfile(f):
                try:
                    os.remove(f)
                except OSError as e:  ## if failed, report it back to the user ##
                    journal.send("systemd-denotify: " + "Error: %s - %s." % (e.filename,e.strerror))


installer = Installer()
installer.remove_old_version()
installer.reset_desktop_file()
parser = argparse.ArgumentParser(description="install version 2 or 3 of systemd-denotify(default is 2)")
parser.add_argument("-i", "--install", choices=['v2', 'v3'], default="v2")
parser.add_argument("-u", "--uninstall", action='store_true')
arguments = parser.parse_args()
if arguments.install == "v2":
    installer.is_archlinux()
    installer.addXuser_to_group()
    installer.install_v2()
elif arguments.install == "v3":
    installer.addXuser_to_group()
    installer.install_v3()
if arguments.uninstall:
    installer.uninstall()
=======

# Copyright (C) 2015 George Karakou (gkarakou)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You can get a copy of the GNU General Public License at
# <http://www.gnu.org/licenses/>.

#http://stackoverflow.com/questions/11536764/attempted-relative-import-in-non-package-even-with-init-py
#if __package__ is None:
#    import sys
#    from os import path
#    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#    from install_script import Installer
#else:
#    from .install_script import Installer
from distutils.core import setup
#import os
from setuptools.command.install import install

#class MyInstall(install):
#custom class derived from a stackoverflow answer
#    def run(self):
#        install.run(self)
#        installer = Installer()
#        installer.remove_old_version()
#        installer.reset_desktop_file()
#        #installer.addXuser_to_group()
#        installer.install_v2()

setup(
name = 'systemd-denotify',
version = '1.0',
description = 'systemd related desktop notifications',
long_description = 'A python based desktop app that notifies for user logins, failed systemd services, monitored files and the status of selected services',
author = 'George Karakougioumtzis <gkarakou>',
author_email = 'gkarakou@gmail.com',
url = 'https://github.com/gkarakou/systemd-denotify',
platforms = 'linux',
license = 'GPL-3.0',
packages = ['systemd-denotify'],
package_data = {'systemd-denotify': ['conf/*']},
install_requires= ['dbus-python', 'pygobject', 'python-systemd', 'pyinotify'],
#dependency_links = ["https://pypi.python.org/packages/source/p/python-systemd/python-systemd-0.0.9.tar.gz", "https://pypi.python.org/packages/source/P/PyGObject/pygobject-2.28.3.tar.bz2#md5=aa64900b274c4661a5c32e52922977f9", "https://pypi.python.org/packages/source/d/dbus-python/dbus-python-0.84.0.tar.gz", "https://pypi.python.org/packages/source/p/pyinotify/pyinotify-0.9.5.tar.gz"],
#cmdclass = {'install': MyInstall},
classifiers = ['Development Status :: 1.0 - Stable',
'Environment :: Desktop',
'Intended Audience :: End Users/Desktop',
'Intended Audience :: System Administrators',
'License :: GPL-3.0 ',
'Operating System :: Linux',
'Programming Language :: Python2.7'],
data_files = [('/etc', ['systemd-denotify/conf/systemd-denotify.conf']), ('/etc/xdg/autostart', ['systemd-denotify/conf/systemd-denotify.desktop'])],
scripts = ['scripts/systemd-denotify.py']
)
>>>>>>> build
