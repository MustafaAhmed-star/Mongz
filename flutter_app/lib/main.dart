import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../config/app_theme.dart';
import '../providers/auth_provider.dart';
import '../providers/worker_provider.dart';
import '../providers/order_provider.dart';
import '../providers/notification_provider.dart';
import '../screens/onboarding/splash_screen.dart';
import '../screens/onboarding/onboarding_screen.dart';
import '../screens/auth/login_screen.dart';
import '../screens/auth/register_screen.dart';
import '../screens/client/client_home_screen.dart';
import '../screens/client/order_detail_screen.dart';
import '../screens/client/create_order_screen.dart';
import '../screens/client/workers_list_screen.dart';
import '../screens/client/favorites_screen.dart';
import '../screens/client/profile_screen.dart';
import '../screens/worker/worker_home_screen.dart';
import '../screens/worker/worker_profile_screen.dart';
import '../screens/worker/worker_orders_screen.dart';
import '../screens/worker/availability_toggle_screen.dart';
import '../screens/common/notifications_screen.dart';
import '../screens/common/settings_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize providers and load saved data before running app
  final authProvider = AuthProvider();
  await authProvider.loadUser();
  
  runApp(MyApp(authProvider: authProvider));
}

class MyApp extends StatelessWidget {
  final AuthProvider authProvider;
  
  const MyApp({super.key, required this.authProvider});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: authProvider),
        ChangeNotifierProvider(create: (_) => WorkerProvider()),
        ChangeNotifierProvider(create: (_) => OrderProvider()),
        ChangeNotifierProvider(create: (_) => NotificationProvider()),
      ],
      child: MaterialApp.router(
        title: 'Service Hub',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        routerConfig: _router,
      ),
    );
  }
}

// GoRouter configuration
final GoRouter _router = GoRouter(
  initialLocation: '/splash',
  routes: [
    // Onboarding & Auth Routes
    GoRoute(
      path: '/splash',
      builder: (context, state) => const SplashScreen(),
    ),
    GoRoute(
      path: '/onboarding',
      builder: (context, state) => const OnboardingScreen(),
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: '/register',
      builder: (context, state) => const RegisterScreen(),
    ),
    
    // Client Routes
    GoRoute(
      path: '/client/home',
      builder: (context, state) => const ClientHomeScreen(),
    ),
    GoRoute(
      path: '/client/orders/:id',
      builder: (context, state) => OrderDetailScreen(
        orderId: int.parse(state.pathParameters['id']!),
      ),
    ),
    GoRoute(
      path: '/client/orders/create',
      builder: (context, state) => const CreateOrderScreen(),
    ),
    GoRoute(
      path: '/client/workers',
      builder: (context, state) => WorkersListScreen(
        categoryId: state.uri.queryParameters['category'] != null 
            ? int.parse(state.uri.queryParameters['category']!) 
            : null,
      ),
    ),
    GoRoute(
      path: '/client/favorites',
      builder: (context, state) => const FavoritesScreen(),
    ),
    GoRoute(
      path: '/client/profile',
      builder: (context, state) => const ProfileScreen(),
    ),
    
    // Worker Routes
    GoRoute(
      path: '/worker/home',
      builder: (context, state) => const WorkerHomeScreen(),
    ),
    GoRoute(
      path: '/worker/profile',
      builder: (context, state) => const WorkerProfileScreen(),
    ),
    GoRoute(
      path: '/worker/orders',
      builder: (context, state) => const WorkerOrdersScreen(),
    ),
    GoRoute(
      path: '/worker/availability',
      builder: (context, state) => const AvailabilityToggleScreen(),
    ),
    
    // Common Routes
    GoRoute(
      path: '/notifications',
      builder: (context, state) => const NotificationsScreen(),
    ),
    GoRoute(
      path: '/settings',
      builder: (context, state) => const SettingsScreen(),
    ),
  ],
);
