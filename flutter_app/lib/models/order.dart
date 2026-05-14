/// Order model matching Django backend
class Order {
  final int? id;
  final int clientId;
  final int? workerId;
  final int serviceCategoryId;
  final String serviceCategoryName;
  final String description;
  final double commission;
  final String status; // PENDING, ACCEPTED, REJECTED, CANCELLED, COMPLETED
  final DateTime? createdAt;
  final DateTime? acceptedAt;
  final DateTime? completedAt;
  final DateTime? cancelledAt;
  final String? paymentKey;

  Order({
    this.id,
    required this.clientId,
    this.workerId,
    required this.serviceCategoryId,
    this.serviceCategoryName = '',
    this.description = '',
    this.commission = 0.0,
    this.status = 'PENDING',
    this.createdAt,
    this.acceptedAt,
    this.completedAt,
    this.cancelledAt,
    this.paymentKey,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    final client = json['client'];
    final worker = json['worker'];
    final serviceCategory = json['service_category'];

    return Order(
      id: json['id'],
      clientId: client is Map ? client['id'] ?? 0 : json['client_id'] ?? client ?? 0,
      workerId: worker is Map ? worker['id'] : json['worker_id'] ?? worker,
      serviceCategoryId: serviceCategory is Map
          ? serviceCategory['id'] ?? 0
          : json['service_category_id'] ?? serviceCategory ?? 0,
      serviceCategoryName: json['service_category_name'] ?? 
          (json['service_category'] is Map ? json['service_category']['name'] ?? '' : ''),
      description: json['description'] ?? '',
      commission: double.tryParse(json['commission']?.toString() ?? '0') ?? 0.0,
      status: json['status'] ?? 'PENDING',
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : null,
      acceptedAt: json['accepted_at'] != null 
          ? DateTime.parse(json['accepted_at']) 
          : null,
      completedAt: json['completed_at'] != null 
          ? DateTime.parse(json['completed_at']) 
          : null,
      cancelledAt: json['cancelled_at'] != null 
          ? DateTime.parse(json['cancelled_at']) 
          : null,
      paymentKey: json['payment_key'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'client': clientId,
      'worker': workerId,
      'service_category': serviceCategoryId,
      'service_category_name': serviceCategoryName,
      'description': description,
      'commission': commission.toString(),
      'status': status,
      'created_at': createdAt?.toIso8601String(),
      'accepted_at': acceptedAt?.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
      'cancelled_at': cancelledAt?.toIso8601String(),
      'payment_key': paymentKey,
    };
  }

  bool get isPending => status == 'PENDING';
  bool get isAccepted => status == 'ACCEPTED';
  bool get isRejected => status == 'REJECTED';
  bool get isCancelled => status == 'CANCELLED';
  bool get isCompleted => status == 'COMPLETED';

  Order copyWith({
    int? id,
    int? clientId,
    int? workerId,
    int? serviceCategoryId,
    String? serviceCategoryName,
    String? description,
    double? commission,
    String? status,
    DateTime? createdAt,
    DateTime? acceptedAt,
    DateTime? completedAt,
    DateTime? cancelledAt,
    String? paymentKey,
  }) {
    return Order(
      id: id ?? this.id,
      clientId: clientId ?? this.clientId,
      workerId: workerId ?? this.workerId,
      serviceCategoryId: serviceCategoryId ?? this.serviceCategoryId,
      serviceCategoryName: serviceCategoryName ?? this.serviceCategoryName,
      description: description ?? this.description,
      commission: commission ?? this.commission,
      status: status ?? this.status,
      createdAt: createdAt ?? this.createdAt,
      acceptedAt: acceptedAt ?? this.acceptedAt,
      completedAt: completedAt ?? this.completedAt,
      cancelledAt: cancelledAt ?? this.cancelledAt,
      paymentKey: paymentKey ?? this.paymentKey,
    );
  }
}
