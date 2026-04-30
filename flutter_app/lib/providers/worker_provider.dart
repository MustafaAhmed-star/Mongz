import 'package:flutter/material.dart';
import '../models/models.dart';
import '../services/worker_service.dart';

/// Worker Provider - Manages workers and categories state
class WorkerProvider extends ChangeNotifier {
  final WorkerService _workerService = WorkerService();
  
  List<WorkerProfile> _workers = [];
  List<ServiceCategory> _categories = [];
  bool _isLoading = false;
  String? _error;

  List<WorkerProfile> get workers => _workers;
  List<ServiceCategory> get categories => _categories;
  bool get isLoading => _isLoading;
  String? get error => _error;

  // Load all service categories
  Future<void> loadCategories() async {
    _isLoading = true;
    notifyListeners();
    
    try {
      _categories = await _workerService.getCategories();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  // Load workers with optional filters
  Future<void> loadWorkers({
    int? categoryId,
    String? search,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      _workers = await _workerService.getWorkers(
        categoryId: categoryId,
        search: search,
      );
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  // Get worker by ID
  Future<WorkerProfile?> getWorkerById(int id) async {
    try {
      return await _workerService.getWorkerById(id);
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return null;
    }
  }

  // Create worker profile (for workers only)
  Future<bool> createWorkerProfile({
    required String profession,
    int experienceYears = 0,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      await _workerService.createWorkerProfile(
        profession: profession,
        experienceYears: experienceYears,
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

  // Update worker profile
  Future<bool> updateWorkerProfile({
    String? profession,
    int? experienceYears,
    bool? isAvailable,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      await _workerService.updateWorkerProfile(
        profession: profession,
        experienceYears: experienceYears,
        isAvailable: isAvailable,
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

  // Search workers
  Future<void> searchWorkers(String query) async {
    await loadWorkers(search: query);
  }

  // Filter workers by category
  Future<void> filterWorkersByCategory(int categoryId) async {
    await loadWorkers(categoryId: categoryId);
  }

  @override
  void dispose() {
    _workerService.dispose();
    super.dispose();
  }
}
