# current API endpoints for the **LittleLemon** Restaurant

## Homepage
- http://127.0.0.1:8000/                    `GET`   returns homepage (rendered index.html file, using static assets)

## User
- http://127.0.0.1:8000/auth/users/         `POST`    provide *username* and *password* to create a user (sign up)
- http://127.0.0.1:8000/auth/token/login/   `POST`    provide *username* and *password* to generate a token (login)
- http://127.0.0.1:8000/auth/token/logout/  `POST`    provide *username* and *token* to destroy corresponding token (logout)
- http://127.0.0.1:8000/auth/users/         `GET`     provide *token* to return all users

## Manager Group
- http://127.0.0.1:8000/manager/            `POST`    provide *username* and *token* to add user to manager group
- http://127.0.0.1:8000/manager/            `GET`     provide *token* to return all users in manager group
- http://127.0.0.1:8000/manager/            `DELETE`  provide *username* and *token* to remove user from manager group

## Delivery Group
- http://127.0.0.1:8000/delivery/           `POST`    provide *username* and *token* to add user to delivery group
- http://127.0.0.1:8000/delivery/           `GET`     provide *token* to return all users in delivery group
- http://127.0.0.1:8000/delivery/           `DELETE`  provide *username* and *token* to remove user from delivery group

## Booking
- http://127.0.0.1:8000/booking/            `POST`    provide *name*, *num_guests*, *booking_date (YYYY-MM-DD)*, *booking_slot (10-22)*and *token* to add a **Booking**
- http://127.0.0.1:8000/booking/            `GET`     provide *token* to return all **Bookings**

## Menu
- http://127.0.0.1:8000/menu/               `POST`    provide *title*, *price* and *inventory* to add a **MenuItem**
- http://127.0.0.1:8000/menu/               `GET`     returns all **MenuItems**
- http://127.0.0.1:8000/menu/1              `GET`     returns **MenuItem** with specified pk
- http://127.0.0.1:8000/menu/1              `PUT`     provide *title*, *price* and *inventory* to update **MenuItem** with specified pk
- http://127.0.0.1:8000/menu/1              `PATCH`   provide one or many of *title*/ *price*/ *inventory* to modify **MenuItem** with specified pk
- http://127.0.0.1:8000/menu/1              `DELETE`  deletes **MenuItem** with specified pk

## Category
- http://127.0.0.1:8000/category/           `GET`     provide *token* to return all **Categories**
- http://127.0.0.1:8000/category/           `POST`    provide *title*, *slug* and *token* to add a **Category**
- http://127.0.0.1:8000/category/1          `GET`     provide *token* to return **Category** with specific pk
- http://127.0.0.1:8000/category/1          `DELETE`  provide *token* to delete **Category** with specific pk

## Cart
- http://127.0.0.1:8000/cart/               `GET`     provide *token* to return all **Carts** for corresponding user
- http://127.0.0.1:8000/cart/               `POST`    provide *menuitem_id*, *quantity* and *token* to add **Cart** to corresponding user
- http://127.0.0.1:8000/cart/               `DELETE`  provide *token* to delete all **Carts** from corresponding user
