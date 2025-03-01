import asyncio

from pyrego600 import HeatPump, SerialConnection


async def hp_example():
    connection = SerialConnection(url="socket://192.168.2.50:9265")
    hp = HeatPump(connection)

    try:
        print("Connecting to Heat Pump...")
        await hp.verify()
        print("Connected!")

        for register in hp.registers:
            value = await hp.read(register)
            print(f"register {register.identifier} = {value}")
    except Exception as e:
        print(f"Reading registries from Heat Pump failed due {e!r}")
    finally:
        await hp.dispose()


if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.run(hp_example())