import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/controllers/saved_controller.dart';
import '../../../core/controllers/taxonomy_controller.dart';
import '../../add_dua/screens/add_dua_screen.dart';
import '../../home/screens/home_screen.dart';
import '../../saved/screens/saved_screen.dart';
import '../../search/controller/search_controller.dart';
import '../../search/screens/search_screen.dart';
import '../../settings/controller/settings_controller.dart';
import '../controller/shell_controller.dart';

/// The app shell: an RTL bottom navigation over the four feature screens
/// (Home · All du'as · Add · Saved).
class RootShell extends ConsumerStatefulWidget {
  const RootShell({super.key});

  @override
  ConsumerState<RootShell> createState() => _RootShellState();
}

class _RootShellState extends ConsumerState<RootShell> {
  @override
  void initState() {
    super.initState();
    // Eagerly instantiate the app-wide controllers (matches the previous
    // MultiProvider eager creation): settings pushes the widget interval,
    // taxonomy/search start loading, saved restores from local storage.
    ref.read(settingsControllerProvider);
    ref.read(savedControllerProvider);
    ref.read(taxonomyControllerProvider);
    ref.read(duaSearchControllerProvider);
  }

  @override
  Widget build(BuildContext context) {
    final shell = ref.watch(shellControllerProvider);
    return Scaffold(
      body: IndexedStack(
        index: shell.index,
        children: const [
          HomeScreen(),
          SearchScreen(),
          AddDuaScreen(),
          SavedScreen(),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: shell.index,
        onDestinationSelected: shell.setIndex,
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home_rounded),
            label: 'الرئيسية',
          ),
          NavigationDestination(
            icon: Icon(Icons.search_outlined),
            selectedIcon: Icon(Icons.search_rounded),
            label: 'كل الأدعية',
          ),
          NavigationDestination(
            icon: Icon(Icons.add_circle_outline),
            selectedIcon: Icon(Icons.add_circle_rounded),
            label: 'إضافة',
          ),
          NavigationDestination(
            icon: Icon(Icons.bookmark_border_rounded),
            selectedIcon: Icon(Icons.bookmark_rounded),
            label: 'المحفوظات',
          ),
        ],
      ),
    );
  }
}
