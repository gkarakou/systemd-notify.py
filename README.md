# systemd-denotify
GENERAL
-------------------
systemd-denotify is a set of classes that leverage the power of systemd-python library and many other great python bindings(see the Dependencies section).
These classes provide desktop notification upon a user login, when systemd files are modified and when services fail(you will also be notified orally when systemd services fail).
There is also one class that at a specified interval (by default 30 minutes) notifies the user for the status of some services.
One can override the notifications he/she gets by editing the file /etc/systemd-denotify.conf.

NOTE: if you use vim to edit files that are being monitored by systemd-denotify.py in the /etc/systemd/ and /usr/lib/systemd/ directories you will be notified when the backup files that vim writes before saving a file that is modified are written too.
To overcome this annoyance if and only if you have a ups installed (in the case of a power failure you will lose data if you dont own a ups) you can edit /root/.vimrc and add these lines:
<pre>
set nobackup

set nowritebackup

set noswapfile
</pre>
Do this only if you own a ups, you have been warned.

REQUIREMENTS
-------------------

As the name implies you need to be running a modern linux distribution with systemd.
You also need a running Xorg, this script(though i like to call it a classy python app) wont work without a desktop session.
As a linux user you have to be comfortable with the terminal.

DEPENDENCIES
-------------------

Fedora 21:

<pre>
systemd-python notify-python pygobject2 python-slip-dbus espeak python-espeak python-inotify

</pre>
Arch Linux:

<pre>
python2 python2-notify python2-gobject python2-systemd python2-dbus espeak python-espeak python-pyinotify

</pre>

Debian:

<pre>
python-systemd python-dbus python-notify python-gobject python-gi espeak espeak-data python-espeak python-inotify

</pre>


-------------------------------

NOTE: There is a chance you installed the equivalent python3 packages. See below in the install section what to do.


INSTALL
------------------------
On a terminal:

<pre>git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

git checkout experimental

sudo python2 setup.py

</pre>


NOTE: If you installed the python3 dependencies

<pre>git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

git checkout experimental

sudo python2 setup.py -i v3
</pre>


NOTE for archlinux: if you have trouble installing you might have to pam_permit.so temporarilly in /etc/pam.d/usermod
and after the installation revert back your configuration.


UNINSTALL
-----------------------------

sudo python2 setup.py -u

BUILDING FOR DISTRIBUTIONS
----------------------------
There is a pypi ready dedicated branch to build binaries called build. However due to the complexity of downloading and installing all the dependencies through pip the module/app wont be uploaded to pypi.
I was successful in building and installing an rpm for fedora 21.
