/// API Configuration
class ApiConfig {
  // Update this to your Django backend URL
  static const String baseUrl = 'http://localhost:8000/api';
  
  // Endpoints
  static const String register = '/register/';
  static const String login = '/login/';
  static const String me = '/me/';
  
  // Workers endpoints
  static const String workers = '/workers/';
  static const String workerDetail = '/workers/';
  static const String workerCreate = '/workers/create/';
  static const String workerMe = '/workers/me/';
  static const String categories = '/categories/';
  
  // Orders endpoints
  static const String orders = '/orders/';
  static const String orderDetail = '/orders/';
  static const String orderAccept = '/orders/';
  static const String orderReject = '/orders/';
  static const String orderCancel = '/orders/';
  static const String orderComplete = '/orders/';
  
  // Favorites endpoints
  static const String favorites = '/favorites/';
  
  // Ratings endpoints
  static const String ratings = '/ratings/';
  
  // Notifications endpoints
  static const String notifications = '/notifications/';
  
  // Payments endpoints
  static const String payments = '/payments/';
  
  // Timeout settings
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
}
