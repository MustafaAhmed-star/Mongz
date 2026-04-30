import 'package:flutter/material.dart';
import '../models/models.dart';
import '../services/order_service.dart';

/// Order Provider - Manages orders state
class OrderProvider extends ChangeNotifier {
  final OrderService _orderService = OrderService();
  
  List<Order> _orders = [];
  Order? _selectedOrder;
  bool _isLoading = false;
  String? _error;

  List<Order> get orders => _orders;
  Order? get selectedOrder => _selectedOrder;
  bool get isLoading => _isLoading;
  String? get error => _error;

  // Load user's orders
  Future<void> loadOrders() async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      _orders = await _orderService.getOrders();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  // Get order by ID
  Future<Order?> getOrderById(int id) async {
    _isLoading = true;
    notifyListeners();
    
    try {
      _selectedOrder = await _orderService.getOrderById(id);
      _isLoading = false;
      notifyListeners();
      return _selectedOrder;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return null;
    }
  }

  // Create new order
  Future<Order?> createOrder({
    required int serviceCategoryId,
    int? workerId,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      final order = await _orderService.createOrder(
        serviceCategoryId: serviceCategoryId,
        workerId: workerId,
      );
      _orders.insert(0, order);
      _isLoading = false;
      notifyListeners();
      return order;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return null;
    }
  }

  // Accept order (worker only)
  Future<bool> acceptOrder(int orderId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      final order = await _orderService.acceptOrder(orderId);
      final index = _orders.indexWhere((o) => o.id == orderId);
      if (index != -1) {
        _orders[index] = order;
      }
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Reject order (worker only)
  Future<bool> rejectOrder(int orderId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      final order = await _orderService.rejectOrder(orderId);
      final index = _orders.indexWhere((o) => o.id == orderId);
      if (index != -1) {
        _orders[index] = order;
      }
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Cancel order (client only)
  Future<bool> cancelOrder(int orderId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      final order = await _orderService.cancelOrder(orderId);
      final index = _orders.indexWhere((o) => o.id == orderId);
      if (index != -1) {
        _orders[index] = order;
      }
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Complete order (worker only)
  Future<bool> completeOrder(int orderId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      final order = await _orderService.completeOrder(orderId);
      final index = _orders.indexWhere((o) => o.id == orderId);
      if (index != -1) {
        _orders[index] = order;
      }
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Submit rating for completed order
  Future<bool> submitRating({
    required int orderId,
    required int workerId,
    required int stars,
    String review = '',
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      await _orderService.submitRating(
        orderId: orderId,
        workerId: workerId,
        stars: stars,
        review: review,
      );
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _orderService.dispose();
    super.dispose();
  }
}
