import dotenv
from pydantic import BaseModel

from neurion_ganglion.db.ion_usage import IonUsageDAO
from neurion_ganglion.ion.ion import Ion, ion_handler
from neurion_ganglion.server.server import GanglionServer

dotenv.load_dotenv()
# Define Input Schema
class MyInputSchema(BaseModel):
    message: str
    result: float

# Define Output Schema
class MyOutputSchema(BaseModel):
    message: str
    result: float

# Use decorator to attach schemas
@ion_handler(MyInputSchema, MyOutputSchema)
def my_ion_handler(data: MyInputSchema) -> MyOutputSchema:
    """Handles execution logic."""
    return MyOutputSchema(message="Success", result=data.result*10)


async def main():
    await IonUsageDAO.increment_usage("ion1s39200s6v4c96ml2xzuh389y3pd0guk2u9u2qt",'neurion1s39200s6v4c96ml2xzuh389yxpd0guk2u9u2qt')

# Start Ion Server
if __name__ == "__main__":
    # description = "My custom Ion server"
    # stake = 20000000
    # fee_per_thousand_calls = 1
    # capacities = [Capacity.SCRAPER, Capacity.AI_AGENT]
    # wallet = get_wallet()
    # print(str(wallet.address()))
    #
    # # Start auto-hosted Ion server
    # Ion.create_self_hosting_ion(NetworkConfig.neurion_alpha_testnet(), description, stake, fee_per_thousand_calls,
    #                             capacities, my_ion_handler).start()
    # Ion.start_pure_ion_server(my_ion_handler)


    # Start Ion with custom host and port
    # endpoints = ["http://167.99.69.198:8000"]
    # Ion.create_server_ready_ion(description,stake,fee_per_thousand_calls,capacities,MyInputSchema,MyOutputSchema,endpoints).register_ion()


    # asyncio.run(main())

    GanglionServer.start()

    # ion=Ion.at('ion1s39200s6v4c96ml2xzuh389yxpd0guk2u9u2qt')
    # print(ion.endpoints)
    # NetworkConfig.neurion_localnet()
    # NetworkConfig.neurion_alpha_testnet()