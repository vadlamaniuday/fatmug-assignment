
This project is a Django application for managing vendors and purchase orders, including tracking historical performance metrics. The application provides RESTful APIs for interacting with vendor and purchase order data.

## Installation

To run this application locally, follow these steps:

1.  **Clone the repository:**
    
    bash
   
-   `git clone https://github.com/vadlamaniuday/fatmug-assignment.git` 
    
-   **Install dependencies:**
    
-   `pip install -r requirements.txt` 
    
-   **Apply migrations:**
    
-   `python manage.py migrate` 
    
-   **Run the development server:**
    

1.  `python manage.py runserver` 
    

## API Endpoints

### Vendors

-   `GET /api/vendors/`: Retrieve a list of all vendors.
-   `POST /api/vendors/`: Create a new vendor.
-   `GET /api/vendors/<int:pk>/`: Retrieve details of a specific vendor.
-   `PUT /api/vendors/<int:pk>/`: Update details of a specific vendor.
-   `DELETE /api/vendors/<int:pk>/`: Delete a specific vendor.

### Purchase Orders

-   `GET /api/purchase_orders/`: Retrieve a list of all purchase orders.
-   `POST /api/purchase_orders/`: Create a new purchase order.
-   `GET /api/purchase_orders/<int:pk>/`: Retrieve details of a specific purchase order.
-   `PUT /api/purchase_orders/<int:pk>/`: Update details of a specific purchase order.
-   `DELETE /api/purchase_orders/<int:pk>/`: Delete a specific purchase order.
-   `POST /api/purchase_orders/<int:po_id>/acknowledge/`: Record acknowledgment of a purchase order.

### Vendor Performance

-   `GET /api/vendors/<int:vendor_id>/performance/`: Retrieve performance metrics for a specific vendor.

## Models

### Vendor

-   `name`: Name of the vendor.
-   `contact_details`: Contact details of the vendor.
-   `address`: Address of the vendor.
-   `vendor_code`: Unique code assigned to the vendor.
-   `on_time_delivery_rate`: Rate of on-time delivery (percentage).
-   `quality_rating_avg`: Average quality rating (out of 5).
-   `average_response_time`: Average response time (in seconds).
-   `fulfillment_rate`: Rate of order fulfillment (percentage).

### PurchaseOrder

-   `po_number`: Purchase order number (unique).
-   `vendor`: Foreign key to the Vendor model.
-   `order_date`: Date and time of order creation.
-   `delivery_date`: Date and time of delivery.
-   `items`: JSON field containing order items.
-   `quantity`: Quantity of items ordered.
-   `status`: Status of the purchase order (pending/completed).
-   `quality_rating`: Quality rating provided for the order.
-   `issue_date`: Date and time of order issuance.
-   `acknowledgment_date`: Date and time of acknowledgment.

### HistoricalPerformance

-   `vendor`: Foreign key to the Vendor model.
-   `date`: Date and time of performance recording.
-   `on_time_delivery_rate`: Rate of on-time delivery (percentage).
-   `quality_rating_avg`: Average quality rating (out of 5).
-   `average_response_time`: Average response time (in seconds).
-   `fulfillment_rate`: Rate of order fulfillment (percentage).


### Testing with Postman

1.  **Download and Install Postman**: If you haven't already, download and install Postman.
    
2.  **Launch Postman**: Open Postman on your computer.
    
3.  **Test the Endpoints**:
    
    -   **GET Requests**: Use the appropriate endpoint URLs to send GET requests and retrieve data. 
    -   **POST Requests**: Send POST requests to create new resources. Make sure to include the required parameters in the request body.
    -   **PUT Requests**: Update existing resources by sending PUT requests with the updated data. Specify the resource ID in the URL.
    -   **DELETE Requests**: Delete resources by sending DELETE requests with the resource ID in the URL.
    -   **Testing Performance Endpoint**: To test the performance metrics endpoint, send a GET request to `http://localhost:8000/api/vendors/<vendor_id>/performance/`, replacing `<vendor_id>` with the ID of the vendor.
    -   **Acknowledging Purchase Orders**: To record acknowledgment of a purchase order, send a POST request to `http://localhost:8000/api/purchase_orders/<po_id>/acknowledge/`, replacing `<po_id>` with the ID of the purchase order.

## Additional Notes

-   The application includes validation checks for ensuring data integrity.
-   Performance metrics are calculated dynamically based on historical data.
-   RESTful APIs are implemented using Django REST Framework.
