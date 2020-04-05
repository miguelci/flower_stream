from bouquet_producer.events.event import Event


class AvailableEvents(Event):
    FLOWER_REMOVED = 'FlowerRemoved'
    FLOWER_ADDED_TO_STOCK = 'FlowerAddedToStock'
    FLOWER_REMOVED_FROM_STOCK = 'FlowerRemovedFromStock'
    BOUQUET_DESIGN_COMPLETED = 'BouquetDesignCompleted'
    NO_MORE_BOUQUETS = 'NoMoreBouquets'
