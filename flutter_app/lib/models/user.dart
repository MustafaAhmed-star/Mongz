/// User model matching Django backend
class User {
  final int? id;
  final String username;
  final String email;
  final String phone;
  final String address;
  final String role; // 'client', 'worker', 'admin'
  final DateTime? dateJoined;

  User({
    this.id,
    required this.username,
    required this.email,
    required this.phone,
    this.address = '',
    this.role = 'client',
    this.dateJoined,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      username: json['username'] ?? '',
      email: json['email'] ?? '',
      phone: json['phone'] ?? '',
      address: json['address'] ?? '',
      role: json['role'] ?? 'client',
      dateJoined: json['date_joined'] != null 
          ? DateTime.parse(json['date_joined']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'phone': phone,
      'address': address,
      'role': role,
      'date_joined': dateJoined?.toIso8601String(),
    };
  }

  bool get isClient => role == 'client';
  bool get isWorker => role == 'worker';
  bool get isAdmin => role == 'admin';

  User copyWith({
    int? id,
    String? username,
    String? email,
    String? phone,
    String? address,
    String? role,
    DateTime? dateJoined,
  }) {
    return User(
      id: id ?? this.id,
      username: username ?? this.username,
      email: email ?? this.email,
      phone: phone ?? this.phone,
      address: address ?? this.address,
      role: role ?? this.role,
      dateJoined: dateJoined ?? this.dateJoined,
    );
  }
}
