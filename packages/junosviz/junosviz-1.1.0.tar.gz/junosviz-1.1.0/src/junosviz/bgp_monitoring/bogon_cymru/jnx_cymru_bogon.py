import requests
import logging
from ncclient import manager
from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result

class BogonPrefixManager:
    def __init__(self, prefix_name, log_file):
        self.prefix_name = prefix_name
        self.log_file = log_file
        
        # Configure logging dynamically
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def fetch_bogon_prefixes(self):
        url = "https://team-cymru.org/Services/Bogons/fullbogons-ipv4.txt"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Extract prefixes, ignoring comments and empty lines
            prefixes = [line.strip() for line in response.text.splitlines() if line and not line.startswith('#')]

            logging.info(f"Fetched {len(prefixes)} bogon prefixes.")
            return prefixes
        except requests.RequestException as e:
            logging.error(f"Error fetching bogon prefixes: {e}")
            return None  # Return None to indicate failure

    def create_bogon_prefix_rpc(self, prefixes):
        config = f"""
        <config>
          <configuration>
            <policy-options>
              <prefix-list>
                <name>{self.prefix_name}</name>
        """
        for prefix in prefixes:
            config += f"<prefix-list-item><name>{prefix}</name></prefix-list-item>"
        config += """
              </prefix-list>
            </policy-options>
          </configuration>
        </config>
        """
        return config

    def delete_bogon_prefix_list(self, task: Task):
        host = task.host.hostname
        port = task.host.get("port", 830)
        username = task.host.username
        password = task.host.password
        
        delete_rpc = f"""
        <config>
          <configuration>
            <policy-options>
              <prefix-list operation="delete">
                <name>{self.prefix_name}</name>
              </prefix-list>
            </policy-options>
          </configuration>
        </config>
        """

        try:
            logging.info(f"Connecting to {host} via NETCONF for deletion...")
            with manager.connect(
                host=host,
                port=port,
                username=username,
                password=password,
                hostkey_verify=False,
                device_params={'name': 'junos'},
                allow_agent=False,
                look_for_keys=False,
                timeout=30
            ) as m:
                logging.info(f"Deleting existing bogon prefix list on {host}...")
                m.edit_config(target='candidate', config=delete_rpc)
                m.commit()
                logging.info(f"Successfully deleted bogon prefix list on {host}.")
        except Exception as e:
            logging.error(f"Error deleting prefix list on {host}: {e}")

    def update_bogon_prefix_list(self, task: Task):
        prefixes = self.fetch_bogon_prefixes()
        
        if prefixes is None:
            logging.warning("Failed to fetch prefixes. Removing existing prefix list.")
            self.delete_bogon_prefix_list(task)
            return Result(host=task.host, failed=True, result="Prefix fetch failed, deleted existing list.")
        
        if not prefixes:
            logging.warning("No prefixes to update.")
            return Result(host=task.host, failed=True, result="No prefixes fetched.")

        host = task.host.hostname
        port = task.host.get("port", 830)
        username = task.host.username
        password = task.host.password

        try:
            logging.info(f"Connecting to {host} via NETCONF...")
            with manager.connect(
                host=host,
                port=port,
                username=username,
                password=password,
                hostkey_verify=False,
                device_params={'name': 'junos'},
                allow_agent=False,
                look_for_keys=False,
                timeout=30
            ) as m:

                # Add new bogon prefix list
                bogon_prefix_rpc = self.create_bogon_prefix_rpc(prefixes)
                logging.info(f"Applying bogon prefix list on {host}...")
                m.edit_config(target='candidate', config=bogon_prefix_rpc)

                # Commit the changes
                logging.info(f"Committing changes on {host}...")
                m.commit()

                logging.info(f"Successfully updated bogon prefixes on {host}.")
                return Result(host=task.host, result="Success")
        except Exception as e:
            logging.error(f"Error updating {host}: {e}")
            return Result(host=task.host, failed=True, result=str(e))

# Main function using Nornir
def main():
    nr = InitNornir(config_file="/home/dco/nms/nornir/config.yaml")
    devices = nr.filter(F(groups__contains="ld5-dfz"))
    log_file_path = "/home/dco/nms/nornir/scripts/bogon_update.log"  # Change path as needed
    prefix_manager = BogonPrefixManager("cymru-bogon-v4-prefixes", log_file_path)
    
    # Execute the task on all matching devices
    result = devices.run(task=prefix_manager.update_bogon_prefix_list)
    logging.info("Bogon prefix update process completed.")
    print(result)

if __name__ == "__main__":
    main()
