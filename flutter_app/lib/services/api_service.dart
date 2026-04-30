import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config/api_config.dart';
import '../models/models.dart';

/// API Service for communicating with Django backend
class ApiService {
  final http.Client _client;
  final FlutterSecureStorage _storage;
  
  String? _accessToken;
  String? _refreshToken;

  ApiService({
    http.Client? client,
    FlutterSecureStorage? storage,
  })  : _client = client ?? http.Client(),
        _storage = storage ?? const FlutterSecureStorage();

  // Get headers with auth token
  Map<String, String> get _headers {
    final headers = {'Content-Type': 'application/json'};
    if (_accessToken != null) {
      headers['Authorization'] = 'Bearer $_accessToken';
    }
    return headers;
  }

  // Save tokens to secure storage
  Future<void> _saveTokens(AuthTokens tokens) async {
    _accessToken = tokens.accessToken;
    _refreshToken = tokens.refreshToken;
    await _storage.write(key: 'access_token', value: tokens.accessToken);
    await _storage.write(key: 'refresh_token', value: tokens.refreshToken);
  }

  // Load tokens from secure storage
  Future<void> loadTokens() async {
    _accessToken = await _storage.read(key: 'access_token');
    _refreshToken = await _storage.read(key: 'refresh_token');
  }

  // Clear tokens on logout
  Future<void> clearTokens() async {
    _accessToken = null;
    _refreshToken = null;
    await _storage.delete(key: 'access_token');
    await _storage.delete(key: 'refresh_token');
  }

  // Check if user is authenticated
  bool get isAuthenticated => _accessToken != null;

  // Register new user
  Future<AuthResponse> register({
    required String username,
    required String email,
    required String password,
    required String phone,
    String role = 'client',
  }) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
        'phone': phone,
        'role': role,
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      final authResponse = AuthResponse.fromJson(data);
      await _saveTokens(authResponse.tokens);
      return authResponse;
    } else {
      throw ApiException(
        statusCode: response.statusCode,
        message: jsonDecode(response.body)['message'] ?? 'Registration failed',
      );
    }
  }

  // Login
  Future<AuthResponse> login({
    required String username,
    required String password,
  }) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final authResponse = AuthResponse.fromJson(data);
      await _saveTokens(authResponse.tokens);
      return authResponse;
    } else {
      throw ApiException(
        statusCode: response.statusCode,
        message: jsonDecode(response.body)['message'] ?? 'Login failed',
      );
    }
  }

  // Get current user profile
  Future<User> getMyProfile() async {
    final response = await _client.get(
      Uri.parse('${ApiConfig.baseUrl}/me/'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return User.fromJson(jsonDecode(response.body));
    } else {
      throw ApiException(
        statusCode: response.statusCode,
        message: 'Failed to load profile',
      );
    }
  }

  // Update user profile
  Future<User> updateProfile({
    String? email,
    String? phone,
    String? address,
  }) async {
    final body = <String, dynamic>{};
    if (email != null) body['email'] = email;
    if (phone != null) body['phone'] = phone;
    if (address != null) body['address'] = address;

    final response = await _client.patch(
      Uri.parse('${ApiConfig.baseUrl}/me/'),
      headers: _headers,
      body: jsonEncode(body),
    );

    if (response.statusCode == 200) {
      return User.fromJson(jsonDecode(response.body));
    } else {
      throw ApiException(
        statusCode: response.statusCode,
        message: 'Failed to update profile',
      );
    }
  }

  // Logout
  Future<void> logout() async {
    await clearTokens();
  }

  void dispose() {
    _client.close();
  }
}

// Custom exception for API errors
class ApiException implements Exception {
  final int statusCode;
  final String message;

  ApiException({required this.statusCode, required this.message});

  @override
  String toString() => 'ApiException: $statusCode - $message';
}
