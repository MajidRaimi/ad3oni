import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'repositories/prayers_repository.dart';
import 'repositories/taxonomy_repository.dart';

/// App-wide infrastructure providers (DI roots) shared by the controllers.
///
/// State management uses Riverpod: each controller is a [ChangeNotifier] exposed
/// through a [ChangeNotifierProvider] declared next to it, and these providers
/// supply the dependencies those controllers need.

/// The single [SharedPreferences] instance. Overridden in `main()` with the
/// real instance loaded before `runApp`.
final sharedPreferencesProvider = Provider<SharedPreferences>(
  (ref) => throw UnimplementedError(
    'sharedPreferencesProvider must be overridden in ProviderScope',
  ),
);

/// Data access for du'as (`/v1/prayers`).
final prayersRepositoryProvider =
    Provider<PrayersRepository>((ref) => PrayersRepository());

/// Data access for the reference taxonomy (`/v1/groups|types|categories`).
final taxonomyRepositoryProvider =
    Provider<TaxonomyRepository>((ref) => TaxonomyRepository());
