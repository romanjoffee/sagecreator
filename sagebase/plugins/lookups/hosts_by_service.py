from ansible.plugins.lookup import LookupBase
import boto.ec2


class LookupModule(LookupBase):

    def __init__(self, loader=None, templar=None, **kwargs):
        super(LookupModule, self).__init__(loader, templar, **kwargs)
        self.conn = boto.ec2.connect_to_region('us-east-1')

    def run(self, terms, variables=None, **kwargs):
        env = kwargs.get("env")
        owner = kwargs.get("owner")
        service = kwargs.get("service")
        reservations = self.conn.get_all_instances(filters={"tag:Environment": env, "tag:Owner": owner, "tag:Service": service})
        ret_val = []
        for r in reservations:
            for instance in r.instances:
                if instance.state == "running" or instance.state == "pending":
                    ret_val.append({"ip_address": instance.ip_address, "private_ip_address": instance.private_ip_address})

        return ret_val
