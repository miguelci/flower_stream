import fileinput

from bouquet_producer.events.event_dispatcher import EventDispatcher
from bouquet_producer.objects.flower import Flower
from bouquet_producer.output import Output
from bouquet_producer.entities.production_facility import ProductionFacility
from bouquet_producer.entities.warehouse import Warehouse

EVENT_DISPATCHER = EventDispatcher()
PRODUCTION_FACILITY = ProductionFacility(EVENT_DISPATCHER)
WAREHOUSE = Warehouse(EVENT_DISPATCHER)
OUTPUT = Output(EVENT_DISPATCHER)


def main():
    for line in fileinput.input():
        if not WAREHOUSE.needs_more_flowers:
            break
        line = line.strip()
        if not line:
            continue

        if len(line) > 2:
            PRODUCTION_FACILITY.add_bouquet(line)
        else:
            WAREHOUSE.add_flower(Flower(line[0], line[-1]))


if __name__ == "__main__":
    main()
