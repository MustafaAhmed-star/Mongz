import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/models.dart';
import '../services/api_service.dart';

/// Order Service - Handles order API calls
class OrderService {
  final http.Client _client;
  final ApiService _authService;

  OrderService({
    http.Client? client,
    ApiService? authService,
  })  : _client = client ?? http.Client(),
        _authService = authService ?? ApiService();

  Map<String, String> get _headers {
    final headers = {'Content-Type': 'application/json'};
    // In a real app, you'd add auth token from ApiService
    return headers;
  }

  // Get user's orders
  Future<List<Order>> getOrders() async {
    final response = await _client.get(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.orders}'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Order.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load orders');
    }
  }

  // Get order by ID
  Future<Order> getOrderById(int id) async {
    final response = await _client.get(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.orderDetail}$id/'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return Order.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Order not found');
    }
  }

  // Create new order
  Future<Order> createOrder({
    required int serviceCategoryId,
    int? workerId,
  }) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.orders}'),
      headers: _headers,
      body: jsonEncode({
        'service_category': serviceCategoryId,
        if (workerId != null) 'worker': workerId,
      }),
    );

    if (response.statusCode == 201) {
      return Order.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to create order');
    }
  }

  // Accept order (worker only)
  Future<Order> acceptOrder(int orderId) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.orderAccept}$orderId/accept/'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return Order.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to accept order');
    }
  }

  // Reject order (worker only)
  Future<Order> rejectOrder(int orderId) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.orderReject}$orderId/reject/'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return Order.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to reject order');
    }
  }

  // Cancel order (client only)
  Future<Order> cancelOrder(int orderId) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.orderCancel}$orderId/cancel/'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return Order.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to cancel order');
    }
  }

  // Complete order (worker only)
  Future<Order> completeOrder(int orderId) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.orderComplete}$orderId/complete/'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return Order.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to complete order');
    }
  }

  // Submit rating
  Future<Rating> submitRating({
    required int orderId,
    required int workerId,
    required int stars,
    String review = '',
  }) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.ratings}'),
      headers: _headers,
      body: jsonEncode({
        'order': orderId,
        'worker': workerId,
        'stars': stars,
        'review': review,
      }),
    );

    if (response.statusCode == 201) {
      return Rating.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to submit rating');
    }
  }

  void dispose() {
    _client.close();
  }
}
