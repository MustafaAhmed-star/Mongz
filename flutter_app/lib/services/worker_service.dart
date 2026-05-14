import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/models.dart';
import '../services/api_service.dart';

/// Worker Service - Handles worker and category API calls
class WorkerService {
  final http.Client _client;
  final ApiService _authService;

  WorkerService({
    http.Client? client,
    ApiService? authService,
  })  : _client = client ?? http.Client(),
        _authService = authService ?? ApiService();

  // Get all service categories
  Future<List<ServiceCategory>> getCategories() async {
    final response = await _client.get(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.categories}'),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => ServiceCategory.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load categories');
    }
  }

  // Get workers list with optional filters
  Future<List<WorkerProfile>> getWorkers({
    int? categoryId,
    String? search,
  }) async {
    final uri = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.workers}').replace(
      queryParameters: {
        if (categoryId != null) 'category': categoryId.toString(),
        if (search != null) 'search': search,
      },
    );

    final response = await _client.get(uri);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final List<dynamic> results = data['results'] ?? data;
      return results.map((json) => WorkerProfile.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load workers');
    }
  }

  // Get worker by ID
  Future<WorkerProfile?> getWorkerById(int id) async {
    final response = await _client.get(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.workerDetail}$id/'),
    );

    if (response.statusCode == 200) {
      return WorkerProfile.fromJson(jsonDecode(response.body));
    } else {
      return null;
    }
  }

  // Create worker profile
  Future<WorkerProfile> createWorkerProfile({
    required String profession,
    int experienceYears = 0,
  }) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.workerCreate}'),
      headers: await _authService.getAuthHeaders(),
      body: jsonEncode({
        'profession': profession,
        'experience_years': experienceYears,
      }),
    );

    if (response.statusCode == 201) {
      return WorkerProfile.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to create worker profile');
    }
  }

  // Update worker profile
  Future<WorkerProfile> updateWorkerProfile({
    String? profession,
    int? experienceYears,
    bool? isAvailable,
  }) async {
    final body = <String, dynamic>{};
    if (profession != null) body['profession'] = profession;
    if (experienceYears != null) body['experience_years'] = experienceYears;
    if (isAvailable != null) body['is_available'] = isAvailable;

    final response = await _client.patch(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.workerMe}'),
      headers: await _authService.getAuthHeaders(),
      body: jsonEncode(body),
    );

    if (response.statusCode == 200) {
      return WorkerProfile.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to update worker profile');
    }
  }

  void dispose() {
    _client.close();
  }
}
