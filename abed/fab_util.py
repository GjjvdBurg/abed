from fabric.api import env
from fabric.context_managers import cd as fab_cd
from fabric.context_managers import settings as fab_settings
from fabric.operations import hide, run, put, get

from .conf import settings


class MyFabric(object):
    """
    Class to manage env etc.
    """

    def __init__(self):
        self.host = settings.REMOTE_HOST
        self.user = settings.REMOTE_USER
        self.name = settings.PROJECT_NAME
        self.environment = "staging"
        self.project_path = settings.REMOTE_DIR
        self.port = settings.REMOTE_PORT
        self.data_path = None
        self.empty = None
        # Use the ssh config of the user. If a password is still requested,
        # ensure that the key is added with ``ssh-add /path/to/key``.
        env.use_ssh_config = True

    def run(self, command="", warn_only=False, cd=None):
        env.host_string = "%s@%s:%s" % (self.user, self.host, self.port)
        if self.empty is None:
            with hide("output"):
                self.empty = str(run("echo"))
        if cd is None:
            cd = "/home/{}".format(self.user)
        with (fab_cd(cd)):
            with fab_settings(warn_only=warn_only):
                with hide("output"):
                    output = str(run(command))
        text = output[len(self.empty) + 1 :].replace("\r", "").strip()
        return text

    def get(self, source, dest):
        env.host_string = "%s@%s:%s" % (self.user, self.host, self.port)
        get(source, dest)

    def put(self, source, dest):
        env.host_string = "%s@%s:%s" % (self.user, self.host, self.port)
        put(source, dest)


if settings is None:
    myfab = None
else:
    myfab = MyFabric()
