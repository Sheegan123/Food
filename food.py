import datetime

class Product:
    """Represents a food product."""
    def __init__(self, product_id, name, category, expiry_date=None):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.expiry_date = expiry_date

    def __str__(self):
        expiry_str = f"Expires on: {self.expiry_date.strftime('%Y-%m-%d')}" if self.expiry_date else "No expiry date"
        return f"Product ID: {self.product_id}, Name: {self.name}, Category: {self.category}, {expiry_str}"

class Location:
    """Represents a location in the supply chain (e.g., farm, warehouse, retailer)."""
    def __init__(self, location_id, name, location_type):
        self.location_id = location_id
        self.name = name
        self.location_type = location_type

    def __str__(self):
        return f"Location ID: {self.location_id}, Name: {self.name}, Type: {self.location_type}"

class InventoryItem:
    """Represents a specific quantity of a product at a location."""
    def __init__(self, product, location, quantity):
        self.product = product
        self.location = location
        self.quantity = quantity

    def __str__(self):
        return f"Product: {self.product.name}, Location: {self.location.name}, Quantity: {self.quantity}"

class Order:
    """Represents an order for food products."""
    def __init__(self, order_id, customer, order_date=None, items=None):
        self.order_id = order_id
        self.customer = customer
        self.order_date = order_date if order_date else datetime.date.today()
        self.items = items if items else {}  # {product_id: quantity}
        self.status = "Pending"

    def add_item(self, product_id, quantity):
        if product_id in self.items:
            self.items[product_id] += quantity
        else:
            self.items[product_id] = quantity

    def update_status(self, new_status):
        self.status = new_status

    def __str__(self):
        item_details = "\n  - ".join([f"{pid}: {qty}" for pid, qty in self.items.items()])
        return f"Order ID: {self.order_id}, Customer: {self.customer}, Date: {self.order_date}, Status: {self.status}\n  Items:\n  - {item_details}"

class Delivery:
    """Represents a delivery of an order."""
    def __init__(self, delivery_id, order, delivery_date=None, tracking_id=None):
        self.delivery_id = delivery_id
        self.order = order
        self.delivery_date = delivery_date
        self.tracking_id = tracking_id
        self.status = "Scheduled"

    def update_status(self, new_status):
        self.status = new_status

    def __str__(self):
        return f"Delivery ID: {self.delivery_id}, Order ID: {self.order.order_id}, Delivery Date: {self.delivery_date}, Tracking ID: {self.tracking_id}, Status: {self.status}"

