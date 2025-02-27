from pysnmp.hlapi.v3arch.asyncio import *
import asyncio
import datetime

class JuniperComponentMonitor:
    def __init__(self, community, agent_ip, interval):
        self.community = community
        self.agent_ip = agent_ip
        self.interval = interval
        self.snmp_engine = SnmpEngine()

    async def get_hostname(self, target):
        hostname_oid = ObjectIdentity('1.3.6.1.2.1.1.5.0')
        response = await get_cmd(
            self.snmp_engine,
            CommunityData(self.community),
            target,
            ContextData(),
            ObjectType(hostname_oid)
        )
        errorIndication, errorStatus, errorIndex, varBinds = response
        if errorIndication:
            print("Error retrieving hostname:", errorIndication)
            return None
        elif errorStatus:
            print(f"Error Status at {errorIndex}: {errorStatus.prettyPrint()}")
            return None
        else:
            return str(varBinds[0][1])

    async def walk_oid(self, target, base_oid):
        data = {}
        next_oid = base_oid
        
        while next_oid is not None:
            response = await next_cmd(
                self.snmp_engine,
                CommunityData(self.community),
                target,
                ContextData(),
                ObjectType(next_oid)
            )
            errorIndication, errorStatus, errorIndex, varBinds = response
            if errorIndication:
                print("Error during SNMP walk:", errorIndication)
                break
            elif errorStatus:
                print(f"Error Status at {errorIndex}: {errorStatus.prettyPrint()}")
                break
            else:
                for varBind in varBinds:
                    oid, value = varBind
                    if str(oid).startswith(str(base_oid)):
                        data[str(oid)] = value
                        next_oid = oid
                    else:
                        next_oid = None
                        break
        return data

    async def poll_data(self):
        target = await UdpTransportTarget.create((self.agent_ip, 161))
        
        # Get hostname
        hostname = await self.get_hostname(target)
        if not hostname:
            print("Failed to retrieve hostname.")
            return

        # OIDs for Juniper components
        oids = {
            "jnxOperatingDescr": "1.3.6.1.4.1.2636.3.1.13.1.5",
            "jnxOperatingMemoryCP": "1.3.6.1.4.1.2636.3.1.13.1.28",
            "jnxOperating1MinLoadAvg": "1.3.6.1.4.1.2636.3.1.13.1.20",
            "jnxOperating5MinLoadAvg": "1.3.6.1.4.1.2636.3.1.13.1.21",
            "jnxOperating15MinLoadAvg": "1.3.6.1.4.1.2636.3.1.13.1.22",
            "jnxOperatingMemory": "1.3.6.1.4.1.2636.3.1.13.1.15",
            "jnxOperatingBufferCP": "1.3.6.1.4.1.2636.3.1.13.1.27",
            "jnxOperating1MinAvgCPU": "1.3.6.1.4.1.2636.3.1.13.1.23",
            "jnxOperatingBufferExt": "1.3.6.1.4.1.2636.3.1.13.1.29",
            "jnxOperatingTemperature": "1.3.6.1.4.1.2636.3.1.13.1.30"
        }

        # Walk each OID
        component_data = {key: await self.walk_oid(target, ObjectIdentity(oid)) for key, oid in oids.items()}

        # Organize structured data
        device_data = {hostname: []}

        # Build component mapping from jnxOperatingDescr
        for oid, desc in component_data["jnxOperatingDescr"].items():
            component_id = oid[len(oids["jnxOperatingDescr"]):]  # Extract instance ID
            device_data[hostname].append({
                "instance_id": component_id,
                "jnxOperatingDescr": str(desc),
                "jnxOperatingMemoryCP": int(component_data["jnxOperatingMemoryCP"].get(f'{oids["jnxOperatingMemoryCP"]}{component_id}', 0)),
                "jnxOperating1MinLoadAvg": int(component_data["jnxOperating1MinLoadAvg"].get(f'{oids["jnxOperating1MinLoadAvg"]}{component_id}', 0)),
                "jnxOperating5MinLoadAvg": int(component_data["jnxOperating5MinLoadAvg"].get(f'{oids["jnxOperating5MinLoadAvg"]}{component_id}', 0)),
                "jnxOperating15MinLoadAvg": int(component_data["jnxOperating15MinLoadAvg"].get(f'{oids["jnxOperating15MinLoadAvg"]}{component_id}', 0)),
                "jnxOperatingMemory": int(component_data["jnxOperatingMemory"].get(f'{oids["jnxOperatingMemory"]}{component_id}', 0)),
                "jnxOperatingBufferCP": int(component_data["jnxOperatingBufferCP"].get(f'{oids["jnxOperatingBufferCP"]}{component_id}', 0)),
                "jnxOperating1MinAvgCPU": int(component_data["jnxOperating1MinAvgCPU"].get(f'{oids["jnxOperating1MinAvgCPU"]}{component_id}', 0)),
                "jnxOperatingBufferExt": int(component_data["jnxOperatingBufferExt"].get(f'{oids["jnxOperatingBufferExt"]}{component_id}', 0)),
                "jnxOperatingTemperature": int(component_data["jnxOperatingTemperature"].get(f'{oids["jnxOperatingTemperature"]}{component_id}', 0))
            })

        return device_data

    async def start_polling(self):
        while True:
            data = await self.poll_data()
            print("Polling Result:", data)
            await asyncio.sleep(self.interval)

# Usage example:
if __name__ == "__main__":
    monitor = JuniperComponentMonitor(
        community='HeartInt_Ld5s2024$',
        agent_ip='10.93.166.60',
        interval=300  # Polling every 5 minutes
    )
    asyncio.run(monitor.start_polling())
