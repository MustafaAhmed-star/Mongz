/// Rating model matching Django backend
class Rating {
  final int? id;
  final int orderId;
  final int clientId;
  final int workerId;
  final int stars; // 1 to 5
  final String review;
  final DateTime? createdAt;

  Rating({
    this.id,
    required this.orderId,
    required this.clientId,
    required this.workerId,
    this.stars = 5,
    this.review = '',
    this.createdAt,
  });

  factory Rating.fromJson(Map<String, dynamic> json) {
    return Rating(
      id: json['id'],
      orderId: json['order'] ?? json['order_id'] ?? 0,
      clientId: json['client'] ?? json['client_id'] ?? 0,
      workerId: json['worker'] ?? json['worker_id'] ?? 0,
      stars: json['stars'] ?? 5,
      review: json['review'] ?? '',
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'order': orderId,
      'client': clientId,
      'worker': workerId,
      'stars': stars,
      'review': review,
      'created_at': createdAt?.toIso8601String(),
    };
  }
}