class FoodSupplyChain:
    """Manages the distribution and delivery of food products."""
    def __init__(self):
        self.products = {}  # {product_id: Product}
        self.locations = {}  # {location_id: Location}
        self.inventory = {}  # {(product_id, location_id): InventoryItem}
        self.orders = {}  # {order_id: Order}
        self.deliveries = {}  # {delivery_id: Delivery}

    def add_product(self, product):
        if product.product_id not in self.products:
            self.products[product.product_id] = product
            print(f"Product '{product.name}' added.")
        else:
            print(f"Product with ID '{product.product_id}' already exists.")

    def add_location(self, location):
        if location.location_id not in self.locations:
            self.locations[location.location_id] = location
            print(f"Location '{location.name}' added.")
        else:
            print(f"Location with ID '{location.location_id}' already exists.")

    def add_inventory(self, product_id, location_id, quantity):
        if product_id in self.products and location_id in self.locations:
            key = (product_id, location_id)
            if key not in self.inventory:
                product = self.products[product_id]
                location = self.locations[location_id]
                self.inventory[key] = InventoryItem(product, location, quantity)
                print(f"{quantity} units of '{product.name}' added to '{location.name}'.")
            else:
                self.inventory[key].quantity += quantity
                print(f"{quantity} units of '{self.inventory[key].product.name}' added to '{self.inventory[key].location.name}'.")
        else:
            print("Invalid product ID or location ID.")

    def get_inventory(self, product_id, location_id):
        key = (product_id, location_id)
        return self.inventory.get(key)

    def place_order(self, customer, order_items):
        """Places a new order."""
        order_id = f"ORD-{len(self.orders) + 1}"
        new_order = Order(order_id, customer)
        for product_id, quantity in order_items.items():
            if product_id in self.products:
                new_order.add_item(product_id, quantity)
            else:
                print(f"Warning: Product with ID '{product_id}' not found.")
        self.orders[order_id] = new_order
        print(f"Order '{order_id}' placed by '{customer}'.")
        return new_order

    def fulfill_order(self, order_id):
        """Attempts to fulfill an order by checking inventory."""
        if order_id not in self.orders:
            print(f"Order with ID '{order_id}' not found.")
            return False

        order = self.orders[order_id]
        for product_id, quantity_needed in order.items.items():
            # Find a location with sufficient inventory (simplistic approach - could be optimized)
            found_inventory = None
            for (inv_prod_id, location_id), inventory_item in self.inventory.items():
                if inv_prod_id == product_id and inventory_item.quantity >= quantity_needed:
                    found_inventory = inventory_item
                    break

            if not found_inventory:
                print(f"Insufficient stock of '{self.products[product_id].name}' to fulfill order '{order_id}'.")
                return False
            else:
                found_inventory.quantity -= quantity_needed
                print(f"Shipped {quantity_needed} units of '{self.products[product_id].name}' from '{found_inventory.location.name}' for order '{order_id}'.")

        order.update_status("Fulfilled")
        print(f"Order '{order_id}' has been fulfilled.")
        return True

    def schedule_delivery(self, order_id, delivery_date=None):
        """Schedules a delivery for a fulfilled order."""
        if order_id not in self.orders:
            print(f"Order with ID '{order_id}' not found.")
            return None
        if self.orders[order_id].status != "Fulfilled":
            print(f"Order '{order_id}' is not yet fulfilled and cannot be scheduled for delivery.")
            return None

        delivery_id = f"DEL-{len(self.deliveries) + 1}"
        new_delivery = Delivery(delivery_id, self.orders[order_id], delivery_date)
        self.deliveries[delivery_id] = new_delivery
        print(f"Delivery '{delivery_id}' scheduled for order '{order_id}'.")
        return new_delivery

    def update_delivery_status(self, delivery_id, new_status):
        """Updates the status of a delivery."""
        if delivery_id in self.deliveries:
            self.deliveries[delivery_id].update_status(new_status)
            print(f"Delivery '{delivery_id}' status updated to '{new_status}'.")
        else:
            print(f"Delivery with ID '{delivery_id}' not found.")

    def track_delivery(self, delivery_id):
        """Tracks the status of a delivery."""
        if delivery_id in self.deliveries:
            return self.deliveries[delivery_id]
        else:
            print(f"Delivery with ID '{delivery_id}' not found.")
            return None

    def generate_inventory_report(self):
        """Generates a report of the current inventory."""
        print("\n--- Inventory Report ---")
        if not self.inventory:
            print("No inventory available.")
        else:
            for (prod_id, loc_id), item in self.inventory.items():
                print(item)
        print("-----------------------\n")

# Example Usage
if __name__ == "__main__":
    supply_chain = FoodSupplyChain()

    # Add products
    apple = Product("PROD-001", "Apple", "Fruits", datetime.date(2025, 5, 15))
    banana = Product("PROD-002", "Banana", "Fruits", datetime.date(2025, 4, 25))
    milk = Product("PROD-003", "Milk", "Dairy", datetime.date(2025, 4, 20))
    supply_chain.add_product(apple)
    supply_chain.add_product(banana)
    supply_chain.add_product(milk)

    # Add locations
    farm_a = Location("LOC-001", "Farm A", "Farm")
    warehouse_x = Location("LOC-002", "Warehouse X", "Warehouse")
    retailer_y = Location("LOC-003", "Retailer Y", "Retailer")
    supply_chain.add_location(farm_a)
    supply_chain.add_location(warehouse_x)
    supply_chain.add_location(retailer_y)

    # Add initial inventory
    supply_chain.add_inventory("PROD-001", "LOC-002", 100)  # 100 apples in Warehouse X
    supply_chain.add_inventory("PROD-002", "LOC-002", 150)  # 150 bananas in Warehouse X
    supply_chain.add_inventory("PROD-003", "LOC-002", 50)   # 50 milk cartons in Warehouse X

    supply_chain.add_inventory("PROD-001", "LOC-003", 20)   # 20 apples in Retailer Y
    supply_chain.add_inventory("PROD-003", "LOC-003", 10)   # 10 milk cartons in Retailer Y

    # Place an order
    customer_order = supply_chain.place_order("Alice", {"PROD-001": 5, "PROD-003": 2})
    print(customer_order)

    # Fulfill the order
    supply_chain.fulfill_order(customer_order.order_id)

    # Schedule delivery
    delivery = supply_chain.schedule_delivery(customer_order.order_id, datetime.date(2025, 4, 18))
    if delivery:
        delivery.tracking_id = "TRACK-12345"
        print(delivery)

        # Update delivery status
        supply_chain.update_delivery_status(delivery.delivery_id, "Out for Delivery")
        tracked_delivery = supply_chain.track_delivery(delivery.delivery_id)
        if tracked_delivery:
            print(f"Delivery Status: {tracked_delivery.status}")

    # Generate inventory report
    supply_chain.generate_inventory_report()
