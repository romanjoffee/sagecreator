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
        instances = kwargs.get("instances")
        reservations = self.conn.get_all_instances(filters={"tag:Environment": env, "tag:Owner": owner, "tag:Service": service})
        counter = max([self.get_num_from_tag(i.tags['Name']) for r in reservations for i in r.instances if
                       'Name' in i.tags and '-' in i.tags['Name'] and i.state in ('running', 'pending', 'stopped')] or [0])

        ret_val = []
        counter = counter + 1
        for instance in instances:
            ret_val.append(dict(id=instance['id'],
                                name='{}-{}-{:02d}-{}'.format(owner, service, counter, env),
                                private_ip=instance['private_ip'],
                                public_dns_name=instance['public_dns_name'],
                                region=instance['region']))
            counter = counter + 1

        return ret_val

    def get_num_from_tag(self, str):
        if str:
            val = str.split('-')[-2]

            if val.isdigit():
                return int(val)

        return 0
