/// Worker Profile model matching Django backend
class WorkerProfile {
  final int? id;
  final User user;
  final String profession;
  final int experienceYears;
  final double averageRating;
  final int completedJobs;
  final bool isAvailable;
  final DateTime? createdAt;
  final double score;

  WorkerProfile({
    this.id,
    required this.user,
    required this.profession,
    this.experienceYears = 0,
    this.averageRating = 0.0,
    this.completedJobs = 0,
    this.isAvailable = true,
    this.createdAt,
    this.score = 0.0,
  });

  factory WorkerProfile.fromJson(Map<String, dynamic> json) {
    return WorkerProfile(
      id: json['id'],
      user: User.fromJson(json['user'] ?? {}),
      profession: json['profession'] ?? '',
      experienceYears: json['experience_years'] ?? 0,
      averageRating: (json['average_rating'] ?? 0).toDouble(),
      completedJobs: json['completed_jobs'] ?? 0,
      isAvailable: json['is_available'] ?? true,
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : null,
      score: (json['score'] ?? 0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user': user.toJson(),
      'profession': profession,
      'experience_years': experienceYears,
      'average_rating': averageRating,
      'completed_jobs': completedJobs,
      'is_available': isAvailable,
      'created_at': createdAt?.toIso8601String(),
      'score': score,
    };
  }
}
