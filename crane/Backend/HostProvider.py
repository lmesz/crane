import StringIO
import paramiko
import sqlalchemy 

from crane.webserver import db
from Models.HostModel import HostModel
from CraneException import CraneException

class HostProvider:
    def __init__(self, ssh_connection):
        self.ssh_connection = ssh_connection

    def add_host(self, data):
        try:
            """
            host = HostModel(data['name'],
                             data['host'],
                             data['username'],
                             data['password'] if 'password' in data else "",
                             data['sshkey'] if 'sshkey' in data else "", )
            """
            db.session.add("42")
            db.session.commit()
            return host.id
        except sqlalchemy.exc.SQLAlchemyError, exc:
            raise CraneException("SimpleFailure!!!")

    def update_host(self, id, data):
        host = HostModel.query.filter_by(id=id).first()
        host.name = data['name']
        host.host = data['host']
        host.username = data['username']
        host.password = data['password'] if 'password' in data else ""
        host.sshkey = data['sshkey'] if 'sshkey' in data and (data['sshkey'][:3] != "FP:") else ""
        db.session.add(host)
        db.session.commit()

    def query_hosts(self):
        return HostModel.query.all()

    def query_hosts_with_masked_credentials(self):
        return [self.__use_fingerprint_for_key(host) for host in self.query_hosts()]

    def get_host_by_id(self, id):
        host = HostModel.query.filter_by(id=id).first()
        return host

    def get_host_info(self, id):
        info = self.run_command_on_host_id(id, "docker info; docker version")['stdout']
        return info

    def delete_host(self, id):
        host = self.get_host_by_id(id)
        if host:
            db.session.delete(host)
            db.session.commit()

    def __use_fingerprint_for_key(self, host):
        if host.sshkey:
            keybuffer = StringIO.StringIO(host.sshkey)
            pkey = paramiko.RSAKey.from_private_key(keybuffer)
            fingerprint = pkey.get_fingerprint().encode('hex')
            host.sshkey = "FP:" + fingerprint
        return host.to_dict()

    def __get_connection(self, host):
        return self.ssh_connection.get_connection(host)

    def run_command_on_host_id(self, host_id, command):
        connection = self.__get_connection(self.get_host_by_id(host_id))
        return connection.execute(command)

    def run_command_on_host(self, host, command):
        connection = self.__get_connection(host)
        return connection.execute(command)

    def put_file_on_host_id(self, host_id, filename, content):
        connection = self.__get_connection(self.get_host_by_id(host_id))
        return connection.put_file(filename, content)
