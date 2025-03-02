import requests
import time
import urllib3
import csv
import json
from random import randint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ProxmoxManager:
    def __init__(
        self, proxmox_url, proxmox_user, proxmox_password, node, verify_ssl=False
    ):
        """
        Initialize the ProxmoxManager with the required parameters.

        Args:
            proxmox_url (str): The URL of the Proxmox VE server.
            proxmox_user (str): The username to authenticate with.
            proxmox_password (str): The password to authenticate with.
            node (str): The Proxmox VE node to manage.
            verify_ssl (bool): Whether to verify SSL certificates. Defaults to False.
        """
        self.proxmox_url = proxmox_url
        self.proxmox_user = proxmox_user
        self.proxmox_password = proxmox_password
        self.node = node
        self.verify_ssl = verify_ssl
        self.vm_data_headers = ["VMID", "OWNER", "HNAME"]
        self.vm_data = []
        self.raw_data = ""

    def write_vm_data(self):
        """
        Write VM data to a CSV file.

        This method is usually internal and is used to dump data on range VMs to a CSV file.
        """
        with open("data.csv", "w", newline="") as file:
            csv_writer = csv.DictWriter(file, fieldnames=self.vm_data_headers)
            csv_writer.writeheader()
            csv_writer.writerows(self.vm_data)

    def read_vm_data(self):
        """
        Read VM data from a CSV file.

        This method is usually internal and is used to load data on range VMs from a CSV file.
        """
        with open("data.csv", "r") as file:
            reader = csv.DictReader(file)
            self.vm_data = [row for row in reader]
            self.raw_data = file.read()

    def authenticate(self):
        """
        Authenticate with the Proxmox VE host and obtain a ticket and CSRF token.

        This method is usually internal and is used to authorize with the PVE host.

        Returns:
            tuple: A tuple containing the ticket and CSRF token.
        """
        response = requests.post(
            f"{self.proxmox_url}/access/ticket",
            data={"username": self.proxmox_user, "password": self.proxmox_password},
            verify=self.verify_ssl,
        )
        response.raise_for_status()
        data = response.json()["data"]
        return data["ticket"], data["CSRFPreventionToken"]

    def get_next_vm_id(self, ticket=None):
        """
        Get the next available VMID for clone/create operations.

        Args:
            ticket (str, optional): The authentication ticket.

        Returns:
            int: The next available VMID.
        """
        next_id_url = f"{self.proxmox_url}/cluster/nextid"
        if not ticket:
            ticket, _ = self.authenticate()
        headers = {"Cookie": f"PVEAuthCookie={ticket}"}
        response = requests.get(next_id_url, headers=headers, verify=self.verify_ssl)
        response.raise_for_status()
        next_id = response.json()["data"]
        return next_id

    def clone_vm(self, template_id, new_name, new_id):
        """
        Clone a VM or template to a new VMID and assign a new name.

        Args:
            template_id (int): The ID of the template to clone.
            new_name (str): The new name for the cloned VM.
            new_id (int): The new VMID for the cloned VM.

        Returns:
            dict: The response data from the clone operation.
        """
        clone_url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{template_id}/clone"
        ticket, csrf_token = self.authenticate()
        headers = {
            "Cookie": f"PVEAuthCookie={ticket}",
            "CSRFPreventionToken": csrf_token,
        }
        payload = {
            "newid": new_id,
            "name": new_name,
            "node": self.node,
            "vmid": template_id,
        }
        response = requests.post(
            clone_url, headers=headers, data=payload, verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.json()["data"]

    def assign_admin_vm_permissions(self, vm_id, user):
        """
        Assign admin permissions to a user for a given VMID.

        Args:
            vm_id (int): The ID of the VM.
            user (str): The user to assign admin permissions to.
        """
        ticket, csrf_token = self.authenticate()
        acl_url = f"{self.proxmox_url}/access/acl"
        headers = {
            "Cookie": f"PVEAuthCookie={ticket}",
            "CSRFPreventionToken": csrf_token,
        }
        payload = {"path": f"/vms/{vm_id}", "users": user, "roles": "Administrator"}
        response = requests.put(
            acl_url, headers=headers, data=payload, verify=self.verify_ssl
        )
        response.raise_for_status()

    def set_vm_desc(self, vm_id, desc):
        """
        Set the description (Notes) of a VMID.

        Args:
            vm_id (int): The ID of the VM.
            desc (str): The description to set for the VM.
        """
        conf_url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vm_id}/config"
        ticket, csrf_token = self.authenticate()
        headers = {
            "Cookie": f"PVEAuthCookie={ticket}",
            "CSRFPreventionToken": csrf_token,
        }
        payload = {
            "description": desc,
        }
        response = requests.put(
            conf_url, headers=headers, data=payload, verify=self.verify_ssl
        )
        response.raise_for_status()

    def destroy_vm(self, vmid):
        """
        Destroy a VM by its ID.

        Args:
            vmid (int): The ID of the VM to destroy.
        """
        ticket, csrf_token = self.authenticate()
        delete_url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}"
        headers = {
            "Cookie": f"PVEAuthCookie={ticket}",
            "CSRFPreventionToken": csrf_token,
        }
        response = requests.delete(delete_url, headers=headers, verify=self.verify_ssl)
        response.raise_for_status()
        self.vm_data = [vm for vm in self.vm_data if str(vm["VMID"]) != str(vmid)]
        self.write_vm_data()
        print(f"VM {vmid} on node {self.node} has been destroyed.")

    def create_user(self, new_username, new_password, realm, name=None):
        """
        Create a new user in the given realm

        Args:
            new_username (str): The username (typically short and lowercase, e.g 'john')
            new_password (str): The user's new password
            realm (str): Which realm the user belongs to (typically 'pve' or 'pam' unless your cluster has external authentication sources configured)
            name (str, optional): Human-readable long name for user (e.g. 'John Doe')
        """
        ticket, csrf_token = self.authenticate()
        url = f"{self.proxmox_url}/access/users"
        headers = {
            "CSRFPreventionToken": csrf_token,
            "Cookie": f"PVEAuthCookie={ticket}",
        }

        data = {
            "userid": f"{new_username}@{realm}",
            "password": new_password,
            "firstname": name,
        }

        response = requests.post(
            url, headers=headers, data=data, verify=self.verify_ssl
        )

        response.raise_for_status()

    def set_user_group(self, user, group):
        """
        Set the group of a user

        Args:
            user (str): The username of the user (include realm, e.g. 'john@pve')
            group (str): The group to assign to the user
        """
        ticket, csrf_token = self.authenticate()
        url = f"{self.proxmox_url}/access/users/{user}"
        headers = {
            "CSRFPreventionToken": csrf_token,
            "Cookie": f"PVEAuthCookie={ticket}",
        }

        data = {"groups": group}

        response = requests.put(url, headers=headers, data=data, verify=self.verify_ssl)

        response.raise_for_status()

    def list_users(self):
        """
        Internal method. Returns data array about active users in the cluster
        """
        ticket, csrf_token = self.authenticate()
        url = f"{self.proxmox_url}/access/users"
        headers = {
            "CSRFPreventionToken": csrf_token,
            "Cookie": f"PVEAuthCookie={ticket}",
        }

        response = requests.get(url, headers=headers, verify=self.verify_ssl)

        if response.status_code == 200:
            data = json.loads(response.text)
            return data["data"]
        else:
            return {"status": response.status_code, "message": "response.text"}

    def check_if_user(self, find_userid):
        """
        Check wether or not given username exists in given realm

        Args:
            find_userid (str): user id to search for (full userid, e.g. 'foo@pve')
        """
        users = self.list_users()
        for userdict in users:
            if userdict["userid"] == find_userid:
                return True

        return False

    def destroy_range(self):
        """
        Destroy all range VMs.
        """
        self.read_vm_data()
        for vm in self.vm_data:
            print("Destroying VMID " + str(vm["VMID"]))
            self.set_vm_power_status(vm["VMID"], "stop")
            self.destroy_vm(vm["VMID"])

    def create_range(self, ids, user):
        """
        Create cloned VMs for a given username.

        Args:
            ids (list): A list of VMIDs to clone.
            user (str): The username to assign to the cloned VMs. Defaults to None.
        """
        template_vm_ids = ids
        uf = user.split("@")[0]
        new_instance_names = [uf + "-win1", uf + "-win2", uf + "-win3"]

        ticket, _ = self.authenticate()
        for template_id, new_name in zip(template_vm_ids, new_instance_names):
            new_id = self.get_next_vm_id(ticket)
            self.clone_vm(template_id, new_name, new_id)
            time.sleep(2)
            self.assign_admin_vm_permissions(new_id, user)

            data = {
                "VMID": str(new_id),
                "OWNER": user,
                "HNAME": new_name,
            }
            self.vm_data.append(data)

            print(
                f"VMID - {new_id}, {new_name} cloned from template {template_id} and permissions assigned to {user}"
            )
            self.write_vm_data()

    def apply_sdn(self):
        """
        Apply SDN settings to the cluster.
        """

        url = f"{self.proxmox_url}/cluster/sdn"
        ticket, csrf_token = self.authenticate()

        headers = {
            "Cookie": f"PVEAuthCookie={ticket}",
            "CSRFPreventionToken": csrf_token,
        }

        response = requests.put(url, headers=headers, verify=self.verify_ssl)

        return response.json()

    def add_subnet_to_vnet(self, vnet_id, subnet_cidr, subnet_gateway):
        """
        Add a subnet to a given VNET ID.

        Args:
            vnet_id (int): The ID of the VNET.
            subnet_cidr (str): The CIDR notation of the subnet to add.
        """
        vnet_url = f"{self.proxmox_url}/cluster/sdn/vnets/{vnet_id}/subnets"

        ticket, csrf_token = self.authenticate()

        headers = {
            "Cookie": f"PVEAuthCookie={ticket}",
            "CSRFPreventionToken": csrf_token,
        }

        payload = {
            "subnet": subnet_cidr,
            "snat": True,
            "gateway": subnet_gateway,
            "type": "subnet",
        }

        response = requests.post(
            vnet_url, headers=headers, json=payload, verify=self.verify_ssl
        )

        # self.apply_sdn()

        return str(response.json())

    def destroy_subnet(self, vnet, subnet_cidr):
        """
        Destroy a subnet from a given VNET ID.

        Args:
            vnet (int): The ID of the VNET.
            subnet_cidr (str): The CIDR notation of the subnet to add.
        """
        vnet_url = f"{self.proxmox_url}/cluster/sdn/vnets/{vnet}/subnets/{subnet_cidr}"
        ticket, csrf_token = self.authenticate()

        headers = {
            "Cookie": f"PVEAuthCookie={ticket}",
            "CSRFPreventionToken": csrf_token,
        }

        response = requests.delete(vnet_url, headers=headers, verify=self.verify_ssl)

        return str(response.json())

    def set_vm_power_status(self, vmid, state):
        """
        Set the power state of a VM

        Args:
            vmid (int): The ID of the VM
            state (str): The desired state of the VM. One of "start", "stop", "reset", "shutdown", "suspend", "resume", or "reboot"
        """
        ticket, csrf_token = self.authenticate()
        if state == "start":
            url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}/status/start"
        elif state == "stop":
            url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}/status/stop"
        elif state == "reset":
            url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}/status/reset"
        elif state == "shutdown":
            url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}/status/shutdown"
        elif state == "suspend":
            url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}/status/suspend"
        elif state == "resume":
            url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}/status/resume"
        elif state == "reboot":
            url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}/status/reboot"
        else:
            return "Invalid state"

        headers = {
            "Cookie": f"PVEAuthCookie={ticket}",
            "CSRFPreventionToken": csrf_token,
        }

        response = requests.post(url, headers=headers, verify=self.verify_ssl)

    def set_password(self, user, passw):
        """
        Set the password of a user

        Args:
            user (str): The username of the user (include realm, e.g. 'john@pve')
            passw (str): The new
        """
        ticket, csrf_token = self.authenticate()
        url = f"{self.proxmox_url}/access/password"
        headers = {
            "CSRFPreventionToken": csrf_token,
            "Cookie": f"PVEAuthCookie={ticket}",
        }
        body = {"userid": user, "password": passw}
        response = requests.put(url, headers=headers, data=body, verify=self.verify_ssl)

    def snapshot_vm(
        self, vmid, snapshot_name, description=None, vmstate=False, snode=None
    ):
        """
        Create a snapshot for a given VMID.

        Args:
            vmid (int): The ID of the VM.
            snapshot_name (str): The name of the snapshot.
            description (str, optional): The description of the snapshot.
            vmstate (bool, optional): Whether to save the VM state (RAM). Defaults to False.
            snode (str, optional): Node that the VM is on (if different than the API node)
        """

        snap_node = None
        if snode:
            snap_node = snode
        else:
            snap_node = self.node

        snapshot_url = f"{self.proxmox_url}/nodes/{snap_node}/qemu/{vmid}/snapshot"
        ticket, csrf_token = self.authenticate()
        headers = {
            "Cookie": f"PVEAuthCookie={ticket}",
            "CSRFPreventionToken": csrf_token,
        }
        payload = {
            "snapname": snapshot_name,
            "vmstate": vmstate,
        }
        if description:
            payload["description"] = description

        response = requests.post(
            snapshot_url, headers=headers, json=payload, verify=self.verify_ssl
        )

        return response.json()


if __name__ == "__main__":
    print("Stop it")
