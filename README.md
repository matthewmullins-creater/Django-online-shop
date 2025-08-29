# Online Store - Django Backend Project

A comprehensive e-commerce project focusing on backend development using the Django framework.  
This project includes advanced modules for product management, users, payments, and customer interactions.

## 🌟 Key Features
- **Advanced Authentication**  
  Login/Logout with one-time password (OTP) via SMS (using Kavenegar service).
- **Product Management**  
  Categorization, advanced search, filtering, and sorting + Discount and coupon system.
- **Smart Cart**  
  Add/Remove products, real-time updates with AJAX, and payment gateway integration.
- **User Panel**  
  Profile editing, order tracking, and wishlist management.
- **Comment System**  
  Admin-approved commenting + product rating system.
- **Product Comparison**  
  Create comparison tables for related products.
- **Simple API**  
  Get product list in JSON format (`/test_api/products/`).

## 🛠 Project Applications
| Application       | Description                          |
|-------------------|--------------------------------------|
| `accounts`        | User management & authentication    |
| `products`        | Product catalog & categorization    |
| `orders`          | Shopping cart & orders               |
| `payments`        | Payment gateways & transactions      |
| `discounts`       | Smart coupon & discount system       |
| `comment_scoring_favorit...` | Comments, ratings & wishlists        |
| `warehouses`      | Inventory management                 |
| `search`          | Advanced search with dynamic filters |

## 🚀 Project Setup
1. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/shop.git
   cd shop
   ```

2. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate    # For Windows
   pip install -r requirements.txt
   ```

3. **Database Configuration** (in `settings.py`):  
   Configure `DATABASES` for MySQL connection.

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create Admin User**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## 🔧 Used Technologies
- **Core Platform**: Django 5.1
- **Database**: MySQL
- **Authentication**: SMS OTP (Kavenegar API)
- **Content Editor**: Django-CKEditor
- **Payment**: Iranian Gateways (Extendable)


## 📌 Technical Notes
- Using **Class-Based Views** & **Django REST Framework** for clean logic
- **AJAX Integration** in: Cart, Wishlist, and Comments
- **Custom Middlewares** for access control and logging
- **Unit Tests** for critical modules (Under development)

## 📥 Contribution
Project is actively developed! To contribute:
1. Fork the repository
2. Create your feature branch
3. Submit a Pull Request

## 📅 Roadmap
- Add blog section with commenting capability
- Integrate product recommendation system
- More details to be implemented on site

---