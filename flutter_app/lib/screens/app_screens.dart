import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Mongz', subtitle: 'Service marketplace');
  }
}

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Welcome', subtitle: 'Find trusted workers near you.');
  }
}

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Login', subtitle: 'Connect this screen to AuthProvider.');
  }
}

class RegisterScreen extends StatelessWidget {
  const RegisterScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Create Account', subtitle: 'Register as client or worker.');
  }
}

class ClientHomeScreen extends StatelessWidget {
  const ClientHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Client Home', subtitle: 'Browse services and create orders.');
  }
}

class OrderDetailScreen extends StatelessWidget {
  final int orderId;

  const OrderDetailScreen({super.key, required this.orderId});

  @override
  Widget build(BuildContext context) {
    return _SimpleScreen(title: 'Order #$orderId', subtitle: 'Order details will appear here.');
  }
}

class CreateOrderScreen extends StatelessWidget {
  const CreateOrderScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Create Order', subtitle: 'Choose a service and worker.');
  }
}

class WorkersListScreen extends StatelessWidget {
  final int? categoryId;

  const WorkersListScreen({super.key, this.categoryId});

  @override
  Widget build(BuildContext context) {
    final suffix = categoryId == null ? 'All categories' : 'Category $categoryId';
    return _SimpleScreen(title: 'Workers', subtitle: suffix);
  }
}

class FavoritesScreen extends StatelessWidget {
  const FavoritesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Favorites', subtitle: 'Saved workers.');
  }
}

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Profile', subtitle: 'Account information.');
  }
}

class WorkerHomeScreen extends StatelessWidget {
  const WorkerHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Worker Home', subtitle: 'Manage incoming orders.');
  }
}

class WorkerProfileScreen extends StatelessWidget {
  const WorkerProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Worker Profile', subtitle: 'Edit skills and experience.');
  }
}

class WorkerOrdersScreen extends StatelessWidget {
  const WorkerOrdersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Worker Orders', subtitle: 'Accept, reject, and complete jobs.');
  }
}

class AvailabilityToggleScreen extends StatelessWidget {
  const AvailabilityToggleScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Availability', subtitle: 'Switch your worker status.');
  }
}

class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Notifications', subtitle: 'Unread updates and messages.');
  }
}

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const _SimpleScreen(title: 'Settings', subtitle: 'Application preferences.');
  }
}

class _SimpleScreen extends StatelessWidget {
  final String title;
  final String subtitle;

  const _SimpleScreen({required this.title, required this.subtitle});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                title,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              const SizedBox(height: 12),
              Text(
                subtitle,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyLarge,
              ),
              const SizedBox(height: 24),
              FilledButton(
                onPressed: () => context.go('/client/home'),
                child: const Text('Home'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
