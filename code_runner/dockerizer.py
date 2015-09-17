import docker


class DockerContainer(object):

    def __init__(self, container_id):
        self.cid = container_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.remove_container(self.cid)

    def run(self):
        try:
            self.client = docker.Client(base_url='unix://var/run/docker.sock')
            self.container = self.client.create_container(
                image='python:2.7',
                command="python /mnt/temp/%s.py" % self.cid,
                name=self.cid,
                host_config=self.client.create_host_config(
                    binds={
                        '/home/vagrant/pywars/tempfiles': {'bind': '/mnt/temp/',
                                                           'mode': 'rw'}})
                )

            self.client.start(self.cid)
            self.client.wait(self.cid)
            return self.client.logs(self.cid)
        except Exception as e:
            # TODO
            raise e
