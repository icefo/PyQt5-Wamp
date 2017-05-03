import asyncio
from datetime import datetime

from autobahn import wamp
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class MyBackend(ApplicationSession):
    def __init__(self, config=None):
        super().__init__(config)

        # print the contents of the 'extra' parameter set below
        print(config.extra)

    @wamp.register("com.myapp.add")
    @asyncio.coroutine
    def add(self, list_of_number):
        result = 0

        for x in list_of_number:
            try:
                x = float(x)
            except ValueError:
                x = 0
            result += x
        print('The addition of {0} = {1}'.format(list_of_number, result))
        yield from asyncio.sleep(3)  # simulate processing time
        return result

    @asyncio.coroutine
    def onJoin(self, details):
        print("session ready")
        try:
            res = yield from self.register(self)
            print("{0} procedures registered".format(len(res)))
        except Exception as e:
            print("could not register procedure: {0}".format(e))

        asyncio.async(self.time_teller())

    @asyncio.coroutine
    def time_teller(self):
        while True:
            time_now = str(datetime.now().replace(microsecond=0))
            self.publish('com.myapp.the_time', time_now)
            yield from asyncio.sleep(2)


if __name__ == "__main__":
    runner = ApplicationRunner(url="ws://127.0.0.1:8080/ws", realm="realm1",
                               extra={'key': 'value that will be passed to MyBackend'})
    runner.run(MyBackend)
