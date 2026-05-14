import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/models.dart';
import '../services/api_service.dart';

/// Notification Service - Handles notification API calls
class NotificationService {
  final http.Client _client;
  final ApiService _authService;

  NotificationService({
    http.Client? client,
    ApiService? authService,
  })  : _client = client ?? http.Client(),
        _authService = authService ?? ApiService();

  // Get all notifications for current user
  Future<List<Notification>> getNotifications() async {
    final response = await _client.get(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.notifications}'),
      headers: await _authService.getAuthHeaders(),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Notification.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load notifications');
    }
  }

  // Mark notification as read
  Future<void> markAsRead(int notificationId) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.notifications}$notificationId/read/'),
      headers: await _authService.getAuthHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to mark notification as read');
    }
  }

  // Mark all notifications as read
  Future<void> markAllAsRead() async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.notifications}read-all/'),
      headers: await _authService.getAuthHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to mark all notifications as read');
    }
  }

  void dispose() {
    _client.close();
  }
}
